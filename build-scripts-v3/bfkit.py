"""ByteForce-replica kit. All coordinates are in SOURCE PIXELS of the 2.2x render of the ByteForce PDF
(1310 x 1853 px = the A4 page). Font sizes are in the ByteForce PDF's own points (A4, 595 pt wide).
Our slide is 8.5 x 11 in, so x scales by 8.5/1310 and y by 11/1853."""
import sys, os
sys.path.insert(0, '/tmp/work/build')
from pf import *
import pf
SW, SH = 1310.0, 1853.0
FX, FY = 8.5 / SW, 11.0 / SH
FONT = 1.0
A = '/tmp/work/assets/'
LOGO = "/Users/sumeetsethi/FTC-Portfolio-2026/images/team-logo-23222.png"
R = '/tmp/work/hive/renders/'
BFDIR = '/tmp/work/bf2/'      # bf01.png .. bf16.png : the reference pages (1310x1853)
TEAM = "Cheesy Chips"
NUM = "23222"
SEASON = "BIOBUZZ 2026-2027"

LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
         "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
         "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
         "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ")


def dummy(n_words):
    w = (LOREM * 20).split()
    return " ".join(w[:n_words]).rstrip(",.;") + "."


class K:
    """wrapper around a pf.Page that speaks source pixels"""

    def __init__(self, page):
        self.p = page

    # geometry helpers
    @staticmethod
    def X(v): return v * FX
    @staticmethod
    def Y(v): return v * FY

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, r=0, alpha=None, dash=False):
        rr = r * FX
        return self.p.rect(x * FX, y * FY, w * FX, h * FY, fill=fill, line=line, lw=lw, r=rr, alpha=alpha, dash=dash)

    def oval(self, x, y, w, h, fill=None, line=None, lw=0.75):
        if abs(w - h) < 1e-6:  # a true circle: FX != FY would squash it into an ellipse, so use one diameter
            d = w * FY
            return self.p.oval((x + w / 2) * FX - d / 2, (y + h / 2) * FY - d / 2, d, d, fill=fill, line=line, lw=lw)
        return self.p.oval(x * FX, y * FY, w * FX, h * FY, fill=fill, line=line, lw=lw)

    def line(self, x1, y1, x2, y2, color="000000", w=1.0, arrow=False, dash=False):
        self.p.line(x1 * FX, y1 * FY, x2 * FX, y2 * FY, color=color, w=w, arrow=arrow, dash=dash)

    def poly(self, pts, fill=None, line=None, lw=1.0, alpha=None):
        self.p.poly([(a * FX, b * FY) for a, b in pts], fill=fill, line=line, lw=lw, alpha=alpha)

    def curve(self, pts, color="000000", w=2.0, dash=False):
        self.p.curve([(a * FX, b * FY) for a, b in pts], color=color, w=w, dash=dash)

    def text(self, x, y, w, h, paras, pt=8, color="000000", bold=False, head=False, align="l", anchor="t",
             margin=(0, 0, 0, 0), gap=2, ls=1.0, fill=None, line=None, r=0, lw=0.75, alpha=None):
        """pt = the font size in the original ByteForce PDF (points). margin in source px (l,t,r,b).
        Inline **bold** works. head=True -> bold display style."""
        m = tuple(v * FX for v in margin)
        return self.p.text(x * FX, y * FY, w * FX, h * FY, paras, size=pt * FONT, color=color, head=head, bold=bold,
                           align=align, anchor=anchor, margin=m, gap=gap, ls=ls, fill=fill, line=line, r=r * FX, lw=lw, alpha=alpha)

    def image(self, path, x, y, w, h, fit="cover", r=0, focus=(0.5, 0.5), border=None, bw=1.0):
        return self.p.image(path, x * FX, y * FY, w * FX, h * FY, fit=fit, r=r * FX, focus=focus, border=border, bw=bw)

    def circle_photo(self, path, cx, cy, d, ring=None, bw=2.0, focus=(0.5, 0.35)):
        """round headshot with coloured ring, centre cx,cy diameter d"""
        dd = d * FY  # inches; one diameter for both axes so it stays a circle
        return self.p.image(path, cx * FX - dd / 2, cy * FY - dd / 2, dd, dd, fit="cover", r=dd / 2, focus=focus, border=ring, bw=bw)

    def dot(self, cx, cy, d, color):
        self.oval(cx - d / 2, cy - d / 2, d, d, fill=color)

    def photo_ph(self, x, y, w, h, label="PHOTO", r=14):
        """placeholder for a photo we do not have yet (looks like a soft grey tile, orange dashed edge)"""
        self.rect(x, y, w, h, fill="E6ECF2", line="F7941D", lw=1.0, r=r, dash=True)
        self.text(x, y, w, h, [dict(text="ADD PHOTO", head=True, size=7 * FONT, color="F7941D"), dict(text=label, size=6 * FONT, color="5E6B7D", bold=False)],
                  align="c", anchor="m", gap=1)

    # standard page furniture ------------------------------------------------
    def header(self, n, chips, side=None):
        """ByteForce top strip. chips = [(label, fillhex, textcolorhex)]. Even pages: round logo left, FIRST text logos right.
        Odd pages: text logos left, round logo + team text right. Also draws the bottom rule + page-number blob."""
        s = 1.4396
        even = (n % 2 == 0) if side is None else (side == "even")
        if even:
            self.image(LOGO, 16, 16, 114, 71, fit="contain")
            self.text(140, 15 * s, 190 * s, 22 * s, "%s **%s**" % (TEAM, NUM), pt=11, color="1D2433", anchor="m")
            self.text(140, 37 * s, 190 * s, 20 * s, SEASON, pt=9.5, color="3A3F4A", anchor="m")
            lx0, lx1 = 700 * s, 1230
            self.text(940, 30, 320, 36, [dict(text="FIRST® TECH CHALLENGE", head=True, size=7 * FONT, color="1D2433"), dict(text="BIOBUZZ presented by RTX", size=6.5 * FONT, color="3A3F4A")], anchor="m", gap=0, align="r")
            rx = 950
        else:
            self.text(25 * s, 14 * s, 300, 44 * s, [dict(text="FIRST® TECH CHALLENGE", head=True, size=7 * FONT, color="1D2433"), dict(text="BIOBUZZ presented by RTX", size=6.5 * FONT, color="3A3F4A")], anchor="m", gap=0)
            self.image(LOGO, 1178, 16, 114, 71, fit="contain")
            self.text(900, 21, 260, 30, "%s **%s**" % (TEAM, NUM), pt=11, color="1D2433", anchor="m", align="r")
            self.text(900, 52, 260, 28, SEASON, pt=9.5, color="3A3F4A", anchor="m", align="r")
            rx = 905
        x = 386
        for lab, fill, tc in chips:
            w = 74 + 11.5 * len(lab)
            self.rect(x, 32, w, 37, fill=fill, line="000000", lw=1.25, r=18.5)
            self.text(x, 32, w, 37, lab, pt=10.5, color=tc, bold=True, align="c", anchor="m")
            x += w + 14
        if x + 20 < rx:
            self.line(x, 50, rx, 50, color="000000", w=1.5)
        self.line(0, 98, SW, 98, color="000000", w=1.0)
        self.line(0, 1752, SW, 1752, color="000000", w=1.0)
        self.image(LOGO, SW / 2 - 66, 1762, 132, 78, fit="contain")  # team logo, centred in the footer band
        cx = 52 if even else SW - 52
        self.oval(cx - 27, 1785 - 27, 54, 54, fill="000000")
        self.text(cx - 27, 1785 - 27, 54, 54, str(n), pt=9, color="FFFFFF", head=True, align="c", anchor="m")

    def footer(self, n):
        pass


def _blob(k, n, side):
    # black blob with page number bottom-left (even) or bottom-right (odd) as in the reference
    cx = 55 if side == "l" else SW - 55
    k.oval(cx - 26, SH - 52 - 26, 52, 52, fill="000000")
    k.text(cx - 26, SH - 52 - 26, 52, 52, str(n), pt=9, color="FFFFFF", bold=True, head=True, align="c", anchor="m")
