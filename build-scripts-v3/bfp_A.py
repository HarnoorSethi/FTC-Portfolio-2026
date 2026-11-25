from bfkit import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import os

BLUE = "2C6E9E"
LBLUE = "E8F7FB"
A2 = '/tmp/work/assets2/'

TILES = [("B", "ev_green.png", (0.5, 0.5)), ("I", "ev_train.png", (0.5, 0.5)), ("O", "ev_open.png", (0.5, 0.5)),
         ("B", "ev_demo.png", (0.5, 0.5)), ("U", "ev_tent.png", (0.5, 0.5)), ("Z", "ev_kids.png", (0.5, 0.5)),
         ("Z", "ev_lib.png", (0.5, 0.5)), ("2", "ev_taiwan.png", (0.5, 0.5)), ("7", "cover_hero.png", (0.5, 0.5))]
COLX = [48, 342, 645]; COLW = [277, 287, 288]
ROWY = [405, 878, 1350]; ROWH = [438, 439, 440]


def make_tile(idx):
    ch, src, foc = TILES[idx]
    c, r = idx % 3, idx // 3
    w, h = int(COLW[c] * 2 * FX / FY), ROWH[r] * 2   # tile pixels match the slide box shape, so "cover" never crops the letter
    im = Image.open(A + src).convert("RGB")
    if src == "cover_hero.png":
        bg = Image.new("RGB", im.size, (30, 80, 140)); im = bg
        rr = Image.open(A + "cover_hero.png").convert("RGB"); im = rr
    iw, ih = im.size
    sc = max(w / iw, h / ih)
    im = im.resize((int(iw * sc) + 1, int(ih * sc) + 1), Image.LANCZOS)
    l = int((im.width - w) * foc[0]); t = int((im.height - h) * foc[1])
    im = im.crop((l, t, l + w, t + h))
    ov = Image.new("RGB", (w, h), (44, 110, 158))
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=90, threshold=2))  # sources are small: sharpen the upscale
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.12)).enhance(1.06)
    im = Image.blend(im, ov, 0.06)
    # stencil: photo visible only inside the heavy letter, white elsewhere
    fnt = ImageFont.truetype("/Users/sumeetsethi/FTC-Portfolio-2026/fonts-needed/Montserrat-VF.ttf", 900)
    fnt.set_variation_by_name(b"Black")
    gm = Image.new("L", (1400, 1400), 0)
    ImageDraw.Draw(gm).text((100, 100), ch, font=fnt, fill=255)
    gm = gm.crop(gm.getbbox())
    if ch == "I":  # a capital I with serifs: top bar, bottom bar and the stem between them
        gm = Image.new("L", (w - 4, h - 4), 0)
        gd = ImageDraw.Draw(gm)
        W_, H_ = gm.size
        bar, stem = int(H_ * 0.15), int(W_ * 0.38)
        q = 22  # inset so the outline can wrap the whole letter
        gd.rectangle([q, q, W_ - q, q + bar], fill=255)
        gd.rectangle([q, H_ - q - bar, W_ - q, H_ - q], fill=255)
        gd.rectangle([(W_ - stem) // 2, q, (W_ + stem) // 2, H_ - q], fill=255)
    else:  # a little padding so round bottoms (U, O, B) are not flattened by the tile edge
        pad = 22
        gm = gm.resize((w - 4 - 2 * pad, h - 4 - 2 * pad), Image.LANCZOS)
        tmp = Image.new("L", (w - 4, h - 4), 0); tmp.paste(gm, (pad, pad)); gm = tmp
    gm = gm.filter(ImageFilter.GaussianBlur(9)).point(lambda v: 255 if v > 128 else 0)
    gm = gm.filter(ImageFilter.GaussianBlur(1.2))
    mask = Image.new("L", (w, h), 0); mask.paste(gm, (2, 2))
    white = Image.new("RGB", (w, h), (255, 255, 255))
    out = Image.composite(im, white, mask).convert("RGBA")
    # thin cover-blue outline so photo areas that are white (tent canopy, sky) do not dissolve into the page
    ring = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(7)), mask.filter(ImageFilter.MinFilter(3)))
    out = Image.composite(Image.new("RGBA", (w, h), (44, 110, 158, 255)), out, ring.point(lambda v: 255 if v > 40 else 0)).convert("RGBA")
    out.putalpha(Image.new("L", (w, h), 255))
    path = A2 + "cover_tile_%d.png" % idx
    out.save(path)
    return path


