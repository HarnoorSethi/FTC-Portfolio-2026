from bfkit import *

import os
from PIL import Image
def T(path):
    """crop transparent margins of a render (cached)"""
    os.makedirs('/tmp/work/out/trim', exist_ok=True)
    o = '/tmp/work/out/trim/' + os.path.basename(path)
    if not os.path.exists(o):
        im = Image.open(path).convert('RGBA')
        bb = im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
        im.crop(bb).save(o)
    return o

BLUE = "4889C8"
INK = "231F20"
W = "FFFFFF"
CHIPS_A = [("inspire", "38BFF2", INK), ("think", "E9D909", INK), ("innovate", "00A857", INK)]
CHIPS_B = [("inspire", "38BFF2", INK), ("think", "E9D909", INK), ("design", "F14B28", INK)]


def numhead(k, x, y, n, title, color=INK, tpt=13.5, npt=26, w=300):
    """big light numeral + light title (reference style). y = top of numeral line"""
    k.text(x, y - 10, 50, 68, str(n), pt=npt, color=color, anchor="m")
    off = 24 if str(n) == "1" else 36
    k.text(x + off, y + 3, w - off, 50, title, pt=tpt, color=color, anchor="m")


def h1(k, x, y, w, t, color=INK, pt=17):
    k.text(x, y - 4, w, 56, t, pt=pt, color=color, anchor="m")


def body(k, x, y, w, h, t, color=INK, pt=8.6, align="l"):
    k.text(x, y, w, h, t, pt=pt, color=color, align=align, ls=1.0, gap=2)


def cap(k, x, y, w, t, color=INK, pt=6.6):
    k.text(x, y, w, 20, t, pt=pt, color=color, align="c", anchor="m")


def card(k, x, y, w, h, num, l1, l2, img=None, ph=None, fit="contain", capt=None):
    k.rect(x, y, w, h, fill=W, line=BLUE, lw=1.6, r=24)
    k.rect(x, y, w, 92, fill=BLUE, r=24)
    k.rect(x, y + 50, w, 42, fill=BLUE)
    k.text(x + 14, y + 8, 60, 78, str(num), pt=30, color=W, anchor="m")
    k.text(x + 70, y + 8, w - 84, 78, [l1, l2], pt=15, color=W, align="r", anchor="m", gap=0, ls=0.95)
    ih = h - 92 - 40
    if img:
        k.image(img, x + 12, y + 100, w - 24, ih, fit=fit)
    else:
        k.photo_ph(x + 14, y + 102, w - 28, ih - 4, ph or "PHOTO")
    if capt:
        cap(k, x, y + h - 30, w, capt)


def procon(k, x, y, w, title, items, boxed=False, h=None, pt=8.6):
    n = len(items)
    hh = h or (40 + 19 * n)
    if boxed:
        k.rect(x, y, w, hh, fill=BLUE, r=22)
        k.text(x + 14, y + 6, w - 24, hh - 8, [dict(text=title, size=10.4 * FONT, color=W, gap=0)] + [dict(text=t, size=pt * FONT, color=W, gap=0) for t in items], pt=pt, color=W, ls=1.0, gap=0)
    else:
        k.text(x + 14, y, w - 20, hh, [dict(text=title, size=10.4 * FONT, color=INK, gap=0)] + [dict(text=t, size=pt * FONT, color=INK, gap=0) for t in items], pt=pt, color=INK, ls=1.0, gap=0)
    return hh


def badge(k, x, y, d, ring, l1, l2):
    k.oval(x, y, d, d, fill=W, line=ring, lw=1.2)
    k.text(x, y, d, d, [dict(text=l1, head=True, size=(6.2 if len(l1) <= 8 else 4.9) * FONT, color=INK), dict(text=l2, size=(5.8 if len(l1) <= 8 else 5.0) * FONT, color="5E5C5C")], align="c", anchor="m", gap=0)


def frame(k, x, y, w, h):
    k.rect(x, y, w, h, fill=W, line=BLUE, lw=3.6)


