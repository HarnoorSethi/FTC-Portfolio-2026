from bfkit import *
_dummy = dummy


def dummy(n):
    return _dummy(n).replace(",.", ".")

INK = "231F20"
GREYT = "BDBBBC"
BLUEP = "4889C8"
CHIPS15 = [("inspire", "38BFF2", "231F20"), ("think", "E9D909", "231F20"), ("design", "F14B28", "231F20")]
CHIPS16 = [("inspire", "38BFF2", "231F20"), ("control", "EC192D", "231F20")]
BP = 8.2   # body pt


def body(k, x, y, w, h, t, color=INK, pt=BP, align="l", ls=0.98, **kw):
    return k.text(x, y, w, h, t, pt=pt, color=color, align=align, ls=ls, gap=0, **kw)


def sub(k, x, y, w, t, pt=17, color=INK, h=50):
    k.text(x, y, w, h, t, pt=pt, color=color, anchor="m")


def numitem(k, x, y, w, n, title, text, h, color=INK, tcolor=None, bcolor=None, npt=26, tpt=13, th=44, bpt=BP, tx=40):
    tcolor = tcolor or color
    k.text(x, y - 6, 40, 80, str(n), pt=npt, color=tcolor, anchor="t")
    k.text(x + tx, y + 2, w - tx, th, title, pt=tpt, color=tcolor, anchor="m")
    body(k, x, y + th + 10, w, h - th - 10, text, color=bcolor or color, pt=bpt)


def caption(k, x, y, w, t, pt=7.4, color=INK):
    k.text(x, y, w, 26, t, pt=pt, color=color, align="c", anchor="m")


# ---------------------------------------------------------------- page 15
def field_diagram(k):
    # outer frame and tiles (6 x 6 checker), like the reference field
    fx, fy, fw, fh = 688, 1128, 592, 590
    k.rect(fx - 8, fy - 8, fw + 16, fh + 16, fill="D7DCE0")
    k.rect(fx, fy, fw, fh, fill="A9ACAA")
    tw, th = fw / 6.0, fh / 6.0
    for r in range(6):
        for c in range(6):
            if (r + c) % 2 == 0:
                k.rect(fx + c * tw, fy + r * th, tw, th, fill="555758")
    for i in range(1, 6):
        k.line(fx + i * tw, fy, fx + i * tw, fy + fh, color="8A8D8C", w=0.6, dash=True)
        k.line(fx, fy + i * th, fx + fw, fy + i * th, color="8A8D8C", w=0.6, dash=True)
    # two stations at the top (black trapezoids with white lines)
    for sx in (780, 1080):
        k.poly([(sx, 1076), (sx + 108, 1076), (sx + 99, 1170), (sx + 9, 1170)], fill="231F20")
        for j in range(4):
            k.line(sx + 12, 1098 + j * 15, sx + 96, 1098 + j * 15, color="FFFFFF", w=1.6)
        for j in range(3):
            k.rect(sx + 22 + j * 26, 1156, 12, 9, fill="FFFFFF")
    # loading zones (red top-right, blue bottom-left) and start lines
    k.rect(fx + 4 * tw, fy + 3, 2 * tw - 4, 6, fill="E8364F")
    k.rect(fx + 3, fy + 3, 2 * tw, 6, fill="4B4CCB")
    k.line(fx + tw * 2, fy + th * 4, fx + tw * 2, fy + th * 5.4, color="4B4CCB", w=2.2)
    k.line(fx + tw * 4, fy + th * 2.2, fx + tw * 4, fy + th * 3.7, color="E8364F", w=2.2)
    k.line(fx + tw * 4, fy + th * 4.2, fx + tw * 4, fy + th * 5.4, color="E8364F", w=2.2)
    # four HIVEs in the centre (two red, two blue), CELLs shown as light baskets
    cx, cy = fx + fw / 2, fy + fh / 2
    for dx, dy, col in ((-70, -70, "E8364F"), (-70, 40, "E8364F"), (20, -80, "4B4CCB"), (20, 30, "4B4CCB")):
        k.rect(cx + dx, cy + dy - 8, 84, 70, fill="EDEFF0", line=col, lw=2.2, r=8)
    k.rect(cx - 20, cy - 8, 74, 12, fill="231F20")
    # pollen dots
    for (px, py) in ((fx + 505, fy + 520), (fx + 540, fy + 535), (fx + 470, fy + 545), (fx + 60, fy + 70), (fx + 90, fy + 100)):
        k.oval(px - 9, py - 9, 18, 18, fill="F5C400", line="B38F00", lw=0.6)
    # marker numbers with small shapes (white bold)
    marks = [(1, fx + 408, fy + 285, 1), (2, fx + 400, fy + 120, 0), (3, fx + 290, fy + 175, 0), (4, fx + 480, fy + 300, 0), (5, fx + 520, fy + 420, 0)]
    for (n, mx, my, _) in marks:
        k.text(mx - 22, my - 26, 44, 52, str(n), pt=17, color="FFFFFF", head=True, align="c", anchor="m")
    k.poly([(fx + 330, fy + 275), (fx + 372, fy + 262), (fx + 350, fy + 292)], fill="C21F2B")