def page_01(D):
    p = D.page(name='p01')
    k = K(p)
    k.rect(0, 0, SW, 162, fill=BLUE)
    # left: FIRST TECH CHALLENGE
    k.text(145, 30, 200, 110, [dict(text="FIRST®", head=True, size=11, color="FFFFFF"), dict(text="TECH", head=True, size=11, color="FFFFFF"),
                                dict(text="CHALLENGE", head=True, size=11, color="FFFFFF")], gap=0, ls=0.85, anchor="m")
    k.rect(34, 50, 100, 62, fill=None, line="FFFFFF", lw=1.5, r=20)
    k.line(346, 32, 346, 126, color="FFFFFF", w=1.5)
    k.text(376, 28, 200, 30, "S E A S O N", pt=5.5, color="FFFFFF", bold=True, align="c")
    k.text(376, 55, 200, 60, "BIOBUZZ", pt=16, color="FFFFFF", head=True, align="c", anchor="m")
    k.text(376, 108, 200, 24, "presented by RTX", pt=6, color="FFFFFF", align="c")
    k.oval(648, 15, 128, 128, fill="FFFFFF")
    k.image(LOGO, 656, 45, 112, 70, fit="contain")
    k.text(868, 30, 170, 24, "O R G A N I Z A T O R", pt=5.5, color="FFFFFF", bold=True, align="c")
    k.text(868, 55, 170, 60, "FIRST", pt=18, color="FFFFFF", head=True, align="c", anchor="m")
    k.line(1057, 32, 1057, 126, color="FFFFFF", w=1.5)
    k.text(1090, 30, 190, 24, "P A R T N E R", pt=5.5, color="FFFFFF", bold=True, align="c")
    k.text(1090, 55, 190, 60, "RTX", pt=18, color="FFFFFF", head=True, align="c", anchor="m")
    k.text(1090, 108, 190, 24, "Partner placeholder", pt=5.5, color="FFFFFF", align="c")
    # titles
    k.text(44, 160, 1230, 150, "Engineering Portfolio", pt=49, color=BLUE, head=True, anchor="m")
    k.text(44, 290, 960, 110, "Cheesy Chips #23222", pt=37, color=BLUE, head=True, anchor="m")
    k.text(1005, 290, 220, 104, [dict(text="BIOBUZZ", bold=True, size=19 * FONT, color=BLUE), dict(text="2026-27", bold=True, size=19 * FONT, color=BLUE)],
           gap=0, ls=0.85, align="c", anchor="m")
    for i in range(9):
        c, r = i % 3, i // 3
        k.image(make_tile(i), COLX[c], ROWY[r], COLW[c], ROWH[r], fit="cover")
    k.image(LOGO, SW / 2 - 60, 1796, 120, 56, fit="contain")
    # content panel
    k.rect(963, 405, 307, 1385, fill=BLUE)
    k.text(979, 410, 280, 80, "Content", pt=24, color=LBLUE, head=True, anchor="m")
    rows = [("1 Think", "p.2", 1), ("1.1 Our team", "p.2", 0), ("1.2 Our journey", "p.2", 0), ("1.3 Summary", "p.2", 0), ("1.4 Objectives", "p.2", 0),
            ("1.5 Sustainability plan", "p.3", 0), ("1.6 SWOT analysis", "p.3", 0),
            ("2 Connect & Motivate", "p.4", 1), ("2.1 Business", "p.4", 0), ("2.2 Sponsors", "p.4", 0), ("2.3 Outreach hub", "p.5", 0),
            ("2.4 Events", "p.6-7", 0), ("2.5 Mentoring", "p.8", 0), ("2.6 Social media", "p.9", 0),
            ("3 Think", "p.10", 1), ("3.1 Design process", "p.10", 0), ("3.2 Chassis", "p.11", 0), ("3.3 Intake", "p.12", 0),
            ("4 Innovate", "p.13", 1), ("4.1 Shooter & hood", "p.13", 0), ("4.2 Turret", "p.14", 0),
            ("5 Think & Design", "p.15", 1), ("5.1 Game strategy", "p.15", 0),
            ("6 Control", "p.16", 1), ("6.1 Software", "p.16", 0), ("6.2 Simulation", "p.16", 0)]
    y = 500
    for lab, pg, b in rows:
        if b and y > 520: y += 14
        k.text(975, y, 250, 34, lab, pt=9.6, color=LBLUE, head=bool(b), anchor="m")
        k.text(1150, y, 105, 34, pg, pt=9.6, color=LBLUE, head=bool(b), align="r", anchor="m")
        y += 43