# ====================================================== PAGE 10
def page_10(D):
    p = D.page(name='p10'); k = K(p)
    k.header(10, CHIPS_A)
    k.rect(0, 99, 655, 1653, fill=BLUE)
    # logo
    k.rect(40, 124, 112, 142, fill="5285CC")
    k.oval(44, 142, 106, 106, fill=W)
    k.image(LOGO, 52, 166, 90, 56, fit="contain")
    k.text(172, 120, 480, 100, "Cheesy Chips", pt=31, color=W, anchor="m")
    k.text(170, 222, 480, 54, ["--- km of filament, --- hours of assembling", "--- hours of 3D design, --- hours of coding"], pt=10.3, color=W, gap=0, ls=0.95)
    # highlights
    numhead(k, 25, 288, 1, "Autonomous", W, w=300)
    body(k, 25, 340, 300, 70, "A preload volley, then we **park**. Timings are still being tuned on the robot.", W)
    numhead(k, 355, 292, 2, "Innovative Design", W, w=300)
    body(k, 348, 346, 302, 70, "**One nose intake** and a turret driven by a motor.", W)
    numhead(k, 185, 398, 3, "Elegant Design", W, w=360)
    body(k, 184, 448, 372, 46, "**One ball path** from the nose to the flywheel. Each subsystem has **one job**.", W, align="c")
    h1(k, 34, 497, 600, "Engineering process", W, pt=17.5)
    # 1 Ideate
    numhead(k, 25, 545, 1, "Ideate", W, w=300)
    body(k, 25, 611, 297, 243, "We read the game manual and list what the robot must do. We conduct **a SWOT analysis** of the ideas and write the **costs and benefits** of each option. We pick the ideas we think can be built and tested. We study how each one can be integrated into the robot and **decide the parts** we need.", W)
    k.photo_ph(25, 859, 289, 163, "Brainstorming photo")
    cap(k, 25, 1022, 289, "Brainstorming", W)
    # right top paragraph
    body(k, 348, 565, 297, 130, "we **test** to validate our concepts. We test in the simulator first, then at the desk, then on the robot. We **log what failed** and run it again.", W, align="l")
    k.photo_ph(433, 715, 139, 140, "Prototype photo")
    cap(k, 395, 860, 220, "Prototype of the intake", W)
    # 4 params
    numhead(k, 348, 903, 4, "Parameters", W, w=300)
    body(k, 346, 969, 297, 123, "We **measure or calculate** the values the robot depends on, such as gear ratios and hood angles. We **write the final values** into the code.", W)
    k.rect(347, 1098, 296, 150, fill=W, r=16)
    k.image(A + "sim_shoot.png", 352, 1102, 286, 142, fit="contain")
    cap(k, 347, 1250, 296, "Shot test in the simulator", W)
    # 2 CAD
    numhead(k, 25, 1075, 2, "CAD in Onshape", W, w=300)
    body(k, 25, 1134, 297, 185, "We design in **Onshape** with master sketches, so parts update when a size changes. The same CAD becomes the model in our **simulator**, so we can check how the robot fits and moves before we build it.", W)
    k.image(T(R + "top.png"), 25, 1341, 296, 163, fit="contain")
    cap(k, 25, 1504, 296, "Robot fitting within the field", W)
    # 5 efficiency
    numhead(k, 350, 1305, 5, "Efficiency", W, w=300)
    body(k, 345, 1373, 297, 163, "We do a final check of each system. We removed the second intake because the simulator showed about the same scoring with one. We keep the robot to **8 motors and 5 servos**.", W)
    k.rect(350, 1540, 290, 152, fill=W, r=16)
    k.image(T(R + "close_intake.png"), 356, 1544, 278, 144, fit="contain")
    cap(k, 350, 1694, 290, "Beam-break switches for the intake", W)
    # 3 prototype
    numhead(k, 25, 1575, 3, "Prototype", W, w=300)
    body(k, 25, 1642, 297, 100, "Using manufacturing processes such as **3D printing** and **CNC milling**, we make the parts our robot needs.", W)
    # robot render right
    k.image(T(R + "hero_front_right.png"), 700, 150, 570, 560, fit="contain")
    # iteration cards
    card(k, 668, 760, 295, 280, 1, "DECODE", "Robot MK1", img=None, ph="DECODE robot", capt="DECODE robot 2025-26")
    card(k, 989, 760, 296, 280, 2, "BIOBUZZ", "Robot MK2", img=T(R + "hero_front_left.png"), capt="BIOBUZZ robot MK2")
    body(k, 668, 1048, 296, 100, "Our **DECODE** robot from 2025-26. It had a **double-sided intake**, a 360 degree turret and color sensors in the feeder.")
    body(k, 989, 1048, 296, 100, "Our **BIOBUZZ** robot now. It has **one nose intake**, a motor-driven turret and **4 beam-break switches**.")
    card(k, 668, 1155, 295, 278, 3, "BIOBUZZ", "Robot MK3", img=T(R + "hero_rear_right.png"), capt="BIOBUZZ robot MK3")
    card(k, 989, 1155, 296, 278, 4, "BIOBUZZ", "Robot MK4", img=T(R + "side_left.png"), capt="BIOBUZZ robot MK4")
    body(k, 668, 1442, 296, 110, dummy(17))
    body(k, 989, 1442, 296, 110, dummy(15))
    k.image(T(R + "side_right.png"), 668, 1572, 620, 160, fit="contain")


