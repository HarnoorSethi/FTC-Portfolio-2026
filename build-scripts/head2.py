from pf import *
import os
A = '/tmp/work/assets/'
NAVY, BLUE, ORANGE, HONEY, CREAM, INK, GRAY, LG, SKY = "1B3F6B", "2B6AA6", "2B6AA6", "FFC53D", "EAF4FC", "1D2433", "5E6B7D", "DDE6EE", "CFEAFB"
PH = "F7941D"  # placeholder colour (intentional "ADD DATA" boxes)
AW = dict(INSPIRE=("2B6AA6", "FFFFFF"), THINK=("F2D600", "1D2433"), DESIGN=("E04848", "FFFFFF"), INNOVATE=("2EB04F", "FFFFFF"), CONTROL=("F26B21", "FFFFFF"),
          CONNECT=("7B5EC6", "FFFFFF"), REACH=("D63CA6", "FFFFFF"), SUSTAIN=("1B9AAA", "FFFFFF"))
SEC = dict(team="3FA9E0", plan="1FA060", out="7B5EC6", eng="2B6AA6")
ACCENT = dict(cover="2B6AA6", p1="3FA9E0", p2="3FA9E0", p3="1FA060", p4="1FA060", p5="1FA060", p6="D63CA6", p7="D63CA6", p8="D63CA6",
              p9="2B6AA6", p10="2B6AA6", p11="2B6AA6", p12="E04848", p13="E04848", p14="E04848", p15="E04848")
TEAMLINE = "CHEESY CHIPS 23222  ·  BIOBUZZ 2026-27 ENGINEERING PORTFOLIO  ·  FIRST TECH CHALLENGE"

D = Deck()


def chip(p, x, y, text, color, w=None, h=0.19, size=6.5, tc="FFFFFF"):
    w = w or (0.12 + 0.062 * len(text))
    p.text(x, y, w, h, text, size=size, color=tc, head=True, align="c", anchor="m", fill=color, r=h / 2, margin=(0.02, 0, 0.02, 0))
    return w


def hchip(p, x, y, name):
    """ByteForce-style pill tag in the page header"""
    col, tc = AW[name.upper()]
    w = 0.3 + 0.075 * len(name)
    p.rect(x, y, w, 0.24, fill=col, line=INK, lw=1.0, r=0.12)
    p.text(x, y, w, 0.24, name.lower(), size=8, color=tc, bold=True, align="c", anchor="m", margin=(0, 0, 0, 0))
    return w + 0.1