# ---------------------------------------------------------------- shared helpers
INK = "1D1D1B"
PANEL = "C9EDFB"
QBLUE = "007199"
GREYN = "939191"
ROLE = dict(Software="4AB2E5", Design="E9D909", Manufacturing="0A9A4B", Outreach="7155A5", Media="EC192D", Captain="F26A3D")


def dashed(k, x1, x2, y, color=INK, w=0.8):
    k.line(x1, y, x2, y, color=color, w=w, dash=True)


def quote(k, x, y, lines_h, text, w, color=QBLUE, pt=8.2):
    k.text(x - 4, y - 20, 62, 120, "“", pt=40, color=color, bold=True, head=True, align="c", anchor="t", margin=(0, 0, 0, 0))
    k.rect(x + 64, y, 2, lines_h, fill=color)
    k.text(x + 79, y - 14, w, lines_h + 30, text, pt=pt, color=color, anchor="m", ls=1.0)


def circ_legend(k, cx, y, items, pt=7):
    """items: list of rows; each row list of (label,color); centred on cx"""
    for ri, row in enumerate(items):
        wid = [20 + 9 * len(l) * 0.8 + 14 for l, c in row]
        tot = sum(wid)
        x = cx - tot / 2
        for (l, c), ww in zip(row, wid):
            k.oval(x, y + ri * 19 - 7, 14, 14, line=c, lw=1.6)
            k.text(x + 19, y + ri * 19 - 11, ww, 22, l, pt=pt, color="3A3F4A", anchor="m")
            x += ww


def num_item(k, x, y, w, n, title, body, bh):
    k.text(x, y - 14, 40, 70, str(n), pt=24, color=GREYN, anchor="t")
    k.text(x + 34, y + 2, w, 44, title, pt=12, color=GREYN, anchor="m")
    k.text(x, y + 48, w, bh, body, pt=8.2, color=INK)