# ====================================================== PAGE 11
def page_11(D):
    p = D.page(name='p11'); k = K(p)
    k.header(11, CHIPS_A)
    k.text(26, 100, 330, 110, "Chassis", pt=30, color=INK, head=True, anchor="m")
    badge(k, 348, 115, 80, "00A857", "Innovative", "Design")
    h1(k, 32, 226, 300, "Goals", pt=17.5)
    numhead(k, 25, 278, 1, "Compact design", w=300)
    body(k, 25, 332, 297, 95, "Everything must fit in **320 by 334 mm** and stay **low**.")
    numhead(k, 25, 421, 2, "Fast and precise", w=300)
    body(k, 25, 475, 297, 80, "The tuned path-following top speed is **72 in/s forward** and **46 in/s sideways**.")
    numhead(k, 25, 558, 3, "Field-centric", w=300)
    body(k, 25, 610, 297, 95, "The driver steers relative to the field. **Two odometry pods** and the IMU track where it is.")
    h1(k, 32, 716, 300, "Iterations", pt=17.5)
    card(k, 25, 762, 296, 278, 1, "Mecanum", "Chassis MK1", ph="Chassis MK1 photo", capt="Implementation of Mecanum")
    body(k, 25, 1048, 297, 290, "It's a chassis that offers a lot of **flexibility** and needs only 4 motors, with **low complexity**. " + dummy(34))
    procon(k, 25, 1345, 296, "Pros", ["One motor per wheel", "Small volume", "Low complexity"])
    procon(k, 25, 1459, 296, "Cons", ["Low traction", "Lower strafing speed"], boxed=True, h=82)
    # column 2
    card(k, 347, 220, 295, 278, 2, "Mecanum", "Chassis MK2", img=T(R + "top.png"), capt="Our current chassis")
    body(k, 347, 505, 296, 310, "In the summer, we designed and built a **mecanum chassis** that uses 4 wheels, each driven by its own motor. " + dummy(40))
    procon(k, 347, 830, 296, "Pros", ["Fast in any direction"])
    procon(k, 347, 895, 295, "Cons", ["Extra weight in wheels", "Complex software", "Large vertical volume"], boxed=True, h=114)
    card(k, 347, 1018, 295, 278, 3, "Mecanum", "Chassis MK3", ph="Chassis MK3 photo", capt="Our chassis implementation")
    body(k, 347, 1303, 296, 225, "The MK2 chassis takes up a lot of space. " + dummy(36))
    # bottom wide image
    k.rect(25, 1553, 608, 165, fill="EEF2F7")
    for i, nm in enumerate(["side_left.png", "top.png", "side_right.png"]):
        k.image(T(R + nm), 35 + i * 200, 1558, 190, 156, fit="contain")
    cap(k, 25, 1722, 608, "Front view of the robot")
    # right panel
    frame(k, 659, 103, 649, 991)
    k.text(686, 120, 400, 52, "Mecanum Drive", pt=17.5, color=INK, anchor="m")
    k.rect(687, 178, 250, 290, fill=W, line="C8C7C7", lw=0.75)
    k.text(697, 190, 235, 275, [dict(text="(from our robot)", size=9 * FONT), dict(text="size = 320 x 334 mm", size=10.5 * FONT, gap=3), dict(text="motors = 4", size=10.5 * FONT, gap=3),
                               dict(text="v_fwd = 72 in/s", size=10.5 * FONT, gap=3), dict(text="v_strafe = 46 in/s", size=10.5 * FONT, gap=3), dict(text="m = --- kg", size=10.5 * FONT, gap=3), dict(text="mu = ---", size=11.5 * FONT)], pt=11, color=INK, gap=4)
    # wheel diagram (simple shapes)
    k.rect(962, 182, 336, 280, fill="E8EAEE", r=10)
    k.oval(985, 262, 150, 150, fill="C9CED6", line="5A6272", lw=1.2)
    k.oval(1120, 262, 150, 150, fill="C9CED6", line="5A6272", lw=1.2)
    for cx in (1060, 1195):
        for i in range(8):
            import math
            a = i * math.pi / 4
            k.line(cx + 25 * math.cos(a), 337 + 25 * math.sin(a), cx + 60 * math.cos(a), 337 + 60 * math.sin(a), color="5A6272", w=1.2)
    k.text(985, 190, 150, 24, "mecanum wheel", pt=6.4, color=INK, align="c")
    k.text(1120, 190, 150, 24, "mecanum wheel", pt=6.4, color=INK, align="c")
    k.line(1060, 337, 1060, 440, color="00A8C8", w=2, arrow=True)
    k.line(1195, 337, 1195, 440, color="00A8C8", w=2, arrow=True)
    k.line(1085, 337, 1160, 300, color="F14B28", w=2, arrow=True)
    k.text(1030, 440, 100, 22, "G/8", pt=7.5, color="00A8C8", head=True, align="c")
    k.text(1165, 440, 100, 22, "G/8", pt=7.5, color="00A8C8", head=True, align="c")
    for (y, h, lines) in [(482, 183, ["Vx = (w1 + w2 + w3 + w4) * r / 4", "Vy = (-w1 + w2 + w3 - w4) * r / 4", "w = (-w1 + w2 - w3 + w4) * r / (4 * (lx + ly))"]),
                          (678, 188, ["F_forward = N * sin(pi/4) * mu", "", "       = (mg/4) * mu  (dummy)"]),
                          (879, 188, ["P = (v_fwd - v_strafe) / v_fwd", "", "= --- %  (dummy)"])]:
        k.rect(687, y, 601, h, fill=W, line="C8C7C7", lw=0.75)
        k.text(698, y + 6, 585, h - 12, [dict(text=t, size=13 * FONT) for t in lines], pt=13, color=INK, gap=6, anchor="m")
    # below the panel
    body(k, 668, 1113, 296, 75, dummy(9))
    procon(k, 668, 1203, 296, "Cons", ["Slow to strafe"], h=50)
    procon(k, 668, 1268, 296, "Pros", ["Easily replaceable", "Increased traction", "Less complex", "Fewer motors"], boxed=True, h=158)
    body(k, 989, 1113, 296, 140, dummy(26))
    k.rect(989, 1262, 296, 90, fill="EEF2F7", r=10)
    k.image(T(R + "side_left.png"), 995, 1265, 140, 84, fit="contain")
    k.image(T(R + "side_right.png"), 1140, 1265, 140, 84, fit="contain")
    cap(k, 989, 1356, 296, "Left and right side views of the robot")
    h1(k, 674, 1437, 300, "Optimizations", pt=17.5)
    body(k, 668, 1488, 296, 265, "A classic mecanum chassis needs **4 motors**. " + dummy(34))
    k.image(T(R + "top.png"), 989, 1385, 296, 355, fit="contain")