def page_15(D):
    p = D.page(name="p15")
    k = K(p)
    k.header(15, CHIPS15)
    # blue strategy panel
    k.rect(656, 99, 654, 1650, fill=BLUEP, r=22)
    k.rect(656, 99, 654, 80, fill=BLUEP)
    k.rect(656, 1690, 80, 59, fill=BLUEP)
    # titles
    k.text(28, 100, 420, 100, "The Game", pt=31, color=INK, bold=True, anchor="m")
    k.oval(440, 124, 58, 62, fill="FBF9D9", line="E9D909", lw=1.2)
    k.text(440, 124, 58, 62, [dict(text="BIOBUZZ", bold=True, size=5 * FONT), dict(text="2026-27", size=4.4 * FONT)], align="c", anchor="m", gap=0, color=INK)
    k.text(668, 100, 600, 100, "Strategy", pt=31, color="FFFFFF", bold=True, anchor="m")
    # left column 1
    sub(k, 28, 222, 290, "BIOBUZZ")
    body(k, 25, 270, 282, 280,
         "Two alliances of two robots launch yellow **POLLEN** into the up **CELL** of their **HIVE**. The HIVE is a rocking structure with a basket at each end. "
         "When enough weight sits in the up CELL, the HIVE **tips**. The other CELL swings up and the alliance scores **20 points**. "
         "The match has a 30 second autonomous, a short transition and a 2 minute TeleOp. A robot holds at most 4 POLLEN.")
    # scoring card (in the slot where the reference has the robot picture)
    k.rect(25, 575, 297, 500, fill="F2F2F2", r=14)
    k.text(25, 583, 297, 40, "Scoring", pt=13, color=INK, align="c", anchor="m")
    rows = [("LEAVE", "3", "-"), ("PARK in loading zone", "5", "5"), ("HIVE TIP", "20", "20"), ("POLLEN in up CELL", "-", "2 each"),
            ("Bottom NECTAR bonus", "-", "5"), ("POLLEN in a FLOWER", "-", "2 each"), ("POLLEN in a GARDEN", "-", "1 each")]
    k.text(37, 627, 150, 30, "Achievement", pt=7, color="FFFFFF", bold=True, fill="231F20", anchor="m", margin=(10, 0, 0, 0), r=6)
    k.text(190, 627, 52, 30, "Auto", pt=7, color="FFFFFF", bold=True, fill="231F20", align="c", anchor="m", r=6)
    k.text(246, 627, 64, 30, "TeleOp", pt=7, color="FFFFFF", bold=True, fill="231F20", align="c", anchor="m", r=6)
    for i, (a, b, c) in enumerate(rows):
        yy = 665 + i * 50
        hl = a.startswith("HIVE")
        k.rect(37, yy, 273, 44, fill="FBF9D9" if hl else "FFFFFF", line="D9D9D9", lw=0.6, r=6)
        k.text(37, yy, 150, 44, a, pt=6.8, color=INK, bold=hl, anchor="m", margin=(10, 0, 0, 0))
        k.text(190, yy, 52, 44, b, pt=7.6, color=INK, bold=True, align="c", anchor="m")
        k.text(246, yy, 64, 44, c, pt=7.2, color=INK, bold=True, align="c", anchor="m")
    body(k, 37, 1020, 273, 50, "Ranking points: SWARM (LEAVE and PARK), POLLINATOR 1 (4 or more TIPs) and POLLINATOR 2 (7 or more).", pt=6.6)
    caption(k, 25, 1080, 297, "Scoring summary")
    sub(k, 28, 1125, 290, "Points", pt=15)
    body(k, 25, 1175, 285, 190,
         "In our best simulated match, almost all of the points came from **TIPs**. Park and the rest were small. So every part of the robot is judged by one question: does it put more POLLEN in the up CELL, faster?", pt=8.2)
    # left column 2
    body(k, 322, 215, 321, 110, "The HIVE has a pivot and two CELLs. One shot cannot tip it, so the robot has to **keep a steady rate** of launches into the up CELL.", pt=8.4)
    k.image(A + "hive_before.png", 345, 335, 298, 170, fit="cover", r=10)
    caption(k, 345, 508, 298, "1. Launch into the up CELL")
    sub(k, 352, 540, 290, "How a TIP works", pt=15)
    body(k, 322, 585, 321, 250,
         "In our model, **8 POLLEN** in the up CELL tip it. The manual gives no ball count, so this is our own CAD number. The weight turns the arm. In our simulator the swing takes **4.5 seconds**. "
         "Then the other CELL is up, so the target has **moved**. We must aim again right away.", pt=8.4)
    k.image(A + "hive_mid.png", 340, 796, 303, 258, fit="cover", r=10)
    caption(k, 340, 1057, 303, "2. The weight swings the arm")
    k.image(A + "hive_after.png", 340, 1096, 303, 258, fit="cover", r=10)
    caption(k, 340, 1357, 303, "3. TIP scored, the other CELL is up")
    # bottom-left bars chart (simulation)
    k.text(25, 1400, 297, 34, "Simulated best match, points", pt=8, color=INK, anchor="m", bold=True)
    bars = [("TIPs", 530, "about 530", "F7941D"), ("PARK", 5, "5", "4889C8"), ("Other", 10, "about 10", "8C8C8C")]
    for i, (a, v, t, c) in enumerate(bars):
        yy = 1445 + i * 55
        k.text(25, yy, 70, 40, a, pt=8, color=INK, anchor="m")
        bw = max(6, 125 * v / 530)
        k.rect(98, yy + 6, bw, 28, fill=c, r=4)
        k.text(98 + bw + 6, yy, 120, 40, t, pt=7.4, color=INK, anchor="m")
    k.line(96, 1440, 96, 1610, color=INK, w=1.2)
    k.line(96, 1610, 310, 1610, color=INK, w=1.2)
    k.text(25, 1640, 297, 30, "Simulation result, not a robot result", pt=6.8, color=INK, anchor="m")
    k.line(330, 1380, 330, 1735, color="CFCFCF", w=0.8, dash=True)
    # hive-frame bottom of col 2: model line
    body(k, 345, 1395, 298, 170,
         "Our AI driver in the simulator got about 1.9 shots every second and about 4.3 seconds between TIPs. A TIP needed about 8.2 shots. "
         "We will measure the real numbers on a field and put them here.", pt=8.4)
    k.photo_ph(345, 1585, 298, 150, "robot launching into the up CELL")
    # ---- strategy panel text
    W = "FFFFFF"
    body(k, 668, 215, 300, 200,
         "We use one idea for all of our choices. We want **more POLLEN in the up CELL**, faster than anyone else. We pick our shots from where the robot is, and we keep **aiming while we drive**. "
         "Our partner can play without waiting for us.", color=W, pt=8.4)
    sub(k, 672, 425, 290, "Autonomy", pt=16, color=W)
    numitem(k, 672, 490, 292, 1, "Safe Autonomous",
            "We want **LEAVE** and **PARK** every match. A state machine does the preload volley, then pickups, then a last shot, then parks. A clock parks us with 3 s left.", 190, color=W)
    numitem(k, 672, 665, 292, 2, "Preload Volley",
            "We shoot the preload first. Timings are still being tuned on the robot.", 135, color=W)
    body(k, 668, 828, 300, 170, dummy(34), color=W, pt=8.4)
    sub(k, 995, 222, 290, "TeleOP", pt=17, color=W)
    items = [("Throughput", "We want a high, steady **shot rate**. The nose intake takes **one path** and counts to 4 balls.", 270),
             ("Aim Anywhere", "The shot must land in a **20 inch opening** from 24 to 96 inches, even when tilted.", 440),
             ("Keep Moving", "The turret keeps aiming while we drive or get pushed. We use **feedforward** from the chassis motion.", 580),
             ("Pick the CELL", "The HIVE flips, so the target moves. We choose the CELL on **our half** of the field.", 775),
             ("Park", "In the last seconds we go to our loading zone to **PARK** for 5 points.", 927)]
    ys = [297, 447, 577, 772, 922]
    for i, ((t, b, _), y) in enumerate(zip(items, ys)):
        hh = 140 if i < 4 else 120
        numitem(k, 995, y, 292, i + 1, t, b, hh, color=W)
    # the BIOBUZZ field as BiobuzzSim shows it from above (the old drawing was another game's field)
    k.image('/Users/sumeetsethi/FTC-Portfolio-2026/images/photos/sim_field_topview.png', 668, 1066, 617, 616, fit="cover", r=14)
    k.text(668, 1690, 617, 50, "The BIOBUZZ field in BiobuzzSim, seen from above: the HIVE with its red and blue CELLs in the middle and POLLEN on the floor (simulation).", pt=7, color=W, align="c", anchor="m", gap=0)
    return p