def page_02(D):
    p = D.page(name='p02')
    k = K(p)
    k.header(2, [("inspire", "3BB0E8", "000000"), ("think", "EEE000", "000000")])
    k.rect(0, 100, 537, 1652, fill=PANEL)
    k.text(40, 130, 300, 64, "We are", pt=16, color=INK, anchor="m")
    k.text(40, 190, 230, 100, "Cheesy", pt=29, color="3FA9DE", bold=True, anchor="m")
    k.text(286, 190, 230, 100, "Chips!", pt=29, color="1F1E1D", bold=True, anchor="m")
    dashed(k, 25, 524, 312)
    studs = [("harnoor", "Harnoor", "Software"), ("johnson", "Johnson", "Design"), ("shaurya", "Shaurya", "Captain"), ("noah", "Noah", "Manufacturing"),
             ("matvei", "Matvei", "Design"), ("michael", "Michael", "Outreach"), ("dylan", "Dylan", "Media"), ("morgan", "Morgan", "Design"),
             ("kevin", "Kevin", "Design"), ("jake", "Jake", "Design"), ("rishaan", "Rishaan", "Manufacturing")]
    cxs = [88, 212, 337, 462]
    cys = [430, 590, 750]
    for i in range(12):
        cx, cy = cxs[i % 4], cys[i // 4]
        if i < 11:
            f, nm, role = studs[i]
            c = ROLE[role]
            k.circle_photo(A + 'p_%s.png' % f, cx, cy, 104, ring=c, bw=3.4)
            k.dot(cx + 24, cy + 40, 13, ROLE["Software"] if role != "Software" else ROLE["Design"])
            k.text(cx - 60, cy + 54, 120, 24, nm, pt=7.5, color=INK, align="c", anchor="m")
        else:
            k.oval(cx - 52, cy - 52, 104, 104, fill="FFFFFF", line="4AB2E5", lw=2.2)
            k.image(LOGO, cx - 42, cy - 26, 84, 52, fit="contain")
            k.text(cx - 60, cy + 54, 120, 24, "You?", pt=7.5, color=INK, align="c", anchor="m")
    circ_legend(k, 268, 895, [[("Software", ROLE["Software"]), ("Design", ROLE["Design"]), ("Manufacturing", ROLE["Manufacturing"])],
                              [("Outreach", ROLE["Outreach"]), ("Media", ROLE["Media"]), ("Captain", ROLE["Captain"])]])
    # mentors
    ment = [("salgaonkar", "Mr. Salgaonkar", "7155A5", 'png'), ("lindemann", "Mr. Lindemann", "7155A5", 'png'),
            ("lawrence", "Andrew Lawrence", "E9D909", 'jpeg'), ("torrance", "Andrew Torrance", "EC192D", 'png')]
    mc = [(150, 1110), (385, 1110), (150, 1340), (385, 1340)]
    for (f, nm, c, ext), (cx, cy) in zip(ment, mc):
        k.circle_photo(A + 'p_%s.%s' % (f, ext), cx, cy, 140, ring=c, bw=3.4)
        k.text(cx - 100, cy + 76, 200, 24, nm, pt=7.5, color=INK, align="c", anchor="m")
    circ_legend(k, 268, 1545, [[("Teacher", "7155A5"), ("Program mentor", "E9D909")], [("Alumni", "EC192D"), ("Technical mentor", "4AB2E5")]])
    # --- right side
    k.text(560, 125, 735, 64, "Our Journey", pt=15.5, color=INK, align="c", anchor="m")
    quote(k, 550, 242, 62, "“Team spirit and passion are contagious: only by working together can we reach new heights.” - our motto", 282, pt=8.2)
    dashed(k, 549, 904, 336)
    k.text(549, 350, 356, 170, ["Our team started three years ago. We branched off from our FRC program, FRC team 254, Bellarmine's Cheesy Poofs. "
                               "Since then we have walked this journey on our **own**. " + dummy(12)], pt=8.2, color=INK)
    k.text(549, 560, 356, 170, ["Every year new members join and veterans move on. Along the way we went to the **World Championship** after being finalists in the Silicon division. " + dummy(18)], pt=8.2, color=INK)
    k.text(930, 213, 340, 560, [dict(text="We mentor teams outside our school. We help a middle school team every week, Code Crackers at St. Clare MS and a Graham MS FLL team. " + dummy(20), gap=14),
                                dict(text="We also help our rookie teams, **23229 Cheesy Strings** and **23230 Cheesy Wheels**. " + dummy(26), gap=14),
                                dict(text=dummy(20))], pt=8.2, color=INK)
    k.text(549, 730, 400, 56, "Summary", pt=15.5, color=INK, anchor="m")
    k.text(549, 788, 356, 310, [dict(text=dummy(50), gap=16), dict(text=dummy(18))], pt=8.2, color=INK)
    k.text(930, 762, 340, 40, "Pre-season", pt=11.5, color=INK, align="r", anchor="m")
    for i, (a, b) in enumerate([("Pre-season event", "Result ---"), ("Pre-season event", "Result ---"), ("Pre-season event", "Result ---")]):
        k.text(930, 805 + i * 56, 250, 52, [dict(text=a), dict(text=b, bold=True)], pt=8.2, color=INK, gap=0)
    k.rect(1183, 808, 102, 167, fill="231F20", r=14)
    for j in range(3):
        k.text(1190, 820 + j * 52, 88, 46, "LOGO", pt=8, color="FFFFFF", bold=True, align="c", anchor="m")
    k.text(930, 978, 340, 44, "Past results", pt=11.5, color=INK, align="r", anchor="m")
    for i, (a, b) in enumerate([("Silicon division", "Finalist Alliance"), ("FIRST World Championship", "Team qualified")]):
        k.text(930, 1022 + i * 56, 250, 52, [dict(text=a), dict(text=b, bold=True)], pt=8.2, color=INK, gap=0)
    k.rect(1183, 1020, 102, 113, fill="231F20", r=14)
    k.text(1190, 1032, 88, 40, "LOGO", pt=8, color="FFFFFF", bold=True, align="c", anchor="m")
    k.text(1190, 1080, 88, 40, "LOGO", pt=7, color="F7C948", bold=True, align="c", anchor="m")
    # work in progress pill
    dashed(k, 549, 678, 1195); dashed(k, 1158, 1285, 1195)
    k.rect(766, 1172, 302, 52, fill="FFFFFF", line="000000", lw=0.8, r=26)
    k.text(776, 1174, 282, 48, "As a work in progress, our future is still unwritten.", pt=7, color=INK, align="c", anchor="m")
    for sx, d in ((693, 1), (1138, -1)):
        k.oval(sx - 8, 1177, 16, 16, fill="FFFFFF", line="000000", lw=1.6)
        k.poly([(sx + d * 12, 1196), (sx + d * 40, 1200), (sx + d * 52, 1210), (sx + d * 30, 1218), (sx + d * 10, 1208)], fill="231F20")
    k.text(549, 1235, 755, 70, "Objectives", pt=15.5, color=INK, align="c", anchor="m")
    num_item(k, 549, 1300, 357, 1, "Victory on the field", "Build a reliable robot with strong technical performance for the BIOBUZZ season. " + dummy(6), 100)
    num_item(k, 549, 1470, 357, 2, "Community growth", "Support the growth of robotics teams in our region. " + dummy(8), 100)
    num_item(k, 930, 1395, 340, 3, "Family expansion", "Bring more students into FTC and robotics. " + dummy(12), 100)
    # growth chart
    tops = [1695, 1679, 1692, 1671, 1640, 1625, 1580]
    cols = ["4AB2E5"] * 4 + ["2C6E9E", "3C3A3F", "3C3A3F"]
    for i, (t, c) in enumerate(zip(tops, cols)):
        x = 549 + i * 110.8
        k.rect(x, t, 36, 1752 - t, fill=c)
    import math
    pts = []
    for i in range(30):
        u = i / 29
        xx = 540 + u * 530
        yy = 1672 - 100 * u ** 2.6
        pts.append((xx, yy))
    pts[-1] = (1070, 1581)
    k.curve(pts, color="1D1D1B", w=0.9)
    k.oval(1063, 1574, 14, 14, fill="FFFFFF", line="1D1D1B", lw=1)
    # mascot
    k.oval(975, 1590, 62, 70, fill="4AB2E5")
    k.oval(1000, 1603, 22, 22, fill="231F20")
    k.oval(1006, 1608, 8, 8, fill="FFFFFF")
    k.oval(990, 1650, 30, 24, fill="3C3A3F")
    k.oval(1022, 1652, 24, 22, fill="3C3A3F")
    k.line(940, 1610, 1050, 1640, color="3C3A3F", w=2)
    k.poly([(960, 1650), (1000, 1640), (1040, 1650), (1020, 1668), (985, 1672)], fill="FFD100")


def sec(k, x, y, w, title, body, bh, pt=8.2, hy=36):
    k.text(x, y, w, hy, title, pt=11, color=INK, anchor="m")
    k.text(x, y + hy + 2, w, bh, body, pt=pt, color=INK)


def page_03(D):
    p = D.page(name='p03')
    k = K(p)
    k.header(3, [("inspire", "3BB0E8", "000000"), ("think", "EEE000", "000000")])
    k.rect(774, 100, 536, 1652, fill=PANEL)
    k.text(38, 120, 710, 70, "Sustainability plan", pt=15.5, color=INK, align="c", anchor="m")
    X1, X2, W = 40, 405, 340
    # col 1
    quote(k, 42, 224, 56, "“Quote placeholder about our team.” - name", 260)
    dashed(k, 40, 380, 288)
    k.text(X1, 303, W, 140, "The longevity of the club is one of the **most important** parts of our plan. Knowledge has to be passed on **from one generation to the next**. " + dummy(8), pt=8.2, color=INK)
    sec(k, X1, 455, W, "Cheesy Chips Organization", dummy(28), 150)
    sec(k, X1, 645, W, "Rookie team pipeline", "Our rookie teams are **23229 Cheesy Strings** and **23230 Cheesy Wheels**. Students join open builds, then apply. In year one they run their own team. After that they join the veteran team and later lead or mentor. " + dummy(6), 160)
    sec(k, X1, 873, W, "Mentoring external teams", "We mentor a middle school team at CHA every week. We also help **Code Crackers** at St. Clare MS and a **Graham MS** FLL team. " + dummy(2), 108)
    sec(k, X1, 1035, W, "3-step Mentoring", "**Step 1** open builds. **Step 2** our own rookie team in year one. **Step 3** the veteran team, then lead or mentor. " + dummy(8), 120)
    # col 2
    k.text(X2, 213, W, 170, dummy(30), pt=8.2, color=INK)
    sec(k, X2, 388, W, "Partners", "**SendCutSend** and **Fabworks** give us discounts on laser cut and fabricated parts. **3Dconnexion** is sending SpaceMouse CAD mice for our designers, **OnlineMetals** offers a metal coupon, and **Apple** and **Costco** support our season.", 190)
    sec(k, X2, 612, W, "Alumni", dummy(42), 230)
    quote(k, 405, 904, 56, "“Quote placeholder from an alumnus.” - name, alumnus", 250)
    dashed(k, 405, 760, 980)
    k.text(X2, 990, W, 40, "Cheesy Chips Ceremony", pt=11, color=INK, anchor="m")
    quote(k, 405, 1056, 56, "“Quote placeholder from a parent.” - parent", 250)
    dashed(k, 405, 760, 1130)
    k.text(X2, 1140, W, 90, "We filled the room with **mentors, supporters, and sponsors** to thank them. " + dummy(6), pt=8.2, color=INK)
    # SWOT
    k.text(38, 1235, 700, 70, "SWOT Analysis", pt=15.5, color=INK, align="c", anchor="m")
    sw = [(X1, 1305, "S", "trengths", 36), (X2, 1305, "W", "eaknesses", 52), (X1, 1486, "O", "pportunities", 44), (X2, 1486, "T", "hreats", 34)]
    texts = ["The team has **strong mentors** and an active alumni network. " + dummy(9), "We are a **small team**. " + dummy(18),
             "More **community** interest in FTC. " + dummy(16), "Limited **time** and funding. " + dummy(12)]
    for (x, y, big, rest, bw), t in zip(sw, texts):
        k.text(x, y - 20, 70, 90, big, pt=24, color="5A5A5A", anchor="b")
        k.text(x + bw, y + 18, 280, 52, rest, pt=12.5, color="5A5A5A", anchor="b")
        k.text(x, y + 74, W, 140, t, pt=8.2, color=INK)
    # photos
    caps = ["Overhead view of a robot match with referees", "Students building at a table with robot parts", "Small robot field in a library with kids watching", "Outdoor booth with a robot on the ground", "Two students at a computer in the lab"]
    focs = [(0.5, 0.5), (0.5, 0.3), (0.5, 0.5), (0.5, 0.6), (0.5, 0.3)]
    imgs = ["ev_camp.png", "ev_open.png", "ev_lib.png", "ev_tent.png", "ev_train.png"]
    for i in range(5):
        y = 232 + i * 245.5
        k.image(A + imgs[i], 840, y, 404, 216, fit="cover", r=16, focus=focs[i])
        k.text(840, y + 217, 404, 24, caps[i], pt=6.8, color=INK, align="c", anchor="m")
    k.photo_ph(1045, 1485, 190, 255, "book / mascot illustration", r=10)