def chrome(p, n, title, sec, awards, secname):
    acc = SEC[sec]
    p.rect(0.25, 0.13, 0.52, 0.52, fill=BLUE, shape=MSO_SHAPE.OVAL)
    p.text(0.25, 0.13, 0.52, 0.52, "CC", size=13, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
    tags = ["inspire"] + [a.lower() for a in awards if a.lower() != "inspire"]
    wtot = sum(0.3 + 0.075 * len(t) + 0.1 for t in tags) - 0.1
    tsz = min(19, (8.25 - wtot - 0.95) * 72 / (0.6 * len(title)))
    p.text(0.85, 0.06, 8.25 - wtot - 0.9, 0.46, title, size=tsz, color=BLUE, head=True, anchor="m", margin=(0, 0, 0, 0))
    p.text(0.86, 0.5, 3.6, 0.2, [dict(text="Cheesy Chips **23222**  ·  BIOBUZZ 2026-2027")], size=7.5, color=GRAY, anchor="m", margin=(0, 0, 0, 0))
    tags = ["inspire"] + [a.lower() for a in awards if a.lower() != "inspire"]
    wtot = sum(0.3 + 0.075 * len(t) + 0.1 for t in tags) - 0.1
    x = 8.25 - wtot
    for t in tags:
        x += hchip(p, x, 0.24, t)
    p.rect(0, 0.76, 8.5, 0.02, fill=INK)
    p.rect(0, 0.78, 8.5, 0.035, fill=acc)
    p.line(0.4, 10.62, 8.1, 10.62, color=INK, w=0.75)
    p.rect(0.4, 10.68, 0.34, 0.34, fill=INK, shape=MSO_SHAPE.OVAL)
    p.text(0.4, 10.68, 0.34, 0.34, str(n), size=9, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
    p.text(0.85, 10.68, 7.2, 0.34, TEAMLINE, size=6, color=GRAY, anchor="m")


def h2(p, x, y, w, text, color=None, size=12):
    color = color or BLUE
    p.rect(x, y + 0.03, 0.07, 0.2, fill=ORANGE, r=0.03)
    p.text(x + 0.13, y - 0.03, w - 0.13, 0.32, text, size=size, color=color, bold=True, anchor="m", margin=(0.02, 0, 0, 0))


def card(p, x, y, w, h, fill="FFFFFF", line=LG, r=0.1, lw=0.75):
    p.rect(x, y, w, h, fill=fill, line=line, lw=lw, r=r)


def stat(p, x, y, w, big, small, color=BLUE, h=0.78):
    p.rect(x, y, w, h, fill="FFFFFF", line=LG, r=0.08)
    p.rect(x, y + 0.1, 0.05, h - 0.2, fill=color)
    p.text(x + 0.1, y + 0.04, w - 0.14, h * 0.5, big, size=17, color=color, head=True, anchor="m")
    p.text(x + 0.1, y + h * 0.5, w - 0.14, h * 0.48, small, size=6.8, color=GRAY, anchor="t", gap=0)


def slot(p, x, y, w, h, label, kind="PHOTO"):
    """marked photo slot the team fills with a real photo"""
    p.rect(x, y, w, h, fill="FFF6E0", line=PH, lw=1.0, r=0.08, dash=True)
    p.text(x, y, w, h, [kind, dict(text=label, size=6.5, head=False, bold=False, color=GRAY)], size=8.5, color=PH, head=True, align="c", anchor="m", gap=1)


def note(p, x, y, w, h, text):
    """marked data-needed box"""
    p.text(x, y, w, h, [dict(text="ADD DATA", head=True, size=6.5, color=PH), dict(text=text, size=6.8, color=GRAY)],
           fill="FFF6E0", line=PH, lw=1.0, r=0.06, anchor="m", align="c", gap=1)


def flow(p, x, y, w, steps, h=0.62, colors=None):
    """horizontal hex-arrow flow: steps=[(title, body)]"""
    n = len(steps)
    cw = w / n
    for i, (t, b) in enumerate(steps):
        c = (colors or [BLUE] * n)[i]
        p.hexa(x + i * cw, y, cw - 0.04, 0.4, fill=c)
        p.text(x + i * cw, y, cw - 0.04, 0.4, t, size=7.2, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.14, 0, 0.14, 0))
        p.text(x + i * cw + 0.02, y + 0.44, cw - 0.1, h, b, size=6.8, color=INK, align="c")


CONTENTS = [
    ("Think", [("Our journey & season", 1), ("Meet the team", 2)]),
    ("Sustain & Connect", [("Team plan, tracking & risk", 3), ("People, mentors & knowledge", 4), ("Business & finance", 5)]),
    ("Reach & Connect", [("Outreach: impact & strategy", 6), ("Teams we start & mentor", 7), ("Events, partners & next", 8)]),
    ("Think & Design", [("Game analysis & strategy", 9), ("Design process & lessons", 10), ("Robot overview", 11)]),
    ("Innovate & Control", [("Shooter & hood", 12), ("Turret, intake & FLOWER", 13), ("Software & controls", 14), ("Simulation & validation", 15)]),
]


# =========================================================== COVER
def cover():
    p = D.page(name="cover")
    p.rect(0, 0, 8.5, 1.0, fill=BLUE)
    p.rect(0.3, 0.2, 1.2, 0.6, fill="FFFFFF", r=0.1)
    p.image(A + 'bellarmine_blue.png', 0.36, 0.23, 1.08, 0.54, fit='contain')
    p.text(1.7, 0.18, 2.4, 0.64, [dict(text="FIRST® TECH CHALLENGE", head=True, size=10), dict(text="BIOBUZZ presented by RTX", size=8)], color="FFFFFF", anchor="m", gap=1)
    p.rect(3.85, 0.1, 0.8, 0.8, fill=NAVY, line="FFFFFF", lw=2, shape=MSO_SHAPE.OVAL)
    p.text(3.85, 0.1, 0.8, 0.8, "CC", size=22, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
    p.text(4.9, 0.18, 1.9, 0.64, [dict(text="BELLARMINE", head=True, size=10), dict(text="ROBOTICS", size=8)], color="FFFFFF", anchor="m", align="r", gap=1)
    p.rect(6.95, 0.2, 1.25, 0.6, fill="FFFFFF", r=0.1)
    p.image(A + 'biobuzz.png', 7.0, 0.23, 1.15, 0.54, fit='contain')
    p.text(0.35, 1.15, 7.8, 0.85, "Engineering Portfolio", size=40, color=BLUE, head=True, anchor="m", margin=(0, 0, 0, 0))
    p.text(0.35, 1.95, 5.6, 0.75, "Cheesy Chips#23222", size=34, color=BLUE, head=True, anchor="m", margin=(0, 0, 0, 0))
    p.text(5.9, 2.0, 2.3, 0.7, ["2026 – 2027", dict(text="Season", size=14)], size=16, color=INK, head=True, align="c", anchor="m", gap=0)
    tiles = [('cover_hero.png', None), ('ev_demo.png', 1), ('side.png', None),
             ('ev_kids.png', 1), ('robot_explode.png', None), ('ev_lib.png', 1),
             ('top.png', None), ('ev_open.png', 1), ('deployed.png', None)]
    tw, th, gap = 1.68, 2.2, 0.1
    for i, (im, ph) in enumerate(tiles):
        x = 0.35 + (i % 3) * (tw + gap)
        y = 2.95 + (i // 3) * (th + gap)
        p.image(A + im, x, y, tw, th, fit='cover', r=0.16)
    # contents panel
    px, py, pw, ph_ = 5.9, 2.95, 2.25, 7.4
    p.rect(px, py, pw, ph_, fill=BLUE)
    p.text(px + 0.12, py + 0.08, pw - 0.2, 0.4, "Content", size=18, color="FFFFFF", bold=True, anchor="m")
    y = py + 0.62
    for sec, items in CONTENTS:
        p.text(px + 0.12, y, 1.7, 0.22, sec, size=8.2, color="FFFFFF", bold=True, anchor="m", margin=(0, 0, 0, 0))
        p.text(px + pw - 0.5, y, 0.4, 0.22, "p.%d" % items[0][1], size=8, color="FFFFFF", bold=True, align="r", anchor="m", margin=(0, 0, 0, 0))
        y += 0.24
        for t, pg in items:
            p.text(px + 0.12, y, 1.75, 0.2, "%d  %s" % (pg, t), size=7, color="E8F2FB", anchor="m", margin=(0, 0, 0, 0))
            p.text(px + pw - 0.5, y, 0.4, 0.2, "p.%d" % pg, size=7, color="E8F2FB", align="r", anchor="m", margin=(0, 0, 0, 0))
            y += 0.215
        y += 0.17
    p.text(0.35, 10.45, 5.4, 0.4, "Robot “Team A 2027”, rendered from our Onshape CAD in our BIOBUZZ simulator", size=7, color=GRAY, anchor="m", margin=(0, 0, 0, 0))
    p.text(0.35, 10.7, 7.8, 0.25, "Bellarmine College Preparatory · San José, California · sister team 23224 Cheesy Bytes · mentored rookie teams 23229 and 23230", size=7, color=GRAY, anchor="m", margin=(0, 0, 0, 0))


# =========================================================== 1 JOURNEY
def p1():
    p = D.page(name="p1")
    chrome(p, 1, "Our Journey & Season", "team", ["THINK"], "Start here")
    p.rect(0, 0.815, 2.85, 9.8, fill=SKY)
    p.text(0.3, 0.95, 2.3, 0.4, "We are", size=15, color=INK, anchor="m", margin=(0, 0, 0, 0))
    p.text(0.3, 1.3, 2.5, 0.7, "Cheesy Chips!", size=22, color=BLUE, head=True, anchor="m", gap=0, ls=0.9)
    p.line(0.3, 2.2, 2.6, 2.2, color=BLUE, w=0.75, dash=True)
    data = [("11", "**students** on the team", BLUE), ("4", "**teacher, alumni & program mentors**", BLUE), ("6+", "**weekly mentoring sessions** logged at CHA this fall", "D63CA6"),
            ("1000+", "**people reached** in person, 2025-26", "D63CA6"), ("300+", "**outreach hours**, 2025-26", "D63CA6")]
    y = 2.35
    for big, small, c in data:
        p.text(0.3, y, 1.1, 0.5, big, size=20, color=c, head=True, anchor="m", margin=(0, 0, 0, 0))
        p.text(1.35, y, 1.4, 0.5, small, size=7, color=INK, anchor="m", margin=(0, 0, 0, 0))
        y += 0.56
    p.line(0.3, y + 0.05, 2.6, y + 0.05, color=BLUE, w=0.75, dash=True)
    p.text(0.3, y + 0.12, 2.4, 0.3, "Start with these five pages", size=10, color=BLUE, bold=True, anchor="m", margin=(0, 0, 0, 0))
    cards = [(9, "The game math", "**97% of our points are TIPs**, so everything is sized for a TIP every ~4 s", ORANGE),
             (12, "The aim math", "A **75° hood** drops the ball in at a **68° descent**; one flywheel band covers 24-96 in", "E04848"),
             (13, "The controller", "A **cascade turret controller** with feedforward leads a moving target", "F26B21"),
             (7, "Teams we start", "**CHA** meets **weekly**; Code Crackers, Graham FLL, two Bellarmine rookie teams", "D63CA6"),
             (15, "The simulator", "**BiobuzzSim** from our CAD: ~30,000 training matches before we cut parts", "7B5EC6")]
    y += 0.5
    for pg, t, d, c in cards:
        p.rect(0.22, y, 2.45, 0.9, fill="FFFFFF", line=LG, r=0.08)
        p.hexa(0.3, y + 0.1, 0.46, 0.38, fill=c)
        p.text(0.3, y + 0.1, 0.46, 0.38, str(pg), size=10, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
        p.text(0.82, y + 0.08, 1.8, 0.42, t, size=8, color=c, head=True, anchor="m", margin=(0.02, 0, 0, 0))
        p.text(0.28, y + 0.5, 2.35, 0.4, d, size=6.5, color=INK, margin=(0.02, 0, 0, 0))
        y += 0.96
    # right column
    X, W = 3.05, 5.05
    p.text(X, 0.95, W, 0.4, "Our Journey", size=17, color=INK, anchor="m", align="c")
    p.text(X, 1.4, W, 1.5,
           ["**Welcome.** Cheesy Chips is a veteran Bellarmine team that **designs its robot in CAD, proves it in a physics simulator** of the BIOBUZZ field, then **tunes it on the robot**.",
            "Team 23222 was founded in the 2023-24 season inside **Bellarmine Robotics** at Bellarmine College Preparatory in San José. We **assist** sister team 23224 Cheesy Bytes and **mentor** rookie teams 23229 Cheesy Strings and 23230 Cheesy Wheels.",
            "We put as much effort into **growing FIRST** (starting teams, mentoring every week, teaching at libraries and museums) as into winning matches."],
           size=8.2, color=INK, gap=4)
    p.line(X, 3.05, X + W, 3.05, color=BLUE, w=0.75, dash=True)
    p.text(X, 3.15, W, 0.36, "Summary", size=15, color=INK, anchor="m")
    p.text(X, 3.55, W, 1.55,
           ["BIOBUZZ rewards one thing above all: **tipping the HIVE**. In our best simulated match **97% of the points are TIPs**, so every design choice is judged by whether it puts more POLLEN in the up CELL, faster, even when defended (p9).",
            "The robot answers with a **turret that leads a moving target**, a **hood-driven high lob** and a single nose intake with an exact 4-ball count (p11-13). The simulator, built from our own CAD, let us test those choices **30,000 times before cutting metal** (p15).",
            "Our work is written down (architecture doc, UML, tuning checklists) so the **knowledge outlives the seniors** (p4)."],
           size=8.2, color=INK, gap=4)
    p.line(X, 5.3, X + W, 5.3, color=BLUE, w=0.75, dash=True)
    p.text(X, 5.4, W, 0.4, "Objectives", size=17, color=INK, anchor="m", align="c")
    obj = [("1", "Win the hive", "Build a **reliable robot** that scores a TIP about every 4 seconds, with numbers and a simulator behind each decision."),
           ("2", "Grow our team", "**Keep and train every member**: open builds, subteam training, rookies leading their own FTC teams, written knowledge (p3-4)."),
           ("3", "Bring STEM to the community", "**Start and mentor teams**, show up weekly, and share what we know with every team that asks (p6-8).")]
    y = 5.9
    for n, t, b in obj:
        p.text(X, y, 0.4, 0.6, n, size=30, color=ORANGE, anchor="t", margin=(0, 0, 0, 0))
        p.text(X + 0.35, y + 0.02, W - 0.35, 0.25, t, size=11, color=BLUE, anchor="m", margin=(0, 0, 0, 0))
        p.text(X + 0.35, y + 0.28, W - 0.35, 0.52, b, size=8, color=INK, margin=(0, 0, 0, 0))
        y += 0.85
    p.line(X, 8.5, X + W, 8.5, color=BLUE, w=0.75, dash=True)
    p.text(X, 8.58, W, 0.3, "How we work, in one picture", size=11, color=BLUE, bold=True, anchor="m", margin=(0, 0, 0, 0))
    flow(p, X, 8.92, W, [("CAD", "One **Onshape** model drives robot and sim"), ("SIMULATE", "**30,000+** AI matches show what scores"),
                         ("BUILD & TUNE", "**Tuner OpModes** and a to-do list"), ("SHARE", "Docs and **weekly mentoring**")],
         colors=["7B5EC6", "E04848", BLUE, "D63CA6"], h=0.55)
    p.text(X, 9.9, W, 0.65, "**Gracious Professionalism® is how we compete.** We share our documentation, templates and tuning notes with the teams we mentor and treat every event as a chance to bring someone new into FIRST.",
           size=7.4, color=INK, fill=CREAM, line=ORANGE, r=0.08, margin=(0.12, 0.04, 0.12, 0.04), anchor="m")