# ---------------------------------------------------------------- page 16
def circ_num(k, cx, cy, n, d=44, color="2C6E9E"):
    k.oval(cx - d / 2, cy - d / 2, d, d, line=color, lw=1.8)
    k.text(cx - d / 2, cy - d / 2, d, d, str(n), pt=14, color=color, align="c", anchor="m")


def axes(k, x, y, w, h, lab_v="v", lab_t="t"):
    k.line(x, y, x, y + h, color=INK, w=1.8)
    k.line(x, y + h, x + w, y + h, color=INK, w=1.8)
    k.text(x - 14, y - 8, 14, 20, lab_v, pt=6.2, color=INK, align="r")
    k.text(x + w + 4, y + h - 10, 14, 20, lab_t, pt=6.2, color=INK)


def box_port(k, x, y, w, h, fill="FFFFFF"):
    k.rect(x, y, w, h, fill=fill, line="9A9A9A", lw=0.8, r=7)


def port(k, x, y):
    k.oval(x - 5, y - 5, 10, 10, fill="FFFFFF", line=INK, lw=1.6)


def page_16(D):
    p = D.page(name="p16")
    k = K(p)
    k.header(16, CHIPS16)
    # title with code icon
    k.oval(45, 115, 105, 105, fill="FFFFFF", line="D5D5D5", lw=0.8)
    k.text(45, 115, 105, 105, "</>", pt=26, color=INK, head=True, align="c", anchor="m")
    k.text(170, 98, 700, 90, "Software", pt=31, color=INK, bold=True, anchor="m")
    k.text(170, 186, 520, 42, "About 99 Java files, --- commits, a shot planner and our own simulator.", pt=8.4, color=INK, ls=0.93, gap=0)
    # --- left column
    sub(k, 30, 232, 300, "Objectives", pt=17)
    numitem(k, 25, 285, 403, 1, "Fast shots", "To keep a steady **shot rate**, the robot needs to know how many balls it holds and when it is ready to fire. " + dummy(4), 135, tx=40, tpt=13, th=44)
    numitem(k, 25, 420, 403, 2, "Aim anywhere", "**Turret, hood and speed** are picked for any spot, even while we move. " + dummy(5), 125, tx=40, tpt=13, th=44)
    numitem(k, 25, 550, 403, 3, "Know our position", "A good **localization** system, so we score from the same spots all match. " + dummy(5), 125, tx=40, tpt=13, th=44)
    sub(k, 30, 685, 380, "Autonomous", pt=16)
    body(k, 25, 737, 403, 190,
         "Our autonomous is a **state machine**: preload shoot, pickups, shoot, park. A clock override parks with a 3 second reserve, so we get **LEAVE 3 and PARK 5** every time. The pose is **handed to TeleOp** after the match, and marked stale after 5 minutes. " + dummy(16))
    sub(k, 30, 925, 400, "Sensors", pt=16)
    body(k, 25, 978, 403, 250,
         "We use the **OctoQuad** to read two dead-wheel pods in one bulk read. Four **switches** count balls in the robot, so it never holds more than 4. "
         "A drop in motor encoder speed shows a **jam**, and the command clears it. These are small checks, but they keep the robot from breaking a match. " + dummy(22))
    # left bottom: sim path + flow boxes
    k.image(A + "sim_path.png", 45, 1262, 345, 300, fit="cover", r=8, border="C8C8C8")
    caption(k, 25, 1568, 403, "An AI driver's path in BiobuzzSim (simulation)", pt=7.4)
    box_port(k, 60, 1600, 160, 64)
    k.text(60, 1600, 160, 64, [dict(text="? Ball count 4", size=7.6 * FONT, bold=True), dict(text="4 switches say full", size=5.2 * FONT)], anchor="m", margin=(14, 0, 0, 0), gap=0, color=INK)
    box_port(k, 180, 1650, 150, 64)
    k.text(180, 1650, 150, 64, [dict(text="? Jam", size=7.6 * FONT, bold=True), dict(text="encoder speed drops", size=5.2 * FONT)], anchor="m", margin=(14, 0, 0, 0), gap=0, color=INK)
    box_port(k, 285, 1600, 120, 64)
    k.text(285, 1600, 120, 64, [dict(text="Reverse", size=7.6 * FONT, bold=True), dict(text="clears it and", size=5.2 * FONT), dict(text="tries again", size=5.2 * FONT)], anchor="m", margin=(12, 0, 0, 0), gap=0, color=INK)
    port(k, 220, 1625); port(k, 285, 1640)
    k.curve([(220, 1625), (250, 1610), (270, 1612), (285, 1640)], color=INK, w=1.0)
    k.text(235, 1596, 40, 22, "No", pt=6.4, color=INK)
    k.text(332, 1660, 40, 22, "Yes", pt=6.4, color=INK)
    caption(k, 25, 1716, 403, "Ball logic in the intake", pt=6.8)

    # --- middle column
    sub(k, 458, 232, 300, "Teleop", pt=17)
    sub(k, 455, 275, 400, "Shot Planner", pt=13.5, h=44)
    body(k, 455, 322, 405, 245,
         "To **score on the move**, the planner moves the aim point. The **virtual goal** is the goal minus the robot's speed times the ball's flight time. "
         "It does **3 fixed-point steps** each loop, and adds a **0.08 second** latency lead. The shot table gives hood and speed. " + dummy(22))
    sub(k, 455, 570, 420, "Target Selector", pt=13.5, h=44)
    body(k, 455, 614, 405, 165,
         "The HIVE flips, so the target moves about 21 inches. We pick the CELL on **our half** of the field, with a 4 inch buffer so it does not flicker. We aim at the middle of the opening. " + dummy(8))
    sub(k, 455, 785, 420, "BiobuzzSim", pt=13.5, h=44)
    body(k, 455, 830, 405, 245,
         "We built a **simulator** from our own CAD and the rules in the manual. Two AI drivers play matches in it, so we can test ideas before we cut metal. "
         "The points below are **simulated**. They are not robot results. We will compare them with real shots on the field. " + dummy(14))
    # four small graphs: circled number at left, graph and caption in x 580..860
    gl, gr = 580, 860
    circ_num(k, 540, 1130, 1)
    res = [("No defense", 458, "2E9E5B"), ("Light", 397, "2E9E5B"), ("Medium", 385, "F79A66"), ("Lockdown", 379, "EC192D")]
    for i, (a_, v, c) in enumerate(res):
        yy = 1090 + i * 20
        k.text(gl, yy, 86, 18, a_, pt=5.8, color=INK, anchor="m", align="r")
        k.rect(gl + 94, yy + 3, 130 * v / 458, 12, fill=c)
        k.text(gl + 98 + 130 * v / 458, yy, 36, 18, str(v), pt=5.8, color=INK, anchor="m")
    caption(k, 500, 1176, 380, "AI average points by defense (simulation)", pt=6.8)
    circ_num(k, 540, 1262, 2)
    cx0 = 735
    k.line(cx0, 1226, cx0, 1296, color=INK, w=1.6)
    k.rect(cx0, 1232, 62, 18, fill="2E9E5B")
    k.text(cx0 + 68, 1230, 50, 22, "+111", pt=6.2, color=INK, anchor="m")
    k.rect(cx0 - 98, 1262, 98, 18, fill="EC192D")
    k.text(cx0 - 150, 1260, 46, 22, "-181", pt=6.2, color=INK, anchor="m", align="r")
    k.text(gl, 1298, cx0 - gl - 6, 18, "driver 250 ms late", pt=5.8, color=INK, align="r", anchor="m")
    k.text(cx0 + 6, 1298, 140, 18, "shoot on the move", pt=5.6, color=INK, anchor="m")
    caption(k, gl, 1320, gr - gl, "Points lost or gained in simulation", pt=6.8)
    circ_num(k, 540, 1392, 3)
    stg = ["CAD", "Physics", "Rules", "AI", "Design"]
    for i, s_ in enumerate(stg):
        x0 = gl + i * 56
        k.poly([(x0, 1370), (x0 + 48, 1370), (x0 + 56, 1392), (x0 + 48, 1414), (x0, 1414), (x0 + 8, 1392)], fill=["6C4BC1", "4889C8", "F79A66", "2E9E5B", "D6457A"][i])
        k.text(x0 + 6, 1370, 44, 44, s_, pt=4.8, color="FFFFFF", bold=True, align="c", anchor="m")
    caption(k, gl, 1428, gr - gl, "From CAD to design decisions", pt=6.8)
    circ_num(k, 540, 1500, 4)
    bx, by, bw_, bh_ = 585, 1470, 275, 175
    axes(k, bx, by, bw_, bh_, "", "")
    steps = [("Desk", 1630), ("Drive", 1600), ("Turret", 1570), ("Flywheel", 1540), ("Table", 1510), ("Auto", 1486)]
    for i, (s_, yy) in enumerate(steps):
        x0 = bx + 8 + i * 44
        k.line(x0, yy, x0 + 38, yy, color="2C6E9E", w=2.6)
        k.text(x0 + 2, (yy - 24) if i == 0 else (yy + 5), 80, 20, s_, pt=4.8, color=INK, align="l", anchor="t")
        if i:
            k.line(x0 - 6, steps[i - 1][1], x0, yy, color="2C6E9E", w=2.6)
    caption(k, gl, 1654, gr - gl, "Tuning order in TUNING.md", pt=6.8)

    # --- right column
    k.text(880, 112, 410, 90, "Where the robot is and where it aims", pt=15.5, color=INK, align="c", anchor="m", ls=0.95)
    body(k, 882, 208, 403, 120,
         "The robot has to know its **position** all match, so the shot planner can aim. We use **two dead-wheel pods**, read through an **OctoQuad MK2**, and the **Pedro Pathing** localizer with IMU fusion. " + dummy(3))
    numitem(k, 882, 330, 403, 1, "Pods => posX, posY", "The two **dead wheels** give the robot position in the XY system. They are read in one bulk read each loop. " + dummy(8), 155, color=INK, tcolor=GREYT, tx=42, tpt=13)
    numitem(k, 882, 520, 403, 2, "IMU => heading", "The **IMU** gives the heading. Pedro fuses it with the pods, so we know which way the turret must turn. " + dummy(8), 150, color=INK, tcolor=GREYT, tx=42, tpt=13)
    numitem(k, 882, 715, 403, 3, "Pose handoff", "At the end of autonomous the **pose is saved** and read back in TeleOp. We mark it stale after 5 minutes. " + dummy(10), 160, color=INK, tcolor=GREYT, tx=42, tpt=13)
    # re-draw bodies of the three items in INK (title grey, text ink): overlay handled by color param below
    ekf_diagram(k)
    sub(k, 882, 1262, 403, "Shoot on the Move", pt=15, h=46)
    body(k, 882, 1308, 403, 215,
         "At 30 in/s and about 1 second of flight, the ball drifts about 30 inches. That is more than the **20 inch opening**. So we shoot at the **virtual goal**, which is shifted back against our motion. "
         "The pivot speed includes the turn of the robot times its radius. " + dummy(26), ls=0.93)
    sotm_diagram(k)
    return p


