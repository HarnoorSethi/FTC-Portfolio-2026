"""Tiny layout engine: one drawing API -> real .pptx (python-pptx) + PIL preview (overflow checking)."""
import re, math, copy, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 144  # preview px per inch
HEAD_FONT = "Montserrat"
BODY_FONT = "Montserrat"
EMPH_FONT = "Montserrat Medium"  # reference emphasis weight (measured vs ByteForce PDF)
LS_MULT = 1.0
LS_BODY = 1.20  # reference line pitch / font size (measured), body copy
LS_DISPLAY = 1.15  # large single-line display text


def pitch_pt(size, ls=1.0):
    return size * (LS_BODY if size <= 10.2 else LS_DISPLAY) * ls

PREV = {
    "body": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "head": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "ital": "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
}
_fc = {}


MONT = "/tmp/work/fonts/Montserrat-VF.ttf"
_VAR = {"body": b"Regular", "bold": b"Medium", "head": b"Bold", "ital": b"Regular"}


def pfont(kind, px):
    k = (kind, round(px, 2))
    if k not in _fc:
        if os.path.exists(MONT):
            f = ImageFont.truetype(MONT, max(1, px))
            try:
                f.set_variation_by_name(_VAR.get(kind, b"Regular"))
            except Exception:
                pass
            _fc[k] = f
        else:
            _fc[k] = ImageFont.truetype(PREV[kind], max(1, int(px * 1.07)))
    return _fc[k]


def rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def tup(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * a))


COL = dict(o="F7941D", b="1456B8", w="FFFFFF", k="1D2433", g="5E6B7D", n="0B1F3A", h="FFC53D", r="D64545", e="2E9E5B")
WARN = []


class Deck:
    def __init__(self, w=8.5, h=11):
        self.prs = Presentation()
        self.prs.slide_width = Inches(w)
        self.prs.slide_height = Inches(h)
        self.w, self.h = w, h
        self.pages = []

    def page(self, bg="FFFFFF", name=""):
        p = Page(self, bg, name)
        self.pages.append(p)
        return p

    def save(self, path):
        self.prs.save(path)


