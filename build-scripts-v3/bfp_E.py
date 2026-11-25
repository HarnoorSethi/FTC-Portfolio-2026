from bfkit import *
import math, os
from PIL import Image, ImageDraw, ImageFont
from ballistics import solve, h0 as H0, ht as HT, g as GRAV

INKT = "231F20"
BLU = "4889C7"
BODY = 8.0
TMP = '/tmp/work/build/_bfE_'
CADD = '/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/'


def crop_png(path, name):
    out = TMP + name + '.png'
    im = Image.open(path).convert('RGBA')
    bb = im.split()[3].getbbox()
    im.crop(bb).save(out)
    return out


def vtext(txt, name, pt_px, color, w, h, bold=False):
    """rotated (90 deg ccw) text as a transparent png"""
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", pt_px)
    im = Image.new("RGBA", (h * 2, w * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tw = d.textlength(txt, font=f)
    d.text(((h * 2 - tw) / 2, (w * 2 - pt_px) / 2), txt, font=f, fill="#" + color)
    im = im.rotate(90, expand=True)
    out = TMP + name + '.png'
    im.save(out)
    return out


def body(k, x, y, w, h, paras, pt=BODY, color=INKT, align="l", gap=4):
    return k.text(x, y, w, h, paras, pt=pt, color=color, gap=gap, align=align)


def sec(k, x, y, w, t, pt=15.5, color=INKT, h=46):
    k.text(x, y, w, h, t, pt=pt, color=color, gap=0)


def badge(k, cx, cy, d, label, ring):
    k.oval(cx - d / 2, cy - d / 2, d, d, fill="FFFFFF", line=ring, lw=1.6)
    k.oval(cx - 7, cy - d / 2 + 9, 14, 14, fill=None, line=ring, lw=1.2)
    k.text(cx - d / 2, cy - 4, d, 20, label.split("|")[0], pt=min(5.2, 5.2 * d / 80.0, 4.6 if len(label.split("|")[0]) > 8 else 9), color=INKT, bold=True, align="c", anchor="m")
    k.text(cx - d / 2, cy + 11, d, 14, label.split("|")[1], pt=4.4, color=INKT, align="c", anchor="m")


def iter_card(k, x, y, num, title, h=278):
    k.rect(x, y, 296, h, fill="FFFFFF", line=BLU, lw=2.4, r=18)
    k.rect(x, y, 296, 90, fill=BLU, r=18)
    k.text(x + 16, y + 10, 60, 74, str(num), pt=28, color="FFFFFF", anchor="m")
    k.text(x + 70, y + 8, 218, 76, title, pt=12.5, color="FFFFFF", align="r", anchor="m", gap=0)


def fillrender(name, bg):
    pass


# ======================================================================= PAGE 13
def page_13(D):
    p = D.page(name='p13'); k = K(p)
    k.header(13, [("inspire", "38BCEE", INKT), ("think", "E9D909", INKT), ("innovate", "00A857", INKT)])
    # title
    k.text(25, 100, 380, 110, "Shooter", pt=37, color=INKT, head=True, anchor="m")
    badge(k, 442, 152, 80, "Innovative|Design", "00A857")
    # objectives
    sec(k, 32, 226, 290, "Objectives", pt=16)
    objs = [(262, "1", "Hit the opening",
             "The up CELL opening is **20 in** wide, 53-60 in high. We shoot into it from 24 to 96 in away."),
            (386, "2", "One speed band",
             "The flywheel should hold **one speed band**. The hood changes the distance."),
            (510, "3", "Recover fast",
             "After each ball the wheel loses speed. It has to **recover between balls** so the next shot is the same.")]
    for y, n, t, tx in objs:
        k.text(36, y, 40, 60, n, pt=25, color=INKT, anchor="t")
        k.text(63, y + 4, 260, 34, t, pt=12.5, color=INKT, anchor="m")
        body(k, 25, y + 52, 297, 66, tx, align="l")
    sec(k, 32, 636, 290, "Iterations", pt=16)
    CAD = '/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/'
    its = [("1", "/tmp/work/assets/shooter_v1.png", "Shooter v1 prototype", "cover",
            "A quick **prototype** with one flywheel. We needed a **tighter speed band**."),
           ("2", "/tmp/work/assets/shooter_v2.png", "Shooter v2 prototype", "cover",
            "The second prototype put a **4 in flywheel** in a rigid frame."),
           ("3", CAD + "shooter_v3_old_cad.png", "Shooter v3 (CAD): the POLLEN shooter", "contain",
            "The first POLLEN shooter on the robot. One flywheel and **no counter rollers**."),
           ("4", CAD + "shooter_v4_current_cad.png", "Shooter v4 (CAD): the current shooter", "contain",
            "The current shooter adds **counter rollers**, on plates that pivot with the hood.")]
    for i, (n, img, cp, fit, tx) in enumerate(its):
        y0 = 690 + i * 264
        k.rect(25, y0, 296, 258, fill="FFFFFF", line=BLU, lw=2.4, r=18)
        k.rect(25, y0, 296, 56, fill=BLU, r=18)
        k.rect(25, y0 + 30, 296, 26, fill=BLU)
        k.text(41, y0 + 0, 50, 56, n, pt=24, color="FFFFFF", anchor="m")
        k.text(95, y0 + 4, 218, 48, "Shooter v" + n, pt=12.5, color="FFFFFF", align="r", anchor="m", gap=0)
        if fit == "cover":
            k.image(img, 45, y0 + 64, 236, 92, fit="cover", r=12)
        else:
            k.image(img, 45, y0 + 64, 236, 92, fit="contain")
        k.text(25, y0 + 158, 296, 18, cp, pt=6.6, color=INKT, align="c", anchor="m")
        body(k, 36, y0 + 178, 274, 74, tx, align="l")

    # column 2
    X2, W2 = 347, 296
    sec(k, 352, 226, 290, "The Flywheel")
    body(k, X2, 271, W2, 140, "The flywheel is **4 in** wide. It holds one speed band, about 2,300 to 2,450 rpm, from 24 to 96 in. At idle it spins at 3,000 rpm so the spin up is short. " + dummy(8))
    k.image(R + 'top.png', 352, 422, 285, 52, fit="cover", r=10)
    k.text(X2, 478, W2, 20, "Shooter CAD view", pt=6.6, color=INKT, align="c", anchor="m")
    sec(k, 352, 512, 290, "Hood")
    body(k, X2, 549, W2, 105, "The hood moves between **70 and 85 degrees**. The code solves the angle again every loop from the measured wheel speed. A slow wheel still lands the ball.")
    sec(k, 352, 657, 290, "Feed Gate")
    body(k, X2, 695, W2, 140, "An index gate sits in front of the wheel. It blocks feeds while we drive. A ball is released when **four checks** pass. " + dummy(9))
    sec(k, 352, 842, 290, "Shot Table")
    body(k, X2, 880, W2, 230, "A tuned shot table keeps anchors at three distances: min, ideal and max. **Projectile physics** fills the gaps between them. Hood servos drift, so the hood uses a calibration table and a tuner OpMode. " + dummy(14))
    k.image(crop_png(CADD + 'shooter_v4_hood_raised.png', 'ft'), 380, 1118, 240, 172, fit="contain")
    k.text(X2, 1294, W2, 20, "Shooter with the hood raised", pt=6.6, color=INKT, align="c", anchor="m")
    sec(k, 352, 1328, 290, "Error Budget")
    body(k, X2, 1368, W2, 240, "At 60 in the opening gives us **10.1 in** each side. The flywheel and turret errors use about two thirds of it. Range changes with speed squared, so 75 rpm moves a shot about 5.5 in. Risk: the hood arrival is not awaited in code yet. " + dummy(10))
    bud = [("Opening half", 10.1, "10.1 in", "9AA5B1"), ("Flywheel 90 rpm", 6.6, "6.6 in", "F7941D"), ("Turret 1.5 deg", 1.6, "1.6 in", BLU), ("Both combined", 6.8, "6.8 in", "00A857")]
    for i, (a, v, t, c) in enumerate(bud):
        yy = 1625 + i * 28
        k.text(X2, yy, 122, 24, a, pt=6.8, color=INKT, anchor="m")
        k.rect(X2 + 126, yy + 5, 110 * v / 10.1, 14, fill=c, r=3)
        k.text(X2 + 131 + 110 * v / 10.1, yy, 70, 24, t, pt=6.8, color=INKT, anchor="m")

    # right panel frame
    for (x, y, w, h) in [(655, 99, 655, 9), (655, 99, 9, 1654), (655, 1745, 655, 8), (1301, 99, 9, 1654)]:
        k.rect(x, y, w, h, fill=BLU)
    k.text(690, 108, 600, 50, "Trajectory to the up CELL", pt=15, color=INKT, anchor="m")
    # param box
    k.rect(688, 215, 248, 413, fill="FFFFFF", line="000000", lw=1.3)
    r75 = solve(72, 75)
    prm = [("(drag-free model)", INKT, 7.8), ("v=%d in/s" % round(r75["v"]), INKT, 13), ("h0=10.63in", "E02020", 13), ("h=56.7in", "7CC242", 13),
           ("d=72in", "5B9BD5", 13), ("t=%.1fs" % r75["tof"], INKT, 13), ("hood=75deg", INKT, 13), ("descent=%ddeg" % round(r75["desc"]), INKT, 13)]
    yy = 236
    for t, c, s in prm:
        k.text(700, yy, 232, 38 if s > 9 else 30, t, pt=s, color=c, anchor="m")
        yy += 38 if s > 9 else 32
    # plot
    gx0, gy0, gw, gh = 975, 188, 260, 332
    k.rect(gx0, gy0, gw, gh, fill="C1ACDC")
    for i in range(1, 8):
        k.line(gx0 + i * gw / 8, gy0, gx0 + i * gw / 8, gy0 + gh, color="AE96CF", w=0.5)
    for i in range(1, 11):
        k.line(gx0, gy0 + i * gh / 11, gx0 + gw, gy0 + i * gh / 11, color="AE96CF", w=0.5)
    k.line(gx0 + gw, gy0, gx0 + gw, gy0 + gh, color="7B55B8", w=1.0, dash=True)
    sc = 3.25
    def P(xi, yi):
        return (gx0 + 10 + xi * sc, gy0 + gh - yi * sc)
    for th, col, dsh in [(75, "3F51B5", False), (50, "D64545", True)]:
        r = solve(72, th); v = r["v"]; t = math.radians(th)
        pts = []
        for i in range(0, 61):
            tt = r["tof"] * i / 60
            pts.append(P(v * math.cos(t) * tt, H0 + v * math.sin(t) * tt - 0.5 * GRAV * tt * tt))
        k.curve(pts, color=col, w=1.3, dash=dsh)
    cx_, cy_ = P(72, HT)
    k.poly([(cx_ - 30, cy_ - 4), (cx_ - 30, cy_ + 10), (cx_ + 20, cy_ + 10), (cx_ + 20, cy_ - 4), (cx_ + 14, cy_ - 4), (cx_ + 14, cy_ + 2), (cx_ - 24, cy_ + 2), (cx_ - 24, cy_ - 4)], fill="F2C230", line="231F20", lw=0.8)
    k.text(cx_ - 52, cy_ + 15, 80, 30, "up CELL", pt=7, color=INKT)
    k.rect(gx0 + 10, gy0 + gh - H0 * sc, 22, H0 * sc, fill="1B3F6B")
    # axes
    k.line(gx0, gy0 + gh + 4, gx0, gy0 - 8, color="000000", w=2.2)
    k.poly([(gx0 - 12, gy0 + 6), (gx0 + 12, gy0 + 6), (gx0, gy0 - 22)], fill="231F20")
    k.line(gx0 - 4, gy0 + gh, gx0 + gw + 20, gy0 + gh, color="000000", w=2.2)
    k.poly([(gx0 + gw - 6, gy0 + gh - 14), (gx0 + gw - 6, gy0 + gh + 14), (gx0 + gw + 30, gy0 + gh)], fill="231F20")
    k.image(vtext("height", "vh", 64, INKT, 52, 220), 940, gy0 + 15, 38, 210, fit="contain")
    k.text(gx0 - 5, gy0 + gh + 20, 60, 36, "0", pt=14, color=INKT)
    k.text(1040, gy0 + gh + 24, 150, 40, "distance", pt=13, color=INKT, align="c")
    k.text(1190, gy0 + gh + 20, 100, 36, "96 in", pt=14, color=INKT)
    k.text(1060, gy0 + gh - 78, 175, 48, [dict(text="75 deg: drops in", size=6.5 * FONT, color="3F51B5"), dict(text="50 deg: too flat", size=6.5 * FONT, color="D64545")], gap=0)
    # robot render with overlay
    k.image(crop_png(R + 'side_left.png', 'sideL'), 690, 660, 300, 300, fit="contain")
    k.text(1010, 664, 200, 30, "hood angle", pt=9, color=INKT)
    # triangle (velocity components)
    tri = [(1012, 810), (1120, 808), (1005, 1012)]
    k.line(1012, 810, 1120, 808, color="7CC242", w=2.2)
    k.line(1012, 810, 1005, 1012, color="5B9BD5", w=2.2)
    k.line(1120, 808, 1005, 1012, color="E8E01A", w=2.2)
    k.text(1052, 770, 60, 34, "vx", pt=11, color=INKT)
    k.text(1022, 822, 120, 34, "180-a", pt=10, color=INKT)
    k.text(980, 880, 40, 34, "vy", pt=11, color=INKT)
    k.text(1078, 880, 150, 70, "exit speed v", pt=11, color=INKT, gap=0)
    # formula
    k.text(698, 1020, 590, 44, "v^2 = g·d^2 / (2·cos^2(a)·(d·tan(a) - dh))", pt=11, color=INKT, anchor="m")
    k.text(698, 1062, 560, 30, "exit speed from distance (d) and hood angle", pt=10.5, color=INKT)
    # table
    cols = [("DISTANCE", 95), ("HOOD", 70), ("EXIT SPEED", 115), ("WHEEL", 105), ("FLIGHT", 90), ("DESCENT", 105)]
    x = 698; y = 1108
    for c, w in cols:
        k.text(x, y, w - 2, 28, c, pt=7.2, color="FFFFFF", head=True, fill=BLU, anchor="m", align="c")
        x += w
    y += 29
    for i, (d_, th) in enumerate([(24, 85), (48, 80), (72, 75), (96, 70)]):
        r = solve(d_, th)
        vals = ["%d in" % d_, "%d deg" % th, "%d in/s" % round(r["v"]), "%d rpm" % round(r["rpm"], -1), "%.1f s" % r["tof"], "%d deg" % round(r["desc"])]
        x = 698
        for (c, w), vv in zip(cols, vals):
            k.text(x, y, w - 2, 26, vv, pt=8.4, color=INKT, align="c", anchor="m", fill="EAF1F9" if i % 2 == 0 else "FFFFFF")
            x += w
        y += 27
    # control law graphic
    k.line(708, 1290, 945, 1273, color="E02020", w=2.4)
    k.line(708, 1290, 708, 1495, color="7CC242", w=2.6)
    k.poly([(696, 1488), (720, 1488), (708, 1514)], fill="7CC242")
    k.line(944, 1273, 944, 1365, color="5BC8E8", w=2.6)
    k.poly([(932, 1358), (956, 1358), (944, 1384)], fill="5BC8E8")
    k.line(780, 1478, 890, 1282, color="C040A0", w=2.4)
    k.text(722, 1350, 80, 70, "cut", pt=17, color="7CC242", anchor="m")
    k.text(950, 1285, 200, 54, "full power", pt=17, color="5BC8E8")
    k.text(960, 1375, 330, 120,
           ["full power if error > 75 rpm", "PID + FF if |error| <= 75 rpm", "kP = 0.0006   kI = 0.0005", "cut power if 60 rpm over"], pt=8.4, color=INKT, gap=3)
    k.text(960, 1500, 330, 30, "ready if |error| < 90 rpm", pt=10, color=INKT)
    # bottom
    k.text(682, 1552, 500, 60, "Ready to shoot", pt=19, color=INKT, anchor="m")
    k.text(668, 1608, 616, 138,
           "The ball is released when **all four checks pass**. The distance must be inside a legal range for the shot table. The wheel speed must be in the band. The hood must have arrived. The turret must be on target. Using the **same speed band**, we can shoot again as soon as the wheel recovers.",
           pt=BODY + 0.3, color=INKT, gap=3)


# ======================================================================= PAGE 14
def page_14(D):
    p = D.page(name='p14'); k = K(p)
    k.header(14, [("inspire", "38BCEE", INKT), ("think", "E1D10A", INKT), ("design", "F14B28", INKT)])
    k.rect(0, 99, 655, 1653, fill=BLU)
    W = "FFFFFF"
    k.text(42, 96, 560, 110, "Turret", pt=38, color=W, head=True, anchor="m")
    # section 1
    sec(k, 32, 212, 190, "Cascade\ncontroller", pt=16, color=W, h=90)
    badge(k, 255, 254, 64, "Innovative|Design", "00A857")
    body(k, 25, 314, 297, 290, "A moving target needs a turret that can **lead it**. The turret has an outer position loop, an inner velocity loop and a feedforward stack. The position loop sets a **speed from the angle error**. The velocity loop turns that speed into motor power. The motor power is capped at **0.85**.", color=W)
    sec(k, 32, 560, 290, "Why a turret?", pt=16, color=W, h=44)
    body(k, 25, 598, 297, 120, "A turret lets us track the HIVE **without turning the chassis**. The driver keeps scoring while being pushed. It also allows shooting on the move.", color=W)
    sec(k, 32, 716, 290, "Cable chain", pt=16, color=W, h=44)
    body(k, 25, 758, 297, 140, "We learned a lot from last year. Wiring was tricky, and we had a **loose cable sleeve**. Now an **igus energy chain** carries the cables around the turret ring, so the turret turns freely.", color=W)
    # col 2
    sec(k, 352, 358, 290, "Feedforward", pt=16, color=W, h=44)
    body(k, 347, 398, 296, 210, "Feedforward adds the motion we already know about. It uses the **chassis rotation**, the chassis translation and the driver input times 0.5. The translation term is the line of sight sweep. " + dummy(8), color=W)
    k.rect(347, 607, 296, 289, fill="FFFFFF", r=14)
    k.image(CADD + 'igus-chain/igus_opaque.png', 357, 619, 276, 265, fit="contain")
    k.text(347, 897, 296, 20, "The igus energy chain on the turret", pt=6.8, color=W, align="c", anchor="m")
    # dashed divider
    xx = 25
    while xx < 640:
        k.rect(xx, 920, 36, 4, fill=W)
        xx += 50
    # section: FLOWER ramp
    sec(k, 27, 953, 190, "FLOWER\nramp", pt=16, color=W, h=90)
    badge(k, 248, 995, 60, "Reliable|Design", "F2D600")
    # quote
    k.rect(18, 1052, 309, 95, fill="FFFFFF")
    for yy in (1052, 1146):
        xx = 18
        while xx < 327:
            k.rect(xx, yy, 7, 2, fill="231F20"); xx += 11
    k.text(20, 1056, 62, 90, "“", pt=32, color="1A7CA8", head=True, anchor="m", align="c")
    k.line(87, 1072, 87, 1128, color="1A7CA8", w=1.2)
    k.text(100, 1062, 224, 80, "“Stow the turret by hand before INIT” - **programmers**", pt=8.3, color="231F20", anchor="m", align="ln")
    k.rect(27, 1157, 295, 231, fill="FFFFFF", r=14)
    k.image(crop_png(CADD + 'flower_v2_cad.png', 'fv2'), 37, 1167, 275, 211, fit="contain")
    k.text(25, 1394, 297, 36, "FLOWER v2: the ramp swings down 32 degrees to the tiles.", pt=7, color=W, align="c", gap=0)
    body(k, 25, 1458, 297, 220, "One servo swings the ramp **32 degrees** down to the tiles. The stand-off is about 12 in. With the ramp out, the intake stays stowed and **holding collect** pulls POLLEN up the ramp. The nose intake is one compact unit, so the robot has the space and the servo this mechanism needs.", color=W)
    # col 2
    body(k, 347, 962, 268, 120, "We park nose in, about **12 in** from the FLOWER. Harvesting works one POLLEN at a time.", color=W)
    sec(k, 352, 1085, 290, "Interlock", pt=16, color=W, h=46)
    body(k, 347, 1135, 268, 120, "The ramp and the intake take turns in software, so they can never fight over the same space. **A stale pose is flagged**, never reused.", color=W)
    sec(k, 352, 1262, 290, "FLOWER v1", pt=16, color=W, h=46)
    body(k, 347, 1306, 268, 190, "FLOWER v1 was a rack and a ramp. We chose it because the **double intake** left no room for more servos, and there was no space anywhere else on the robot for a bigger mechanism. It did not work well, so we **pivoted** to the nose intake and the single-servo ramp.", color=W)
    k.rect(347, 1512, 296, 190, fill="FFFFFF", r=14)
    k.image(crop_png(CADD + 'flower_v1_old_cad.png', 'of1'), 355, 1520, 280, 174, fit="contain")
    k.text(347, 1708, 296, 20, "FLOWER v1: the old rack and ramp", pt=6.8, color=W, align="c", anchor="m")
    # right: robot render + heading
    k.image(crop_png(R + 'hero_front_left.png', 'hfl'), 735, 104, 330, 224, fit="contain")
    k.text(685, 326, 440, 95, "Position loop\nVelocity loop", pt=17, color=INKT, gap=0)
    eq = ["w_cmd = kP * (theta_target - theta)", "kP = 9.0 rad/s per rad", "w_cmd is capped at 8 rad/s", "tolerance = 1.5 deg",
          "", "power = kS*sign(w) + kV*w_cmd + kA*a + kP2*(w_cmd - w)", "kS = 0.06    kV = 0.033    kA = 0.002", "kP2 = 0.02   accel limit = 60 rad/s^2",
          "", "w_ff = w_chassis + w_translation + 0.5 * w_driver", "w_cmd = w_cmd + w_ff", "power cap = 0.85"]
    yy = 438
    for e in eq:
        if e:
            k.text(697, yy, 600, 30, e, pt=8.8, color=INKT, anchor="m")
        yy += 31 if e else 14
    # cascade diagram (right edge)
    nodes = [(1162, 178, "A", "target"), (1178, 281, "B", "pos"), (1198, 370, "C", "vel"), (1218, 480, "D", "motor")]
    k.line(1127, 143, 1235, 118, color="231F20", w=1.2)
    k.line(1162, 140, 1162, 160, color="231F20", w=1.2)
    for i in range(3):
        a, b = nodes[i], nodes[i + 1]
        k.line(a[0], a[1] + 17, b[0], b[1] - 17, color="231F20", w=1.2)
    for (cx, cy, l, t) in nodes:
        k.oval(cx - 17, cy - 17, 34, 34, fill="FFFFFF", line="231F20", lw=1.0)
        k.text(cx - 17, cy - 17, 34, 34, l, pt=7.5, color=INKT, align="c", anchor="m")
        k.text(cx + 22, cy - 12, 70, 24, t, pt=6, color=INKT, anchor="m")
    for (x1, y1, x2, y2) in [(1135, 215, 1160, 252), (1150, 300, 1178, 330), (1165, 400, 1198, 440)]:
        k.line(x1, y1, x2, y2, color="E02020", w=1.3, arrow=True)
    k.line(1228, 210, 1228, 250, color="231F20", w=1.0, arrow=True)
    k.text(1236, 215, 40, 24, "w_ff", pt=6, color=INKT)
    k.oval(1212, 540, 58, 40, fill="1B3F6B")
    k.line(1218, 500, 1226, 540, color="231F20", w=1.0)
    # white card
    k.rect(627, 938, 658, 244, fill="FFFFFF", line=BLU, lw=3.6, r=4)
    k.text(640, 955, 620, 56, "How does it know where it is?", pt=17, color=INKT, anchor="m")
    k.text(642, 1010, 630, 28, "Two encoders give the turret angle and speed:", pt=9.2, color=INKT, anchor="m")
    k.text(642, 1042, 630, 32, "motor 28 tick/rev    absolute 4,000 tick/rev, 4:1 up", pt=9.6, color=INKT, anchor="m")
    k.text(642, 1078, 630, 32, "w = 0.5 * w_motor + 0.5 * w_abs", pt=9.6, color=INKT, anchor="m")
    k.text(642, 1120, 630, 50, "The motor reading is dropped if the two differ by more than 1.5 rad/s. " + dummy(6), pt=9.2, color=INKT)
    k.text(675, 1195, 600, 100, "Gear train\nSoft limits", pt=19, color=INKT, gap=0)
    eq2 = ["ratio = (60 / 9) * (72 / 15) = 32", "ratio = 6.67 * 4.8 = 32 : 1", "", "limit = +/- 200 deg", "",
           "zero: stow by hand before INIT", "seed = off until verified", "", "log: CSV tuner, 721 lines", "gains pasted back to code after tuning"]
    yy = 1318
    for e in eq2:
        if e:
            k.text(682, yy, 600, 32, e, pt=10.4, color=INKT, anchor="m")
        yy += 38 if e else 14