def ekf_diagram(k):
    ox, oy = 880, 905
    # boxes
    box_port(k, 917, 928, 160, 100)
    box_port(k, 1127, 928, 157, 100)
    box_port(k, 1127, 1022, 157, 84)
    box_port(k, 917, 1117, 160, 110)
    box_port(k, 1127, 1117, 157, 110)
    k.text(924, 936, 150, 44, [dict(text="**1**  Clear caches", size=7.4 * FONT), dict(text="      stale reads dropped", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(924, 982, 150, 44, [dict(text="**2**  Bulk read", size=7.4 * FONT), dict(text="      one OctoQuad read", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(1141, 940, 136, 80, [dict(text="**0**  Start of loop", size=7.4 * FONT), dict(text="      Pods and IMU", size=5.2 * FONT), dict(text="      ready to read", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(1141, 1030, 136, 70, [dict(text="Telemetry", size=7.6 * FONT), dict(text="20 Hz, rate-limited", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(924, 1120, 152, 34, [dict(text="**3**  Subsystems", size=7.4 * FONT), dict(text="      READ", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(924, 1154, 152, 34, [dict(text="**4**  Commands", size=7.4 * FONT), dict(text="      EXECUTE, then WRITE", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(924, 1188, 152, 34, [dict(text="**5**  Follower", size=7.4 * FONT), dict(text="      path update", size=5.2 * FONT)], color=INK, gap=0, anchor="m")
    k.text(1141, 1122, 136, 88, [dict(text="Pods", size=7.4 * FONT), dict(text="OctoQuad", size=7.4 * FONT), dict(text="IMU", size=7.4 * FONT), dict(text="Data collectors", size=5.4 * FONT), dict(text="for localization", size=5.4 * FONT)], color=INK, gap=0, anchor="m")
    k.rect(930, 1043, 133, 52, fill="231F20", r=8)
    k.text(930, 1043, 133, 52, "Every loop, 50 Hz", pt=5.8, color="FFFFFF", align="c", anchor="m")
    k.text(917, 903, 160, 22, "Read", pt=5.8, color=INK, align="c", anchor="m")
    k.text(917, 1097, 160, 22, "Act", pt=5.8, color=INK, align="c", anchor="m")
    for (px, py) in ((1044, 928), (1140, 928), (917, 969), (1077, 975), (1077, 1128), (1127, 1088), (1077, 1148), (1077, 1215), (1127, 1215)):
        port(k, px, py)
    k.curve([(1044, 928), (1070, 915), (1110, 912), (1140, 928)], color=INK, w=0.9)
    k.curve([(1077, 975), (1100, 1010), (1112, 1050), (1077, 1128)], color=INK, w=0.9)
    k.curve([(917, 1140), (890, 1100), (890, 1010), (917, 969)], color=INK, w=0.9)
    k.curve([(1077, 1148), (1110, 1120), (1120, 1100), (1127, 1088)], color=INK, w=0.9)
    k.curve([(1127, 1215), (1100, 1222), (1090, 1220), (1077, 1215)], color=INK, w=0.9)
    caption(k, 880, 1230, 403, "Order of one control loop", pt=6.4)


def sotm_diagram(k):
    # replaces the rollback timeline: virtual goal diagram on a horizontal axis
    y0 = 1655
    k.line(895, y0, 1280, y0, color=INK, w=1.6, arrow=True)
    k.text(1244, y0 + 9, 50, 22, "field", pt=6, color=INK)
    k.rect(905, y0 - 38, 70, 38, fill="231F20", r=5)
    k.text(905, y0 - 38, 70, 38, "robot", pt=5.8, color="FFFFFF", align="c", anchor="m")
    k.line(980, y0 - 20, 1070, y0 - 20, color="2E9E5B", w=2.4, arrow=True)
    k.text(985, y0 + 9, 100, 20, "v = 30 in/s", pt=5.8, color="2E9E5B", bold=True)
    # CELL shapes: real (filled), virtual (dashed outline)
    def cell(cx, fill, line, lw, dash=False):
        k.poly([(cx - 40, y0 - 70), (cx - 40, y0 - 30), (cx + 40, y0 - 30), (cx + 40, y0 - 70), (cx + 28, y0 - 70), (cx + 28, y0 - 44), (cx - 28, y0 - 44), (cx - 28, y0 - 70)], fill=fill, line=line, lw=lw)
    cell(1235, "F5C400", INK, 1.2)
    cell(1105, None, "F7941D", 1.6)
    k.text(1190, y0 - 108, 100, 26, "real CELL", pt=6, color=INK, bold=True, align="c")
    k.text(1050, y0 - 108, 110, 26, "virtual goal", pt=6, color="F7941D", bold=True, align="c")
    k.line(1190, y0 - 52, 1152, y0 - 52, color="F7941D", w=1.3, arrow=True)
    k.line(980, y0 - 28, 1062, y0 - 48, color=INK, w=1.2, arrow=True, dash=True)
    caption(k, 880, 1712, 403, "Virtual goal for shoot on the move", pt=6.4)