class Page:
    def __init__(self, deck, bg, name):
        self.deck = deck
        self.name = name
        self.slide = deck.prs.slides.add_slide(deck.prs.slide_layouts[6])
        self.slide.background.fill.solid()
        self.slide.background.fill.fore_color.rgb = rgb(bg)
        self.img = Image.new("RGB", (int(deck.w * S), int(deck.h * S)), "#" + bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.regions = []
        self.imgs = []

    # ---------- primitives ----------
    def _style(self, shp, fill, line, lw, alpha=None, dash=None):
        shp.shadow.inherit = False
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(fill)
            if alpha is not None:
                clr = shp.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
                a = etree.SubElement(clr, qn("a:alpha"))
                a.set("val", str(int(alpha * 100000)))
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(lw)
            if dash:
                ln = shp.line._get_or_add_ln()
                pd = etree.SubElement(ln, qn("a:prstDash"))
                pd.set("val", "dash")

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, r=0.0, alpha=None, dash=False, shape=None):
        kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if r > 0 else MSO_SHAPE.RECTANGLE)
        shp = self.slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if r > 0 and shape is None:
            shp.adjustments[0] = min(0.5, r / min(w, h))
        self._style(shp, fill, line, lw, alpha, dash)
        # preview
        box = [x * S, y * S, (x + w) * S, (y + h) * S]
        f = tup(fill, alpha if alpha is not None else 1) if fill else None
        l = tup(line) if line else None
        if shape == MSO_SHAPE.HEXAGON:
            pts = hex_pts(x, y, w, h)
            self.d.polygon(pts, fill=f, outline=l)
        elif shape == MSO_SHAPE.OVAL:
            self.d.ellipse(box, fill=f, outline=l, width=max(1, int(lw * S / 72)) if l else 0)
        elif r > 0:
            self.d.rounded_rectangle(box, radius=r * S, fill=f, outline=l, width=max(1, int(lw * S / 72)) if l else 0)
        else:
            self.d.rectangle(box, fill=f, outline=l, width=max(1, int(lw * S / 72)) if l else 0)
        if dash and line:
            pass
        return shp

    def hexa(self, x, y, w, h, fill=None, line=None, lw=0.75, alpha=None):
        return self.rect(x, y, w, h, fill, line, lw, alpha=alpha, shape=MSO_SHAPE.HEXAGON)

    def oval(self, x, y, w, h, fill=None, line=None, lw=0.75, alpha=None):
        return self.rect(x, y, w, h, fill, line, lw, alpha=alpha, shape=MSO_SHAPE.OVAL)

    def line(self, x1, y1, x2, y2, color="1D2433", w=1.0, arrow=False, dash=False):
        c = self.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color)
        c.line.width = Pt(w)
        ln = c.line._get_or_add_ln()
        if dash:
            pd = etree.SubElement(ln, qn("a:prstDash"))
            pd.set("val", "dash")
        if arrow:
            te = etree.SubElement(ln, qn("a:tailEnd"))
            te.set("type", "triangle")
        self.d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=tup(color), width=max(1, int(w * S / 72)))
        if arrow:
            ang = math.atan2(y2 - y1, x2 - x1)
            L = 0.09 * S
            p = [(x2 * S, y2 * S), (x2 * S - L * math.cos(ang - 0.4), y2 * S - L * math.sin(ang - 0.4)),
                 (x2 * S - L * math.cos(ang + 0.4), y2 * S - L * math.sin(ang + 0.4))]
            self.d.polygon(p, fill=tup(color))

    def poly(self, pts, fill=None, line=None, lw=1.0, alpha=None):
        """freeform polygon, pts in inches"""
        fb = self.slide.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
        fb.add_line_segments([(Inches(a), Inches(b)) for a, b in pts[1:]], close=True)
        shp = fb.convert_to_shape()
        self._style(shp, fill, line, lw, alpha)
        self.d.polygon([(a * S, b * S) for a, b in pts], fill=tup(fill, alpha if alpha else 1) if fill else None,
                       outline=tup(line) if line else None)

    def curve(self, pts, color="F7941D", w=2.0, dash=False):
        """polyline through many points (open path)"""
        fb = self.slide.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
        fb.add_line_segments([(Inches(a), Inches(b)) for a, b in pts[1:]], close=False)
        shp = fb.convert_to_shape()
        shp.shadow.inherit = False
        shp.fill.background()
        shp.line.color.rgb = rgb(color)
        shp.line.width = Pt(w)
        if dash:
            ln = shp.line._get_or_add_ln()
            pd = etree.SubElement(ln, qn("a:prstDash"))
            pd.set("val", "sysDash")
        self.d.line([(a * S, b * S) for a, b in pts], fill=tup(color), width=max(1, int(w * S / 72)), joint="curve")

    # ---------- images ----------
    def image(self, path, x, y, w, h, fit="cover", r=0.0, focus=(0.5, 0.5), border=None, bw=1.0):
        im = Image.open(path)
        iw, ih = im.size
        pic = None
        if fit == "cover":
            ar_box, ar_im = w / h, iw / ih
            if ar_im > ar_box:  # crop sides
                vis = ar_box / ar_im
                cl = (1 - vis) * focus[0]
                crop = (cl, 0, 1 - vis - cl, 0)
            else:
                vis = ar_im / ar_box
                ct = (1 - vis) * focus[1]
                crop = (0, ct, 0, 1 - vis - ct)
            pic = self.slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
            pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = crop
            l, t = crop[0], crop[1]
            rr, bb = 1 - crop[2], 1 - crop[3]
            sub = im.convert("RGBA").crop((int(l * iw), int(t * ih), int(rr * iw), int(bb * ih)))
        else:  # contain
            sc = min(w / iw, h / ih)
            nw, nh = iw * sc, ih * sc
            x0, y0 = x + (w - nw) / 2, y + (h - nh) / 2
            pic = self.slide.shapes.add_picture(path, Inches(x0), Inches(y0), Inches(nw), Inches(nh))
            sub = im.convert("RGBA")
            x, y, w, h = x0, y0, nw, nh
        if r > 0:
            pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
            av = pic._element.spPr.find(qn("a:prstGeom")).find(qn("a:avLst"))
            if av is None:
                av = etree.SubElement(pic._element.spPr.find(qn("a:prstGeom")), qn("a:avLst"))
            gd = etree.SubElement(av, qn("a:gd"))
            gd.set("name", "adj")
            gd.set("fmla", "val %d" % int(min(0.5, r / min(w, h)) * 100000))
        if border:
            pic.line.color.rgb = rgb(border)
            pic.line.width = Pt(bw)
        self.imgs.append((x, y, x + w, y + h, path.split('/')[-1]))
        # preview
        pw, ph = int(w * S), int(h * S)
        sub = sub.resize((max(1, pw), max(1, ph)), Image.LANCZOS)
        mask = Image.new("L", (pw, ph), 0)
        md = ImageDraw.Draw(mask)
        if r > 0:
            md.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=r * S, fill=255)
        else:
            md.rectangle([0, 0, pw, ph], fill=255)
        self.img.paste(sub.convert("RGB"), (int(x * S), int(y * S)), Image.composite(sub.split()[3], Image.new("L", (pw, ph), 0), mask))
        if border:
            if r > 0:
                self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S, outline=tup(border), width=max(1, int(bw * S / 72)))
            else:
                self.d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], outline=tup(border), width=max(1, int(bw * S / 72)))
        return pic

    # ---------- text ----------
    def text(self, x, y, w, h, paras, size=8.5, color="1D2433", head=False, bold=False, align="l", anchor="t",
             margin=(0.04, 0.02, 0.04, 0.02), gap=3, ls=1.0, fill=None, line=None, r=0.0, lw=0.75, alpha=None, name=None):
        if isinstance(paras, str):
            paras = paras.split("\n")
        if fill or line:
            self.rect(x, y, w, h, fill, line, lw, r, alpha)
        tb = self.slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(m) for m in margin]
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        bodyPr = tf._txBody.find(qn("a:bodyPr"))
        for ch in list(bodyPr):
            bodyPr.remove(ch)
        etree.SubElement(bodyPr, qn("a:noAutofit"))
        # build model
        blocks = []
        for i, p in enumerate(paras):
            if isinstance(p, str):
                p = dict(text=p)
            p = dict(p)
            t = p["text"]
            bullet = p.get("bullet", False)
            if t.startswith("• "):
                bullet, t = True, t[2:]
            psz = p.get("size", size)
            pcol = p.get("color", color)
            pbold = p.get("bold", bold)
            phead = p.get("head", head)
            phead_ = phead
            palign = p.get("align", align)
            if palign == "l" and p.get("size", size) <= 10.2 and not phead_ and not p.get("bullet", False) and not t.startswith("• "):
                palign = "j"  # ByteForce body copy is justified
            if palign == "ln":
                palign = "l"  # forced left (quotes, narrow boxes)
            pgap = p.get("gap", gap)
            runs = parse_runs(t, pcol, pbold, phead)
            blocks.append(dict(runs=runs, size=psz, bullet=bullet, align=palign, gap=pgap, head=phead))
        # shrink-to-fit (like PowerPoint's 'shrink text on overflow'): up to 12% smaller
        have0 = h - margin[1] - margin[3]
        for sc in (1.0, 0.98, 0.96, 0.94, 0.92, 0.90, 0.88):
            if self._measure(blocks, w, margin, ls, sc) <= have0 + 0.02:
                break
        if sc < 1.0:
            for b in blocks:
                b["size"] = round(b["size"] * sc, 2)
        # pptx
        first = True
        for b in blocks:
            para = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT, "j": PP_ALIGN.JUSTIFY}[b["align"]]
            para.space_after = Pt(b["gap"])
            para.line_spacing = Pt(round(pitch_pt(b["size"], ls), 2))
            pPr = para._p.get_or_add_pPr()
            if b["bullet"]:
                ind = int(b["size"] * 1.15 * 12700)
                pPr.set("marL", str(ind))
                pPr.set("indent", str(-ind))
                bc = etree.SubElement(pPr, qn("a:buClr"))
                sc = etree.SubElement(bc, qn("a:srgbClr"))
                sc.set("val", COL["o"])
                bf = etree.SubElement(pPr, qn("a:buFont"))
                bf.set("typeface", "Arial")
                bu = etree.SubElement(pPr, qn("a:buChar"))
                bu.set("char", "•")
            else:
                etree.SubElement(pPr, qn("a:buNone"))
            for (tx, rc, rb, rh) in b["runs"]:
                run = para.add_run()
                run.text = tx
                run.font.size = Pt(b["size"])
                run.font.bold = bool(rh)
                run.font.name = HEAD_FONT if rh else (EMPH_FONT if rb else BODY_FONT)
                run.font.color.rgb = rgb(rc)
        # preview + overflow
        need = self._prev_text(x, y, w, h, blocks, margin, anchor, ls)
        have = h - margin[1] - margin[3]
        if need > have + 0.02:
            WARN.append("[%s] overflow %.2f>%.2f in: %s" % (self.name, need, have, blocks[0]["runs"][0][0][:40] if blocks and blocks[0]["runs"] else ""))
        return need

    def _measure(self, blocks, w, margin, ls, sc):
        W = (w - margin[0] - margin[2]) * S
        total = 0.0
        for b in blocks:
            size = b["size"] * sc
            px = size / 72 * S
            ind = size * 1.15 / 72 * S if b["bullet"] else 0
            n = len(wrap_runs(b["runs"], px, (W - ind) * 0.985))
            total += pitch_pt(size, ls) / 72 * S * n + b["gap"] / 72 * S
        if blocks:
            total -= blocks[-1]["gap"] / 72 * S
        return total / S

    def _prev_text(self, x, y, w, h, blocks, margin, anchor, ls):
        W = (w - margin[0] - margin[2]) * S
        lines_all = []  # (segments, align, size, bullet_indent, gapbelow)
        total = 0.0
        for b in blocks:
            px = b["size"] / 72 * S
            ind = b["size"] * 1.15 / 72 * S if b["bullet"] else 0
            lines = wrap_runs(b["runs"], px, (W - ind) * 0.985)
            lh = pitch_pt(b["size"], ls) / 72 * S
            for li, ln in enumerate(lines):
                lines_all.append((ln, b["align"], px, ind if True else 0, li == 0 and b["bullet"], lh, b["head"], 0, li == len(lines) - 1))
            if lines:
                lines_all[-1] = lines_all[-1][:7] + (b["gap"] / 72 * S, True)
            for _ in range(len(lines) - 1):
                pass
            total += lh * len(lines) + b["gap"] / 72 * S
        total_in = total / S
        # last gap shouldn't count
        if blocks:
            total_in -= blocks[-1]["gap"] / 72
        if anchor == "t":
            cy = y * S + margin[1] * S
        elif anchor == "m":
            cy = y * S + (h * S - total_in * S) / 2
        else:
            cy = (y + h) * S - margin[3] * S - total_in * S
        cur = cy
        ink = [1e9, 1e9, -1e9, -1e9]
        for item in lines_all:
            ln, al, px, ind, isb, lh, hd = item[:7]
            gapb = item[7] if len(item) > 7 else 0
            islast = item[8] if len(item) > 8 else True
            wsum = sum(sw for (_, sw, *_r) in ln_widths(ln, px))
            spaces = sum(1 for (tx, *_r) in ln_widths(ln, px) for ch in tx if ch == " ")
            extra = (W - ind - wsum) / spaces if (al == "j" and not islast and spaces) else 0.0
            if al == "c":
                cx = x * S + margin[0] * S + (W - ind - wsum) / 2 + ind
            elif al == "r":
                cx = x * S + margin[0] * S + (W - ind - wsum) + ind
            else:
                cx = x * S + margin[0] * S + ind
            cx0 = cx - (ind if isb else 0)
            if isb:
                self.d.text((cx - ind, cur + lh * 0.05), "•", font=pfont("bold", px), fill=tup(COL["o"]))
            for (tx, sw, kind, col) in ln_widths(ln, px):
                if extra:
                    sw += extra * tx.count(" ")
                    fnt = pfont(kind, px)
                    xx = cx
                    for wd in re.findall(r"\S+|\s+", tx):
                        self.d.text((xx, cur + lh * 0.05), wd, font=fnt, fill=tup(col))
                        xx += fnt.getlength(wd) + (extra * wd.count(" "))
                else:
                    self.d.text((cx, cur + lh * 0.05), tx, font=pfont(kind, px), fill=tup(col))
                cx += sw
            ink[0] = min(ink[0], cx0); ink[2] = max(ink[2], cx); ink[1] = min(ink[1], cur); ink[3] = max(ink[3], cur + lh)
            cur += lh
            cur += gapb
        if lines_all and blocks and any(r[0].strip() for b in blocks for r in b['runs']):
            self.regions.append((ink[0] / S, ink[1] / S, ink[2] / S, ink[3] / S, blocks[0]['runs'][0][0][:30]))
        return total_in