# ====================================================== PAGE 12
def page_12(D):
    p = D.page(name='p12'); k = K(p)
    k.header(12, CHIPS_B)
    k.text(26, 100, 280, 106, "Intake", pt=28, color=INK, head=True, anchor="m")
    badge(k, 305, 112, 85, "E9D909", "Reliable", "Design")
    h1(k, 32, 226, 300, "Objectives", pt=17.5)
    numhead(k, 25, 272, 1, "Rapid intake", w=300)
    body(k, 25, 330, 297, 90, "We need a design that is as **fast as possible**, to keep the cycle time short. The principle is **\"Touch it, own it.\"**")
    numhead(k, 25, 438, 2, "Exact count", w=300)
    body(k, 25, 490, 297, 80, "The robot may hold **4 POLLEN**. We want to know the count exactly.")
    numhead(k, 25, 578, 3, "Modular design", w=300)
    body(k, 25, 628, 297, 70, "to make changes easy, so we can test and reach the **most efficient way** of collecting.")
    h1(k, 32, 704, 300, "Iterations", pt=17.5)
    card(k, 25, 750, 296, 280, 1, "Double", "Intake v1", img=T("/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/old_hero_finished.png"), capt="Double intake v1")
    body(k, 25, 1035, 297, 250, "The first iteration is **a double intake**: one roller frame at the front and one at the back. It took up the space around the robot, so we **could not add more servos** for a bigger FLOWER mechanism.")
    procon(k, 25, 1272, 296, "Pros", ["Easy to build", "Also serves as a guide"])
    procon(k, 25, 1356, 296, "Cons", ["Hard to operate", "Inefficient, long intake time", "No room for a bigger FLOWER"], boxed=True, h=100)
    card(k, 25, 1466, 296, 272, 2, "Nose", "Intake v2", img=T(R + "close_intake.png"), capt="Single nose intake v2")
    # column 2
    body(k, 347, 222, 296, 290, "To reach our goals, we chose **one nose intake**, v2, with 305 mm reach and a 300 mm mouth. **Two pivot servos** lower it to pick up and stow it. **Two motors** run the pickup and the transfer. " + dummy(26))
    procon(k, 347, 512, 296, "Pros", ["Instant retrieval", "Easy to operate"])
    procon(k, 347, 597, 295, "Cons", ["Large volume", "Narrow intake area", "Too short pivot arm"], boxed=True, h=113)
    card(k, 347, 720, 295, 278, "", "Intake v2", "deployed", img=T(R + "hero_deployed.png"), capt="Intake v2, lowered to pick up")
    body(k, 347, 1005, 296, 310, "Because the intake has to **fold away** when we are not collecting, we added two pivot servos. " + dummy(40))
    procon(k, 347, 1316, 296, "Cons", ["Unable to pick up 2 balls", "side by side", "Large volume"], h=96)
    procon(k, 347, 1428, 295, "Pros", ["Instant retrieval", "Large pickup radius", "POLLEN does not exit", "Can take from stack"], boxed=True, h=132)
    h1(k, 352, 1566, 300, "Transmission", pt=17.5)
    body(k, 347, 1615, 296, 136, "In the final design, we want the game elements to be picked up by a **compact ramp**.")
    # column 3 top
    body(k, 668, 115, 296, 160, dummy(27))
    k.image(T(R + "close_turret.png"), 1057, 90, 158, 158, fit="contain")
    cap(k, 1010, 248, 250, "Improved intake", pt=6.4)
    frame(k, 659, 284, 649, 201)
    k.text(670, 292, 600, 56, "Ball count", pt=17.5, color=INK, anchor="m")
    k.text(670, 360, 620, 115, [dict(text="count = switch1 + switch2 + switch3 + switch4      (0 to 4)", size=10 * FONT, gap=6),
                                dict(text="jam  =  motor speed low while power is high", size=10 * FONT)], pt=10, color=INK, anchor="m")
    k.text(666, 500, 360, 100, "Transfer", pt=30, color=INK, head=True, anchor="m")
    badge(k, 1025, 508, 85, "E9D909", "Reliable", "Design")
    card(k, 668, 622, 295, 278, 1, "Transfer", "v1", ph="Master sketch of the v1 transfer", capt="Transfer v1: bootleg wheel based")
    body(k, 668, 905, 296, 210, "The v1 transfer was **bootleg wheel based**. The robot holds up to 4 POLLEN until they are fed to the shooter. The system has **a box with walls**, **bootleg wheels** that move the POLLEN and **4 beam-break switches**.")
    procon(k, 668, 1104, 296, "Pros", ["Simple design", "Iterative design"])
    procon(k, 668, 1192, 296, "Cons", ["Balls sometimes jump out", "of the transfer", "Does not give feedback"], boxed=True, h=123)
    card(k, 668, 1332, 295, 276, 2, "Transfer", "v2", img=T("/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/transfer_v2_linear.png"), capt="Transfer v2: linear (CAD, top view)")
    body(k, 668, 1615, 296, 110, "The v2 transfer is **linear**. The POLLEN travel in a straight line from the nose intake to the shooter, on belt and wheel rollers.")
    # column 4
    body(k, 989, 592, 296, 380, "Four **beam-break switches** count the balls from 0 to 4. We detect a **jam** from the intake and transfer motor speed, and **EJECT** reverses the path. The modes are IDLE, COLLECT, EJECT and SHOOT. " + dummy(26))
    procon(k, 989, 968, 296, "Cons", ["More complex design"], h=50)
    procon(k, 989, 1028, 296, "Pros", ["Exact ball count", "Jams are detected", "Feedback through LEDs"], boxed=True, h=112)
    h1(k, 989, 1149, 296, "Flower ramp", pt=17.5)
    body(k, 989, 1195, 296, 215, "One servo swings the ramp **32 degrees** down to the tiles, about 12 in from the FLOWER. The ramp and the intake **take turns** in software, so they never use the same space.")
    k.image(T("/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/flower_v2_cad.png"), 989, 1423, 296, 142, fit="contain")
    cap(k, 989, 1573, 296, "FLOWER v2")
    k.image(T("/Users/sumeetsethi/FTC-Portfolio-2026/images/cad-renders/flower_v1_old_cad.png"), 989, 1596, 296, 118, fit="contain")
    cap(k, 989, 1716, 296, "FLOWER v1: the old rack and ramp")