def hex_pts(x, y, w, h):
    # MSO hexagon: adj 25% of min dimension offset at left/right
    a = 0.25 * min(w, h) * 1.0
    return [((x + a) * S, y * S), ((x + w - a) * S, y * S), ((x + w) * S, (y + h / 2) * S), ((x + w - a) * S, (y + h) * S),
            ((x + a) * S, (y + h) * S), (x * S, (y + h / 2) * S)]


AUTO_BOLD = ['shoot-on-the-move', 'virtual goal', 'one speed band', 'exact count', 'falling steeply', 'cascade controller', 'bang-bang', 'documentation-first', 'bulk read', 'sim-first', 'worst-case', 'held-out seeds']
TOK = re.compile(r"(\*\*.+?\*\*|\[\[\w:.+?\]\])")


def parse_runs(t, color, bold, head):
    out = []
    for part in TOK.split(t):
        if not part:
            continue
        if part.startswith("**"):
            out.append((part[2:-2], color, True, head))
        elif part.startswith("[["):
            m = re.match(r"\[\[(\w):(.+?)\]\]", part)
            out.append((m.group(2), COL[m.group(1)], True, head))
        else:
            if head or bold:
                out.append((part, color, bold, head))
            else:
                for q in re.split("(" + "|".join(re.escape(b) for b in AUTO_BOLD) + ")", part):
                    if q:
                        out.append((q, color, q in AUTO_BOLD, head))
    return out


def kind_of(bold, head):
    return "head" if head else ("bold" if bold else "body")


def ln_widths(ln, px):
    out = []
    for (tx, col, bd, hd) in ln:
        f = pfont(kind_of(bd, hd), px)
        out.append((tx, f.getlength(tx), kind_of(bd, hd), col))
    return out


def wrap_runs(runs, px, W):
    """greedy wrap on words across styled runs -> list of lines, each list of (text,color,bold,head)"""
    words = []
    for (tx, col, bd, hd) in runs:
        for i, wd in enumerate(re.findall(r"\S+|\s+", tx)):
            words.append((wd, col, bd, hd))
    lines, cur, curw = [], [], 0.0
    for (wd, col, bd, hd) in words:
        f = pfont(kind_of(bd, hd), px)
        wl = f.getlength(wd)
        if wd.isspace():
            if cur:
                cur.append((wd, col, bd, hd))
                curw += wl
            continue
        if curw + wl > W and cur:
            # strip trailing space
            while cur and cur[-1][0].isspace():
                cur.pop()
            lines.append(cur)
            cur, curw = [], 0.0
        cur.append((wd, col, bd, hd))
        curw += wl
    while cur and cur[-1][0].isspace():
        cur.pop()
    if cur:
        lines.append(cur)
    return lines or [[("", "000000", False, False)]]


def check_overlaps(deck):
    out = []
    for pg in deck.pages:
        R = pg.regions
        for i in range(len(R)):
            a = R[i]
            if a[2] > 8.5 - 0.25 or a[0] < 0.25:
                out.append("[%s] text beyond margin: %s (%.2f..%.2f)" % (pg.name, a[4], a[0], a[2]))
            for j in range(i + 1, len(R)):
                b = R[j]
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 0.03 and oy > 0.03:
                    out.append("[%s] OVERLAP '%s' x '%s' (%.2f x %.2f in) at y=%.2f" % (pg.name, a[4], b[4], ox, oy, max(a[1], b[1])))
    return out


def check_text_on_images(deck):
    out = []
    for pg in deck.pages:
        for r in pg.regions:
            for im in pg.imgs:
                if im[4].startswith('honey'): continue
                ox = min(r[2], im[2]) - max(r[0], im[0]); oy = min(r[3], im[3]) - max(r[1], im[1])
                if ox > 0.03 and oy > 0.03:
                    out.append("[%s] text '%s' over image %s (%.2f x %.2f)" % (pg.name, r[4], im[4], ox, oy))
    return out


BOLD_PHRASES = ["shoot-on-the-move", "shoot on the move", "virtual goal", "one speed band", "exact count", "documentation-first", "every week", "every month", "every season",
                "falling steeply", "cascade controller", "feedforward", "bang-bang", "open-source", "hands-on", "sim-first", "held-out seeds", "worst-case", "single point of failure",
                "bulk read", "bulk-read", "knowledge transfer", "community", "mentor"]
