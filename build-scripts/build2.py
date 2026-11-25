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


# =========================================================== 2 TEAM
def p2():
    p = D.page(name="p2")
    chrome(p, 2, "Meet the Team", "team", ["INSPIRE", "SUSTAIN"], "Team")
    card(p, 0.4, 0.92, 7.7, 1.62)
    p.text(0.55, 0.98, 5.4, 1.52,
           ["**Team 23222, the Cheesy Chips,** was founded in the 2023-24 season inside Bellarmine Robotics. We aim to equip a community of students passionate about science and technology "
            "with the skills and initiative to become the next generation of leaders and create positive change in their fields.",
            "Together we build the robot, bring STEM to the community, and sustain the program. We **assist** sister team 23224 Cheesy Bytes and **mentor** rookie teams 23229 Cheesy Strings and 23230 Cheesy Wheels, "
            "and this season we also mentor middle-school teams outside Bellarmine (p7)."],
           size=8, color=INK, gap=4)
    p.image(A + 'bellarmine_blue.png', 6.15, 1.0, 0.72, 0.72, fit='contain')
    p.text(6.9, 1.02, 1.15, 0.7, "Bellarmine College Preparatory, est. 1851", size=7, color=GRAY, anchor="m")
    vals = [("Discovery", "6C4BC1"), ("Innovation", ORANGE), ("Impact", "D6457A"), ("Inclusion", "2E9E5B"), ("Teamwork", BLUE), ("Fun", "E0A100")]
    p.text(6.15, 1.76, 1.9, 0.18, "FIRST CORE VALUES WE WORK BY", size=6, color=GRAY, head=True, margin=(0, 0, 0, 0))
    for i, (v, c) in enumerate(vals):
        chip(p, 6.15 + (i % 3) * 0.64, 1.97 + (i // 3) * 0.24, v, c, w=0.6, h=0.2, size=5.8)
    h2(p, 0.4, 2.66, 7.7, "Students")
    st = [("harnoor", "Harnoor Sethi", "Software", "Software lead · robot code, simulator", BLUE), ("johnson", "Johnson Che", "Design", "CAD & mechanisms", ORANGE),
          ("shaurya", "Shaurya Singhal", "Team Captain", "Leads team & drives", "E0A100"), ("noah", "Noah Ballestrasse", "Manufacturing", "Machining & assembly", "2E9E5B"),
          ("matvei", "Matvei Potov", "Design", "CAD & mechanisms", ORANGE), ("michael", "Michael Ghobrial", "Outreach", "Outreach lead", "D6457A"),
          ("dylan", "Dylan Reilley-Garcia", "Media", "Photo, video, documentation", "6C4BC1"), ("morgan", "Morgan Curlee", "Design", "CAD & mechanisms", ORANGE),
          ("kevin", "Kevin Xu", "Design", "CAD & mechanisms", ORANGE), ("jake", "Jake Laponis", "Design", "CAD & mechanisms", ORANGE),
          ("rishaan", "Rishaan Saini", "Manufacturing", "Machining & assembly", "2E9E5B")]
    cw = 1.285
    for i, (k, nm, role, sub, c) in enumerate(st):
        cx = 0.4 + (i % 6) * cw
        cy = 2.98 + (i // 6) * 1.72
        p.rect(cx + 0.02, cy, cw - 0.08, 1.62, fill="FFFFFF", line=LG, r=0.08)
        p.rect(cx + 0.02, cy, cw - 0.08, 0.07, fill=c)
        p.image(A + f'p_{k}.png', cx + 0.2, cy + 0.14, 0.82, 1.0, fit='cover', r=0.07, border=c, bw=1.25)
        p.text(cx + 0.02, cy + 1.16, cw - 0.08, 0.2, nm, size=7.2, color=INK, bold=True, align="c", anchor="m", margin=(0.01, 0, 0.01, 0))
        chip(p, cx + 0.12, cy + 1.37, role, c, w=cw - 0.28, h=0.17, size=5.8)
    # 11th slot is col 5 of row 2 -> use 12th cell for subteam chart
    cx, cy = 0.4 + 5 * cw, 2.98 + 1.72
    p.rect(cx + 0.02, cy, cw - 0.08, 1.62, fill=NAVY, r=0.08)
    p.text(cx + 0.02, cy + 0.05, cw - 0.08, 1.52,
           [dict(text="11", size=26, head=True, color=HONEY), dict(text="students\n5 subteams", size=7.5, color="FFFFFF")], align="c", anchor="m", gap=0)
    h2(p, 0.4, 6.44, 7.7, "Mentors")
    mt = [("salgaonkar", "Mr. Salgaonkar", "Teacher · non-tech mentor", "Guides business, outreach & planning"),
          ("lindemann", "Mr. Lindemann", "Teacher · software mentor", "Guides software development"),
          ("lawrence", "Andrew Lawrence", "Program mentor", "Across Bellarmine Robotics"),
          ("torrance", "Andrew Torrance", "Alumni · tech mentor", "Alumni; guides technical design")]
    for i, (k, nm, role, desc) in enumerate(mt):
        mx = 0.4 + i * 1.93
        card(p, mx, 6.76, 1.85, 1.0)
        ph = A + f'p_{k}.' + ('jpeg' if k == 'lawrence' else 'png')
        p.image(ph, mx + 0.08, 6.84, 0.6, 0.8, fit='cover', r=0.06, border=BLUE, bw=1)
        p.text(mx + 0.72, 6.82, 1.1, 0.86, [dict(text=nm, bold=True, size=7.6), dict(text=role, size=6.6, color=BLUE, bold=True), dict(text=desc, size=6.4, color=GRAY)], gap=1, anchor="m")
    p.text(0.4, 7.82, 7.7, 0.62,
           "Our mentors are **teachers, alumni and volunteers**, many of them former Cheesy Chips. They **teach technical skills**, help organize events and train new members. "
           "Every season mentors **re-train all members on the “green tools”** (the safest tier) in our shop so rookies and veterans start the season on equal footing.",
           size=7.8, color=INK)
    h2(p, 0.4, 8.5, 7.7, "How the team is organized (every member has a role)")
    sub = [("Design", 5, ORANGE, "CAD, mechanisms, FEA"), ("Manufacturing", 2, "2E9E5B", "Machining, assembly"), ("Software", 1, BLUE, "Robot code, simulator, tuning"),
           ("Media", 1, "6C4BC1", "Documentation, social"), ("Outreach", 1, "D6457A", "Events, partners, mentoring"), ("Captain", 1, "E0A100", "Coordination, driving")]
    y = 8.84
    for i, (nm, n, c, d) in enumerate(sub):
        yy = y + i * 0.28
        p.text(0.4, yy, 1.0, 0.22, nm, size=7.6, color=INK, bold=True, anchor="m")
        p.rect(1.45, yy + 0.03, 0.34 * n, 0.16, fill=c, r=0.04)
        p.text(1.5 + 0.34 * n, yy, 0.3, 0.22, str(n), size=7.6, color=c, head=True, anchor="m")
        p.text(3.3, yy, 1.8, 0.22, d, size=6.8, color=GRAY, anchor="m")
    p.text(5.2, 8.82, 2.9, 1.7,
           ["**A hive, not a hero.** Every build ends with a team debrief after we clean the lab, every outreach event ends with a what-went-well / what-to-improve review (p6), "
            "and software knowledge is written down (p4, p14) so no single member is a point of failure."],
           size=8, color=INK, fill=CREAM, line=ORANGE, r=0.1, margin=(0.12, 0.08, 0.12, 0.08), anchor="m")


# =========================================================== 3 PLAN
def p3():
    p = D.page(name="p3")
    chrome(p, 3, "Team Plan, Tracking & Risk", "plan", ["SUSTAIN", "CONNECT", "THINK"], "Planning")
    h2(p, 0.4, 0.92, 7.7, "Goals → steps → how we track them")
    cols = [("GOAL", 1.7), ("STEPS WE TAKE", 3.0), ("HOW WE TRACK IT", 1.85), ("TARGET", 1.15)]
    x = 0.4
    for (c, w) in cols:
        p.text(x, 1.22, w - 0.04, 0.22, c, size=6.8, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.08, 0, 0.04, 0), r=0.04)
        x += w
    rows = [
        ("Build and keep a bigger, stronger team", "**Open Builds** on campus; applications; **tool training**; new members run their **own FTC team** in year one (23229 / 23230); leadership roles applied for, then interviewed",
         "Attendance log; sub-team check-ins every other week", "85%+ new-member retention (92% last season)"),
        ("Grow skills of every member", "**Subteam training** from leads; mentors review CAD and code; **pairing** rookies with veterans on real tasks; weekly **tuning checklists** (p14)",
         "Tune-0 to-do list OpMode marks each item DONE / STOCK / TODO; mentor reviews", "Every member owns one named deliverable"),
        ("Build a robot that wins the hive", "Read the manual & Team Updates on release; **model the game**; **sim-test before cutting parts** (p15); build, tune, log",
         "Design reviews; sim vs. robot comparisons; tuning to-do list", "Reliable TIP cycle; 7+ TIPs (POLLINATOR 2)"),
        ("Bring STEM to every age group", "**Monthly library events**, school visits, museum exhibits; **start and mentor new teams** (p7)",
         "Notion outreach calendar; debrief after every event", "Weekly mentoring; 1000+ reached (met in 2025-26)"),
        ("Share what we know", "Publish our template & docs to the teams we mentor; run hackathons; host scrimmages",
         "Teams using our setup (23230 already does, p4)", "More teams, more connections"),
    ]
    y = 1.48
    for i, (g, s, t, tg) in enumerate(rows):
        h = 0.64
        f = "FFFFFF" if i % 2 == 0 else "F4F7FC"
        p.rect(0.4, y, 7.7, h - 0.03, fill=f, line=LG, r=0.04)
        x = 0.4
        for (txt, (c, w), bold) in zip((g, s, t, tg), cols, (True, False, False, False)):
            p.text(x, y, w - 0.04, h - 0.03, txt, size=6.9 if not bold else 7.4, color=INK if bold else INK, bold=bold, anchor="m", margin=(0.08, 0.01, 0.05, 0.01))
            x += w
        y += h
    h2(p, 0.4, 4.78, 7.7, "Season timeline: what is done and what is next")
    # timeline
    months = ["SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]
    tx0, tw = 1.45, 6.65
    mw = tw / 7
    for i, m in enumerate(months):
        p.text(tx0 + i * mw, 5.08, mw - 0.03, 0.2, m, size=6.5, color="FFFFFF", head=True, fill=BLUE if i < 3 else "7F93B5", align="c", anchor="m", r=0.04)
    p.rect(tx0 + 2.33 * mw, 5.08, 0.02, 1.98, fill="D64545")
    p.text(tx0 + 2.33 * mw - 0.3, 7.08, 0.62, 0.16, "NOV 10", size=5.8, color="D64545", head=True, align="c")
    lanes = [("Game & rules", [(0, 2.0, "Reveal · manual · Team Updates 06-07", BLUE, 0)]),
             ("Simulator", [(0.35, 0.75, "Sim v1", ORANGE, 0), (1.1, 1.2, "AI drivers · pit display", ORANGE, 0), (2.33, 0.9, "Validate vs. robot", ORANGE, 1)]),
             ("Robot design", [(0.2, 1.1, "CAD · hood / turret", "2E9E5B", 0), (1.3, 1.03, "One-intake CAD", "2E9E5B", 0), (2.33, 0.9, "Iterate", "2E9E5B", 1)]),
             ("Robot code", [(0.4, 1.3, "Team A code · docs", "6C4BC1", 0), (1.7, 0.63, "Tuning", "6C4BC1", 0), (2.33, 1.6, "Autonomous · shot table · tuning", "6C4BC1", 1)]),
             ("Outreach", [(0.3, 2.03, "CHA weekly · libraries monthly · Code Crackers", "D6457A", 0), (2.33, 2.4, "Monthly events · CHA weekly continues", "D6457A", 1)]),
             ("Competition", [(3.3, 1.5, "Qualifier (date TBD)", "E0A100", 1), (5.0, 1.8, "Regional / advance", "E0A100", 1)])]
    ly = 5.34
    for (nm, bars) in lanes:
        p.text(0.4, ly, 1.0, 0.24, nm, size=7, color=INK, bold=True, anchor="m")
        p.line(tx0, ly + 0.25, 8.1, ly + 0.25, color=LG, w=0.5)
        for (st_, ln_, lab, c, plan) in bars:
            p.text(tx0 + st_ * mw, ly + 0.02, ln_ * mw - 0.03, 0.21, lab, size=5.8, color="FFFFFF" if not plan else INK, fill=c, alpha=0.45 if plan else None, anchor="m", r=0.05, margin=(0.05, 0, 0.02, 0))
        ly += 0.29
    p.text(5.0, 4.82, 3.1, 0.2, "solid = done   ·   light = planned", size=6, color=GRAY, align="r", anchor="m")
    # risk register
    h2(p, 0.4, 7.36, 7.7, "Constraints and risks we manage")
    rk = [("Small team, limited lab hours", "Simulator & desk-test tools find problems before we cut parts; sim-first design (p15)", "High"),
          ("Graduating seniors take knowledge with them", "Written architecture doc, UML, tuning checklists; rookies lead their own teams first (p4)", "High"),
          ("Rules change weekly (Team Updates)", "Rules mirrored in the sim; we re-read every Team Update and re-check the code (p9)", "Med"),
          ("Mechanism risk: hood must reach 70–85°, turret needs zeroing", "Required angles derived from CAD (p12); absolute turret encoder as a fallback (p13)", "Med"),
          ("Single point of failure in code", "Subsystems never reference each other; a written doc explains every choice (p4, p14)", "Med"),
          ("Funding variance", "Diversified sponsors + dues, reserve carried over each year (p5)", "Low")]
    y = 7.66
    for (r_, m_, lv) in rk:
        c = {"High": "D64545", "Med": ORANGE, "Low": "2E9E5B"}[lv]
        p.rect(0.4, y, 7.7, 0.4, fill="FFFFFF", line=LG, r=0.04)
        chip(p, 0.46, y + 0.1, lv.upper(), c, w=0.42, h=0.19, size=6)
        p.text(0.95, y, 2.6, 0.4, r_, size=7, color=INK, bold=True, anchor="m")
        p.text(3.55, y, 4.5, 0.4, m_, size=6.9, color=GRAY, anchor="m")
        y += 0.43
    p.text(0.4, 10.28, 7.7, 0.3, "Review rhythm: team debrief after each build day; event debrief after every outreach event; plan reviewed at the start of each month.", size=7, color=GRAY, anchor="m")
    D.pages[-1]




def flow(p, x, y, w, steps, h=0.62, colors=None):
    """horizontal hex-arrow flow: steps=[(title, body)]"""
    n = len(steps)
    cw = w / n
    for i, (t, b) in enumerate(steps):
        c = (colors or [BLUE] * n)[i]
        p.hexa(x + i * cw, y, cw - 0.04, 0.4, fill=c)
        p.text(x + i * cw, y, cw - 0.04, 0.4, t, size=7.2, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.14, 0, 0.14, 0))
        p.text(x + i * cw + 0.02, y + 0.44, cw - 0.1, h, b, size=6.8, color=INK, align="c")


# =========================================================== 4 SUSTAIN: PEOPLE
def p4():
    p = D.page(name="p4")
    chrome(p, 4, "People, Mentors & Knowledge", "plan", ["SUSTAIN", "THINK", "REACH"], "People & knowledge")
    p.text(0.4, 0.9, 7.7, 0.5, "Our robot is rebuilt every year; **our people and knowledge are what carry over.** Every part of our sustainability plan answers one question: "
           "what happens to the team when its seniors graduate?", size=8.4, color=INK)
    h2(p, 0.4, 1.46, 7.7, "Member pipeline: every member gets a real job and a path up")
    flow(p, 0.4, 1.8, 7.7, [("OPEN BUILD", "Campus-wide hands-on days for students who have never touched FTC"),
                            ("APPLY", "Application to the team; training in sub-teams before the season"),
                            ("OWN TEAM", "Rookies run their own FTC team in year one (23229, 23230)"),
                            ("VETERAN TEAM", "Join 23222 / 23224 with a full season of experience"),
                            ("LEAD & MENTOR", "Captains, leads, then alumni mentors (many now at SCU)")],
         colors=[ "2E9E5B", BLUE, ORANGE, "6C4BC1", "D6457A"])
    stat(p, 0.4, 2.98, 1.5, "92%", "member retention last season (goal 85%+)", "2E9E5B", h=0.72)
    stat(p, 2.0, 2.98, 1.5, "4 teams", "in our family: 23222 · 23224 · 23229 · 23230", BLUE, h=0.72)
    stat(p, 3.6, 2.98, 1.5, "100%", "of members trained on shop “green tools” each season", ORANGE, h=0.72)
    p.text(5.2, 2.98, 2.9, 0.72, "**Why own teams for rookies?** Rookies learn by doing real work instead of watching, and veterans can try ambitious designs without leaving anyone behind (trade-offs below).",
           size=7.4, color=INK, fill=CREAM, line=ORANGE, r=0.08, margin=(0.1, 0.04, 0.1, 0.04), anchor="m")
    h2(p, 0.4, 3.86, 7.7, "Trade-off analysis: the rookie-team model")
    tr = [("Benefit", "2E9E5B", ["Rookies are not pushed out of roles by veterans", "Rookies learn through their own work and get personal FTC experience", "Veterans can attempt more complex strategies without harming rookie progress"]),
          ("Risk", "D64545", ["Rookies receive less direct training from veterans", "Veteran teams get less individual mentor attention"]),
          ("Our mitigation", BLUE, ["Veterans coach rookie leads on a schedule", "Shared templates & docs (below) so rookies do not start from zero", "Leadership applications open to every member each season"])]
    for i, (t, c, items) in enumerate(tr):
        x = 0.4 + i * 2.58
        p.rect(x, 4.18, 2.5, 0.22, fill=c, r=0.05)
        p.text(x, 4.18, 2.5, 0.22, t.upper(), size=7, color="FFFFFF", head=True, align="c", anchor="m")
        p.text(x, 4.44, 2.5, 0.95, ["• " + it for it in items], size=7, color=INK, gap=2)
    h2(p, 0.4, 5.5, 3.7, "Leadership: earned, not assigned")
    p.text(0.4, 5.84, 3.7, 1.55,
           ["Each season every member may **apply** for a captain or sub-team lead role. Mentors narrow the candidates; the remaining candidates **submit a sample of their work**; if the position is still contested, mentors **interview** each candidate.",
            "Result: leads are dedicated, qualified and confident, and they train the next leaders by pairing with them from day one."],
           size=8.2, color=INK, gap=4)
    h2(p, 4.3, 5.5, 3.8, "How we learn from mentors")
    p.text(4.3, 5.84, 3.8, 1.55,
           ["• **Teacher mentors** (Mr. Salgaonkar, Mr. Lindemann) keep the program running and review our non-tech and software work.",
            "• **Alumni mentors** (Andrew Torrance, college-age alumni from Santa Clara University) teach hardware & electrical skills they learned on this team.",
            "• **Program mentor** (Andrew Lawrence) connects the four Bellarmine teams and our community partners.",
            "• **Industry volunteers** judge our hackathon and give feedback on our projects (p8)."],
           size=7.8, color=INK, gap=3)
    h2(p, 0.4, 7.5, 7.7, "Documentation-first: so knowledge outlives the people who wrote it")
    docs = [("Architecture doc", "A **28 KB written walkthrough** of the robot code: field geometry, shot math, loop order, wiring channels, and the **reason behind each choice**"),
            ("Bring-up guide", "TUNING.md: **ten sections** in the order to do them, starting with **step 0 desk work** that needs no robot, then on-robot tuning"),
            ("Tune-0 to-do OpMode", "An OpMode on the Driver Station that marks **every tuning item** DONE / STOCK / TODO / CHECK so anyone sees what is left"),
            ("UML diagrams", "**Four class diagrams** (OpModes, subsystems & commands, shooting & field math, path tuners) show the structure at a glance (p14)")]
    for i, (t, b) in enumerate(docs):
        x = 0.4 + i * 1.94
        card(p, x, 7.84, 1.86, 1.3)
        p.rect(x, 7.84, 1.86, 0.07, fill=ORANGE)
        p.text(x + 0.05, 7.95, 1.76, 0.25, t, size=7.8, color=BLUE, bold=True, anchor="m")
        p.text(x + 0.05, 8.2, 1.76, 0.92, b, size=7.6, color=INK)
    p.text(0.4, 9.3, 7.7, 1.2,
           ["**Proof it transfers:** team 23230, which we mentor, started its season on the Gradle, FTC SDK 12.0.0 and library setup from our project, and its own project notes say so. "
            "Our code is built on the open FTC-Template-2027 starter, and we are passing our improvements forward in turn.",
            "**Time is our scarcest resource**, with 11 members and limited lab hours, so everyone ideates on season projects early and refreshes skills in the off-season to get a head start."],
           size=8.4, color=INK, fill="EEF3FB", line=BLUE, r=0.08, margin=(0.12, 0.06, 0.12, 0.06), anchor="m", gap=3)


# =========================================================== 5 BUSINESS
def bar_h(p, x, y, w, items, maxv, h=0.26, size=7):
    for i, (lab, v, c, txt) in enumerate(items):
        yy = y + i * (h + 0.07)
        p.text(x, yy, 1.1, h, lab, size=size, color=INK, bold=True, anchor="m")
        bw = max(0.02, (w - 1.9) * abs(v) / maxv)
        p.rect(x + 1.15, yy + 0.03, bw, h - 0.06, fill=c, r=0.04)
        p.text(x + 1.2 + bw, yy, 0.9, h, txt, size=size, color=c, head=True, anchor="m")


def p5():
    p = D.page(name="p5")
    chrome(p, 5, "Business & Finance", "plan", ["SUSTAIN", "THINK"], "Business")
    h2(p, 0.4, 0.92, 4.0, "Financial plan")
    p.text(0.4, 1.24, 3.85, 1.6,
           ["FTC is **expensive**, so we **plan money before we spend it**. Our rules:",
            "• **Sponsors first:** more reliable than grants and larger than fundraisers",
            "• **Cost-aware design:** expensive decisions get a written cost-benefit (below)",
            "• **Stay net-positive:** funding minus spending is tracked all season",
            "• **Carry a reserve** into next season for lean years"],
           size=8.2, color=INK, gap=4)
    h2(p, 4.35, 0.92, 3.75, "Last season's actuals (2025-26)")
    bar_h(p, 4.35, 1.28, 3.75, [("Sponsors", 15000, "2E9E5B", "+$15,000"), ("Member dues", 3300, "2E9E5B", "+$3,300"),
                                 ("Robot parts", 2038.26, "D64545", "−$2,038"), ("Registration", 1500, "D64545", "−$1,500")], 15000, h=0.24, size=6.8)
    p.text(4.35, 2.52, 3.75, 0.3, "Net: **+$14,761.74**, funds carried into this season", size=8, color="2E9E5B", fill="EAF6EF", r=0.06, anchor="m", margin=(0.1, 0, 0.05, 0))
    h2(p, 0.4, 2.98, 7.7, "This season")
    note(p, 0.4, 3.3, 3.75, 0.82, "2026-27 budget: sponsors $, dues $, registration $, parts $, travel $, reserve $ (a bar chart will go here)")
    p.text(4.3, 3.3, 3.8, 0.82, "**Sponsor engagement plan:** thank-you updates after each event, an invitation to see the robot at a meeting or qualifier, logos on the robot, pit, social media and this portfolio, and a yearly report of what their gift built.",
           size=7.2, color=INK, fill=CREAM, line=ORANGE, r=0.08, margin=(0.1, 0.04, 0.1, 0.04), anchor="m")
    p.text(0.4, 4.2, 7.7, 0.2, "THANK YOU TO OUR SPONSORS", size=7, color=ORANGE, head=True, margin=(0, 0, 0, 0))
    for i in range(6):
        slot(p, 0.4 + i * 1.29, 4.42, 1.2, 0.52, "sponsor", kind="ADD LOGO")
    h2(p, 0.4, 5.12, 7.7, "Cost-benefit analysis: five decisions that shaped the robot")
    cols = [("DECISION", 1.55), ("WHAT IT COSTS", 2.0), ("WHAT WE GET", 2.6), ("VERDICT", 1.55)]
    x = 0.4
    for c, w in cols:
        p.text(x, 5.44, w - 0.04, 0.22, c, size=6.5, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.08, 0, 0.04, 0), r=0.04)
        x += w
    rows = [("Turret on the shooter", "1 motor of our 8, a 32:1 gear train, an absolute encoder, and a 588-line turret subsystem to tune", "Aims at the hive with no chassis turning; enables shooting on the move (worth about +111 sim points)", "KEEP", "2E9E5B"),
            ("Single nose intake (was two)", "A shorter pickup zone: the robot must face the balls", "One fewer roller assembly and its deploy servos; sim scores about the same (≈459 vs ≈450)", "DROP 2nd INTAKE", ORANGE),
            ("4 beam-break switches, no color sensors", "Four cheap switches and wiring", "Exact ball count for a 4-ball limit; all POLLEN are yellow, so color adds nothing", "ADOPT", "2E9E5B"),
            ("No camera on the competition robot", "No automatic correction of odometry drift", "No camera, mount or vision code to fail; hive position is fixed, so odometry aims", "OMIT (proto kept)", ORANGE),
            ("OctoQuad encoder hub", "One extra board", "All encoders read in one bulk transaction per loop, so less loop time spent on I/O", "ADOPT", "2E9E5B")]
    y = 5.7
    for (a, b, c, v, vc) in rows:
        p.rect(0.4, y, 7.7, 0.56, fill="FFFFFF", line=LG, r=0.04)
        x = 0.4
        for txt, (cn, w), bold in zip((a, b, c), cols[:3], (True, False, False)):
            p.text(x, y, w - 0.04, 0.56, txt, size=6.7, color=INK, bold=bold, anchor="m", margin=(0.08, 0.01, 0.04, 0.01))
            x += w
        chip(p, x + 0.05, y + 0.18, v, vc, w=1.42, h=0.2, size=5.8)
        y += 0.59
    p.text(0.4, 8.7, 7.7, 0.42, "Sim scores come from our own AI driver in our simulator, not from robot matches (p15). Costs are given as parts, complexity and tuning time because exact prices change; the cost column will gain dollar figures from our bill of materials.",
           size=6.8, color=GRAY)
    h2(p, 0.4, 9.2, 7.7, "How a decision gets made")
    steps = [("1  NEED", "What does the game reward? (p9)"), ("2  OPTIONS", "Sketch 2-3 ways; list parts & complexity"), ("3  MODEL", "Run the sim and the math before cutting parts"),
             ("4  COST-BENEFIT", "Write cost vs. benefit; mentor reviews"), ("5  COMMIT", "Build it, log what we learn")]
    for i, (t, b) in enumerate(steps):
        x = 0.4 + i * 1.54
        p.hexa(x, 9.52, 1.5, 0.34, fill=NAVY if i % 2 == 0 else BLUE)
        p.text(x, 9.52, 1.5, 0.34, t, size=6.6, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.12, 0, 0.12, 0))
        p.text(x, 9.9, 1.5, 0.5, b, size=6.6, color=INK, align="c")


# =========================================================== 6 OUTREACH OVERVIEW
def p6():
    p = D.page(name="p6")
    chrome(p, 6, "Outreach: Impact & Strategy", "out", ["REACH", "CONNECT", "INSPIRE"], "Outreach")
    p.text(0.4, 0.9, 7.7, 0.55,
           "**Our goal:** establish **deep connections with the local community** and be an ambassador that puts **FIRST programs, from FLL to FTC,** in people's minds. "
           "We do not stop at one-time demos: **every event is designed to leave something behind**, ideally a new team.",
           size=8.4, color=INK)
    h2(p, 0.4, 1.5, 7.7, "Our outreach ladder")
    flow(p, 0.4, 1.84, 7.7, [("SPARK", "Exhibits where kids drive a real FTC robot: museums, festivals, libraries"),
                             ("TEACH", "Hands-on sessions: build a drivebase, code it, take on a challenge"),
                             ("FOUND", "Help schools and clubs start FLL / FTC teams of their own"),
                             ("STAY", "Keep showing up: weekly mentoring and monthly library events")],
         colors=["D6457A", ORANGE, "2E9E5B", BLUE])
    p.text(0.4, 2.98, 3.7, 0.2, "AUDIENCE PER EVENT (2025-26 SEASON)", size=7, color=BLUE, head=True, margin=(0, 0, 0, 0))
    ev = [("Techfest @ CHM", 400, "400+"), ("SJPL: 9 branches", 220, "220+"), ("Children's Disc. Museum", 200, "200+"), ("Bay Area Sci. Festival", 200, "200+"), ("The Tech Interactive", 100, "100+"), ("Scout-O-Rama", 100, "100+")]
    for i, (lab, v, t) in enumerate(ev):
        yy = 3.22 + i * 0.3
        p.text(0.4, yy, 1.5, 0.26, lab, size=6.8, color=INK, anchor="m")
        p.rect(1.95, yy + 0.04, 1.6 * v / 400, 0.18, fill="D6457A", r=0.04)
        p.text(1.98 + 1.6 * v / 400, yy, 0.5, 0.26, t, size=6.8, color="D6457A", head=True, anchor="m")
    stat(p, 4.3, 3.0, 1.2, "1000+", "people reached in person", "D6457A", h=0.72)
    stat(p, 5.58, 3.0, 1.2, "300+", "hours of outreach", "D6457A", h=0.72)
    stat(p, 6.86, 3.0, 1.24, "20+", "venues on our calendar", "D6457A", h=0.72)
    p.text(4.3, 3.8, 3.8, 1.2,
           ["Figures through our 2025-26 regional portfolio. This season adds weekly CHA mentoring, monthly library events, Code Crackers sessions, a joint library event with Astrobruins and Quixilver, and an OpenSauce invitation (p7-8).",
            dict(text="Totals for 2026-27 so far: ADD", color=ORANGE, bold=True)],
           size=7, color=GRAY, gap=2)
    h2(p, 0.4, 5.1, 7.7, "Who we work with")
    groups = [("LIBRARIES", "San José Public Library: Joyce Ellington, Dr. MLK, Biblioteca Latinoamericana, Rose Garden, Berryessa, Fremont Main and more", "2E9E5B"),
              ("MUSEUMS & SCIENCE", "The Tech Interactive · Computer History Museum · Children's Discovery Museum · Chabot Space & Science Center · Bay Area Science Festival · OpenSauce", ORANGE),
              ("SCHOOLS & CLUBS", "Graham Middle School · Canyon Heights Academy · St. Clare (Code Crackers) · St. Francis Cabrini · Stratford Fremont · Boy Scouts", BLUE),
              ("INDUSTRY & CITY", "Engineers at Meta (ChezyHacks judge) · City of San José / Beautify SJ · Silicon Valley 2025", "6C4BC1"),
              ("GLOBAL", "Agami / Switch School, Bangladesh (virtual coding class with codeMane) · Taipei STEAM delegation", "D6457A")]
    y = 5.42
    for (g, t, c) in groups:
        p.rect(0.4, y, 7.7, 0.4, fill="FFFFFF", line=LG, r=0.05)
        p.rect(0.4, y, 1.3, 0.4, fill=c, r=0.05)
        p.rect(1.55, y, 0.15, 0.4, fill=c)
        p.text(0.4, y, 1.3, 0.4, g, size=6.5, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.04, 0, 0.04, 0))
        p.text(1.76, y, 6.3, 0.4, t, size=6.9, color=INK, anchor="m")
        y += 0.44
    h2(p, 0.4, 7.7, 7.7, "We evaluate every event, then change how we do outreach")
    cols = [("WHAT WENT WELL", "2E9E5B", ["Parents asked how their kids can stay in FIRST, so we point elementary students to FLL", "Kids drive the robot themselves and light up"]),
            ("WHAT WE IMPROVE", "D64545", ["Needed more helping hands than expected, so we plan shifts and a standby crew", "Some ideas were too complex for kids"]),
            ("WHAT WE CHANGED", BLUE, ["Building drivebases from scratch was not feasible, so we use kitbots with manuals and Tinkercad", "Square fields only; added demo lifts and subsystem explanations"])]
    for i, (t, c, it) in enumerate(cols):
        x = 0.4 + i * 2.58
        p.rect(x, 8.02, 2.5, 0.22, fill=c, r=0.05)
        p.text(x, 8.02, 2.5, 0.22, t, size=6.8, color="FFFFFF", head=True, align="c", anchor="m")
        p.text(x, 8.28, 2.5, 1.05, ["• " + z for z in it], size=7.5, color=INK, gap=3)
    slot(p, 0.4, 9.4, 2.5, 1.1, "Recent event: kids driving a robot")
    slot(p, 3.0, 9.4, 2.5, 1.1, "Recent event: library or museum")
    p.text(5.6, 9.4, 2.5, 1.1, "**Safe by design:** our mentors who work with minors complete safe-environment (VIRTUS) training before school sessions.",
           size=7.2, color=INK, fill=CREAM, line=ORANGE, r=0.08, margin=(0.1, 0.04, 0.1, 0.04), anchor="m")


# =========================================================== 7 MENTORING
def p7():
    p = D.page(name="p7")
    chrome(p, 7, "Teams We Start & Mentor", "out", ["REACH", "CONNECT", "SUSTAIN"], "Outreach")
    p.text(0.4, 0.9, 7.7, 0.5, "Exhibits spark interest; **teams make it last.** We recruit new teams, coaches and mentors into FIRST by starting programs and showing up every week to help them succeed.",
           size=8.4, color=INK)
    # CHA hero
    p.rect(0.4, 1.46, 7.7, 2.45, fill=NAVY, r=0.12)
    p.hexa(0.55, 1.58, 1.2, 1.04, fill=ORANGE)
    p.text(0.55, 1.58, 1.2, 1.04, ["NEW", "THIS", "SEASON"], size=8, color="FFFFFF", head=True, align="c", anchor="m", gap=0)
    p.text(1.9, 1.52, 6.1, 0.4, "CHA MIDDLE SCHOOL ROBOTICS TEAM", size=14, color=HONEY, head=True, anchor="m")
    p.text(1.9, 1.92, 6.1, 0.3, "We started a robotics team at Canyon Heights Academy and mentor it every week.", size=8.4, color="FFFFFF", bold=True, anchor="m")
    ks = [("THURSDAYS", "3:40 pm, one hour per session"), ("SINCE 9/10", "6 sessions logged by Oct 29"), ("LAB TOUR", "CHA students visited our lab 9/29"), ("CERTIFIED", "Mentors carry VIRTUS safe-environment training")]
    for i, (a, b) in enumerate(ks):
        x = 1.9 + i * 1.55
        p.text(x, 2.3, 1.5, 0.8, [dict(text=a, head=True, size=8.5, color=HONEY), dict(text=b, size=6.9, color="FFFFFF")], fill="16305A", r=0.08, margin=(0.08, 0.04, 0.06, 0.04), anchor="m", gap=2)
    p.text(0.55, 2.72, 1.3, 1.2, "Weekly > one-off:\nstudents build, program and compete with a coach who knows their robot.", size=6.9, color="B8C4D8", anchor="t")
    p.text(1.9, 3.2, 6.1, 0.7, "**Why CHA:** Canyon Heights Academy had no team, so we started one. It is part of our push into Catholic middle schools and the Jesuit school network, a pipeline toward FLL and FTC. "
           "Students own the build; our mentors ask questions instead of giving answers.", size=7.2, color="FFFFFF")
    note(p, 0.4, 4.06, 7.7, 0.44, "CHA details: number of students, what they are building, coach / teacher who joined, goals for their first competition")
    # Code Crackers
    h2(p, 0.4, 4.62, 3.75, "Code Crackers · St. Clare MS", size=10)
    p.text(0.4, 4.94, 3.75, 1.9,
           ["Code Crackers is the student robotics team at St. Clare Middle School, working with a staff moderator. Our software and outreach members visit in small groups and **coach the students on their own robot and code**, then keep in touch through the team's moderator.",
            "• Sessions: Dec 1 and Dec 12, 2025 and again Sept 24, 2026",
            "• December visit: four of our members",
            "• Approach: coach, do not drive: students keep ownership of their robot and code"],
           size=7.8, color=INK, gap=3)
    h2(p, 4.35, 4.62, 3.75, "Graham Middle School → FLL")
    p.text(4.35, 4.94, 3.75, 1.9,
           ["We introduced robotics to Graham Middle School in Mountain View and **inspired them to create a First LEGO League team**. We guided students through designing and assembling drivebases and committed to support them through the FLL season.",
            dict(text="Our four-session starter curriculum:", bold=True, color=BLUE, gap=1),
            "• Day 1: form teams, start drivebase  • Day 2: finish drivebase, drive it",
            "• Day 3: program the drivebase  • Day 4: introduce a challenge"],
           size=7.8, color=INK, gap=3)
    h2(p, 0.4, 6.35, 7.7, "Everyone we have helped start or grow")
    rows = [("Graham MS (Mountain View)", "New FLL team", "Curriculum + drivebase build", "2E9E5B"),
            ("Canyon Heights Academy", "New team, weekly", "Thursdays since 9/10/2026", "2E9E5B"),
            ("Code Crackers · St. Clare MS", "Mentored team", "Software & robot coaching", BLUE),
            ("23229 & 23230 (Bellarmine)", "Rookie FTC teams", "Templates, tools, mentoring", BLUE),
            ("St. Francis Cabrini · Stratford Fremont", "Proposals for FLL", "Demo + full proposals sent", ORANGE),
            ("Agami / Switch School (Bangladesh)", "Virtual coding class", "~25 hours: Scratch → Python → Godot → Java", "D6457A"),
            ("Robotics summer camp", "6 weeks, ages by group", "Students build and compete", "D6457A")]
    p.text(0.4, 6.67, 2.6, 0.2, "WHO", size=6.3, color=GRAY, head=True, margin=(0.06, 0, 0, 0))
    p.text(3.0, 6.67, 1.5, 0.2, "WHAT", size=6.3, color=GRAY, head=True)
    p.text(4.5, 6.67, 3.6, 0.2, "HOW WE HELP", size=6.3, color=GRAY, head=True)
    y = 6.89
    for (a, b, c, col) in rows:
        p.rect(0.4, y, 7.7, 0.28, fill="FFFFFF", line=LG, r=0.04)
        p.rect(0.4, y, 0.06, 0.28, fill=col)
        p.text(0.5, y, 2.5, 0.28, a, size=6.9, color=INK, bold=True, anchor="m")
        p.text(3.0, y, 1.5, 0.28, b, size=6.9, color=col, bold=True, anchor="m")
        p.text(4.5, y, 3.6, 0.28, c, size=6.9, color=INK, anchor="m")
        y += 0.31
    h2(p, 0.4, 9.12, 7.7, "New coaches, mentors and volunteers we have brought in")
    p.text(0.4, 9.42, 7.7, 0.5,
           "A middle-school teacher and school staff who now host FIRST programs (Graham, CHA, St. Clare) · a Meta software engineer who judged ChezyHacks and offered continuing software support · "
           "San José Public Library staff who host us every month · college-age alumni who return to mentor.",
           size=7.4, color=INK)
    pr = [("Students drive", "We coach and ask questions; they keep the controller"), ("Kits, not scratch", "Starter kits and manuals; building a drivebase from raw parts was unfeasible"),
          ("Show up weekly", "Consistency beats a big one-time event"), ("Leave a coach behind", "Find a local champion, a teacher or parent, who keeps the team going")]
    for i, (a, b) in enumerate(pr):
        p.text(0.4 + i * 1.94, 10.0, 1.86, 0.55, [dict(text=a, bold=True, size=7, color=BLUE), dict(text=b, size=6.3, color=INK)], fill="EEF3FB", r=0.06, margin=(0.08, 0.03, 0.05, 0.03), anchor="m", gap=1)


# =========================================================== 8 COMMUNITY EVENTS
def p8():
    p = D.page(name="p8")
    chrome(p, 8, "Events, Partners & What's Next", "out", ["REACH", "CONNECT", "INSPIRE"], "Outreach")
    p.text(0.4, 0.9, 7.7, 0.45, "We go where families already are: libraries, museums, festivals and schools, with a robot kids can drive and an answer to “what can my child do next?”",
           size=8.4, color=INK)
    h2(p, 0.4, 1.4, 7.7, "Recurring programs: showing up on a schedule")
    rec = [("ROSE GARDEN LIBRARY", "First Thursday of every month, 4:30-5:30 pm", "2E9E5B"), ("BERRYESSA LIBRARY", "Monthly, starting Oct 11 at 3 pm", "2E9E5B"),
           ("CHA MENTORING", "Every Thursday, 3:40 pm (p7)", "D6457A"), ("SUMMER CAMP", "6-week robotics camp by age group", ORANGE)]
    for i, (a, b, c) in enumerate(rec):
        x = 0.4 + i * 1.94
        p.text(x, 1.74, 1.86, 0.72, [dict(text=a, head=True, size=7, color=c), dict(text=b, size=7, color=INK)], fill="FFFFFF", line=c, lw=1.25, r=0.08, margin=(0.1, 0.04, 0.06, 0.04), anchor="m", gap=2)
    h2(p, 0.4, 2.6, 7.7, "Featured events")
    cards = [("Techfest @ Computer History Museum", "400+", "We hosted a booth at a major Silicon Valley tech showcase and were personally invited back to return annually.", ORANGE),
             ("Bay Area Science Festival", "200+", "Visitors drove our robot; we recommended FLL to elementary families and invited rookie teams. Covered by KQED News.", "D6457A"),
             ("Fremont Main Library (joint)", "3+ teams", "Oct 11 joint event with Astrobruins and Quixilver, three Bay Area teams sharing one exhibit.", "2E9E5B"),
             ("ChezyHacks hackathon", "7 teams", "We hosted a hackathon for freshmen: teamwork, time management and presenting new ideas, judged by a Meta engineer.", BLUE),
             ("Children's Discovery Museum", "200+", "Two weekends supporting 23224's exhibit; we built a kit so kids could assemble a drivebase and drive it.", "6C4BC1"),
             ("Autumn Cleanup with Beautify SJ", "Off-season bot", "We repurposed an off-season robot to pick up trash, showing kids robotics can solve real-world problems.", "2E9E5B")]
    for i, (t, b, d, c) in enumerate(cards):
        x = 0.4 + (i % 3) * 2.58
        y = 2.92 + (i // 3) * 1.44
        card(p, x, y, 2.5, 1.36)
        p.rect(x, y, 2.5, 0.07, fill=c)
        p.text(x + 0.04, y + 0.1, 1.6, 0.4, t, size=7.2, color=INK, bold=True, anchor="m")
        p.text(x + 1.55, y + 0.1, 0.92, 0.4, b, size=9, color=c, head=True, align="r", anchor="m")
        p.text(x + 0.04, y + 0.52, 2.42, 1.0, d, size=7.6, color=INK)
    h2(p, 0.4, 5.9, 7.7, "Also on our calendar")
    p.text(0.4, 6.22, 7.7, 0.62,
           "The Tech Interactive · Scout-O-Rama and Boy Scouts robotics merit badge workshops · San José Public Library branches (Joyce Ellington, Dr. MLK, Biblioteca Latinoamericana, "
           "Willow Glen, Hillview and others) · Chabot Space & Science Center, Oakland · Warm Springs Elementary · Chezy Champs · Taipei STEAM delegation hosted with 23224",
           size=7.2, color=INK)
    p.rect(0.4, 6.95, 7.7, 0.9, fill=NAVY, r=0.1)
    p.hexa(0.52, 7.08, 1.0, 0.64, fill=HONEY)
    p.text(0.52, 7.08, 1.0, 0.64, "NEW", size=10, color=NAVY, head=True, align="c", anchor="m")
    p.text(1.65, 6.99, 6.35, 0.82, [dict(text="OPENSAUCE INVITATION", head=True, size=9.5, color=HONEY),
                                     dict(text="We were invited to bring our robot to OpenSauce, a large maker and engineering expo, to reach makers, engineers and families far beyond the FIRST community.", size=7.2, color="FFFFFF")],
           anchor="m", gap=2)
    note(p, 0.4, 7.95, 7.7, 0.4, "OpenSauce: date, role, attendance; plus attendance for the Oct-Nov 2026 library and school events")
    slot(p, 0.4, 8.5, 2.5, 1.0, "Event photo: library / museum")
    slot(p, 3.0, 8.5, 2.5, 1.0, "Event photo: hackathon / OpenSauce")
    slot(p, 5.6, 8.5, 2.5, 1.0, "Event photo: kids with the robot")
    h2(p, 0.4, 9.62, 7.7, "What's next: ideas already on our plan")
    nx = [("Mentor-matching website", "Connect mentors with FIRST teams that need them"), ("More scrimmages", "Host multi-team events, not just sister teams"),
          ("Autism daycare visits", "Bring kitbots for children to build"), ("Guatemala outreach", "Through a mission trip and nonprofit")]
    for i, (a, b) in enumerate(nx):
        x = 0.4 + i * 1.94
        p.text(x, 9.94, 1.86, 0.58, [dict(text=a, bold=True, size=7, color=BLUE), dict(text=b, size=6.6, color=GRAY)], fill="EEF3FB", r=0.06, margin=(0.08, 0.03, 0.05, 0.03), anchor="m", gap=1)



def sect_title(p, x, y, w, t, color=NAVY):
    p.text(x, y, w, 0.22, t.upper(), size=7, color=color, head=True, anchor="m", margin=(0, 0, 0, 0))


# =========================================================== 9 GAME STRATEGY
def p9():
    p = D.page(name="p9")
    chrome(p, 9, "Game Analysis & Strategy", "eng", [], "Engineering")
    p.text(0.4, 0.9, 7.7, 0.62,
           "**BIOBUZZ in brief.** Two alliances of two robots launch yellow **POLLEN** into the **up CELL** of their **HIVE**, a bi-stable rocking structure with a basket (CELL) at each end of its arm. "
           "When enough weight sits in the up CELL, the HIVE **TIPS**: that CELL spills, the other CELL swings up, and the alliance scores **20 points**. "
           "Match: **AUTO 30 s · 8 s transition · TELEOP 2:00**. A robot holds at most **4 POLLEN** (G407).", size=8, color=INK)
    caps = [("1", "**Launch** into the up CELL. POLLEN collects in the basket.", ORANGE), ("2", "**Swing.** The weight tips the arm; our sim models the swing at **4.5 s**.", BLUE),
            ("3", "**Settled.** TIP scored (**+20**); the other CELL is now up, so the **target has moved**.", "2E9E5B")]
    for i, ((n, c_, col), im) in enumerate(zip(caps, ["hive_before.png", "hive_mid.png", "hive_after.png"])):
        x = 0.4 + i * 2.6
        p.rect(x, 1.6, 2.5, 1.62, fill="14202F", r=0.08)
        p.image(A + im, x + 0.03, 1.63, 2.44, 1.56, fit='cover', r=0.07)
        p.hexa(x + 0.08, 1.68, 0.4, 0.34, fill=col)
        p.text(x + 0.08, 1.68, 0.4, 0.34, n, size=10, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
        p.text(x, 3.25, 2.5, 0.42, c_, size=7, color=INK, margin=(0.04, 0.02, 0.04, 0))
        if i < 2:
            p.line(x + 2.5, 2.4, x + 2.6, 2.4, color=ORANGE, w=2, arrow=True)
    p.text(0.4, 3.68, 7.7, 0.18, "Frames rendered by our simulator from the official field CAD: the HIVE tilts about its pivot at 43.95 in; each CELL opening sits 53-60 in off the floor.", size=6, color=GRAY, margin=(0.02, 0, 0, 0))
    # scoring table
    sect_title(p, 0.4, 3.92, 4, "Scoring (manual V1 + Team Updates through TU07)", BLUE)
    rows = [("LEAVE (stop touching the wall)", "3", "–"), ("PARK in own LOADING ZONE", "5", "5"), ("HIVE TIP", "20", "20"), ("POLLEN / NECTAR left in an up CELL", "–", "2 each"),
            ("Bottom NECTAR bonus (FLOWER)", "–", "5"), ("POLLEN / NECTAR in an owned FLOWER", "–", "2 each"), ("POLLEN / NECTAR in a GARDEN", "–", "1 each")]
    p.text(0.4, 4.15, 2.7, 0.19, "ACHIEVEMENT", size=6, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.06, 0, 0, 0), r=0.03)
    p.text(3.1, 4.15, 0.5, 0.19, "AUTO", size=6, color="FFFFFF", head=True, fill=NAVY, align="c", anchor="m")
    p.text(3.62, 4.15, 0.7, 0.19, "TELEOP", size=6, color="FFFFFF", head=True, fill=NAVY, align="c", anchor="m")
    y = 4.36
    for i, (a_, b_, c_) in enumerate(rows):
        hl = a_.startswith("HIVE")
        p.rect(0.4, y, 3.92, 0.19, fill="FFF6E0" if hl else ("FFFFFF" if i % 2 == 0 else "F4F7FC"), line=LG, r=0.02)
        p.text(0.4, y, 2.7, 0.19, a_, size=6.8, color=INK, bold=hl, anchor="m", margin=(0.06, 0, 0, 0))
        p.text(3.1, y, 0.5, 0.19, b_, size=7.2, color=ORANGE if hl else INK, head=hl, bold=not hl, align="c", anchor="m")
        p.text(3.62, y, 0.7, 0.19, c_, size=7.2, color=ORANGE if hl else INK, head=hl, bold=not hl, align="c", anchor="m")
        y += 0.19
    p.text(0.4, y + 0.02, 3.92, 0.3, "**Ranking points:** SWARM (LEAVE + PARK), POLLINATOR 1 (**4+ TIPs**), POLLINATOR 2 (**7+ TIPs**). Only a launch into the up CELL can cause a TIP (G417).", size=6.5, color=GRAY)
    sect_title(p, 4.55, 3.92, 3.5, "Where our points come from (simulated best-AI match)", BLUE)
    bars = [("TIPs", 530, "TIP × 26.5 ≈ 530", ORANGE), ("PARK", 5, "5", BLUE), ("Other", 10, "≈ 10", GRAY)]
    for i, (a_, v, t, c) in enumerate(bars):
        yy = 4.16 + i * 0.3
        p.text(4.55, yy, 0.6, 0.26, a_, size=7.2, color=INK, bold=True, anchor="m")
        p.rect(5.15, yy + 0.04, max(0.05, 1.7 * v / 530), 0.18, fill=c, r=0.04)
        p.text(5.2 + 1.7 * v / 530, yy, 1.3, 0.26, t, size=6.8, color=c, bold=True, anchor="m")
    p.text(4.55, 5.1, 3.55, 0.6, "**97% of points are TIPs.** Every design choice is judged by one question: does it put **more POLLEN in the up CELL, faster, even when defended?**", size=7.3, color=INK, fill=CREAM, line=ORANGE, r=0.07, margin=(0.1, 0.03, 0.1, 0.03), anchor="m")
    # tip economics
    h2(p, 0.4, 5.98, 7.7, "TIP economics → the numbers that size the robot")
    bx = [("8", "**POLLEN** in the up CELL tips it (our model: NECTAR/5 + POLLEN/8 ≥ 1)", ORANGE), ("4.3 s", "**between TIPs** in the best simulated match (first TIP at 3.0 s)", BLUE),
          ("8.2", "**shots per TIP**, so about **1.9 shots every second**, sustained", "2E9E5B"), ("4.5 s", "**HIVE swing time:** the target moves and we must re-aim at once", "6C4BC1")]
    for i, (b_, t, c) in enumerate(bx):
        x = 0.4 + i * 1.94
        p.hexa(x, 6.3, 0.85, 0.58, fill=c)
        p.text(x, 6.3, 0.85, 0.58, b_, size=11, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.12, 0, 0.12, 0))
        p.text(x + 0.88, 6.26, 1.02, 0.66, t, size=6.4, color=INK, anchor="m", margin=(0.02, 0, 0, 0))
    p.text(0.4, 6.92, 7.7, 0.26, "The manual gives no ball count for a TIP, so **8 is our model** of the HIVE (derived from the CAD, checked in the simulator, p15). We will re-measure on a real field.", size=6.5, color=GRAY)
    # pillars
    h2(p, 0.4, 7.22, 7.7, "Strategy pillars → robot requirements → what we built")
    cols = [("PILLAR", 1.55), ("REQUIREMENT", 2.55), ("OUR ANSWER", 3.6)]
    x = 0.4
    for c, w in cols:
        p.text(x, 7.52, w - 0.04, 0.2, c, size=6.4, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.08, 0, 0.04, 0), r=0.04)
        x += w
    pil = [("1  Throughput", "About **1.9 shots/s**; never wait for balls or a flywheel", "**One-path nose intake**, exact 4-ball count, full-power feed with an index gate, a flywheel that recovers within a ball's time (p12-13)", ORANGE),
           ("2  Accuracy anywhere", "Land in a **20 in opening** from 24-96 in, tilted, from a moving robot", "**Hood to 70-85°**, turret, shot table + physics, shoot-on-the-move (p12, p14)", BLUE),
           ("3  Keep moving", "Aim while driving and while being pushed; follow the HIVE as it tips", "**Turret feedforward** from chassis motion; target CELL chosen by field position (p13-14)", "2E9E5B"),
           ("4  Safe autonomous", "**LEAVE 3 + PARK 5** and a preload volley, every time", "**State-machine auto** with a clock override that parks with time to spare (p14)", "6C4BC1")]
    y = 7.74
    for (a_, b_, c_, col) in pil:
        p.rect(0.4, y, 7.7, 0.44, fill="FFFFFF", line=LG, r=0.04)
        p.rect(0.4, y, 0.06, 0.44, fill=col)
        p.text(0.5, y, 1.45, 0.44, a_, size=7.3, color=col, head=True, anchor="m")
        p.text(1.95, y, 2.5, 0.44, b_, size=6.7, color=INK, anchor="m")
        p.text(4.5, y, 3.58, 0.44, c_, size=6.7, color=INK, anchor="m")
        y += 0.47
    h2(p, 0.4, 9.66, 7.7, "What we chose not to build, and the evidence")
    nb = [("No FLOWER farming", "Our AI driver **learned to ignore FLOWERs** (0 pickups per match in the best run), so the ramp is small and interlocked."),
          ("No sorting, no color", "BIOBUZZ has **no color pattern** to score, so 4 switches count balls and nothing more."),
          ("Plan for defense", "The strongest simulated defense cuts our simulated score from **458 to 379**, so aiming must survive pushing.")]
    for i, (a_, b_) in enumerate(nb):
        x = 0.4 + i * 2.58
        p.text(x, 9.96, 2.5, 0.6, [dict(text=a_, bold=True, size=7, color=BLUE), dict(text=b_, size=6.5, color=INK)], fill="EEF3FB", r=0.07, margin=(0.08, 0.03, 0.06, 0.03), anchor="m", gap=1)


# =========================================================== 10 DESIGN PROCESS
def p10():
    p = D.page(name="p10")
    chrome(p, 10, "Design Process & Lessons", "eng", ["THINK", "DESIGN", "INNOVATE"], "Engineering")
    h2(p, 0.4, 0.92, 7.7, "Ideate → Create → Test → Iterate, with a simulator in the loop")
    st = [("IDEATE", "Read the manual, model the game (p9), list options, write costs and benefits (p5)", "2E9E5B"),
          ("CREATE", "Parametric Onshape CAD with master sketches; the same CAD becomes the sim model", BLUE),
          ("TEST", "Sim first (physics, AI drivers), then desk tests, then the robot with tuner OpModes", ORANGE),
          ("ITERATE", "Log what failed, change one thing, re-run. Every change is explained in a doc", "D6457A")]
    for i, (t, b, c) in enumerate(st):
        x = 0.4 + i * 1.94
        p.hexa(x, 1.26, 1.86, 0.44, fill=c)
        p.text(x, 1.26, 1.86, 0.44, t, size=8.5, color="FFFFFF", head=True, align="c", anchor="m")
        p.text(x, 1.74, 1.86, 0.72, b, size=6.9, color=INK, align="c")
    sect_title(p, 0.4, 2.52, 7.7, "Every part is judged against our SECURE checklist: Sustainable · Efficient · Controlled · Unique · Reliable · Elegant", BLUE)
    sec = [("Sustainable", "**Docs, tuning checklists** and serviceable modules outlive the season"), ("Efficient", "**One ball path**, 8 motors, 5 servos, no spare mechanisms"),
           ("Controlled", "**Feedback on every axis:** pods, turret encoders, ball switches, flywheel speed"), ("Unique", "**Hood-driven high lob** and a turret that leads a moving target"),
           ("Reliable", "**Exact ball count**, jam detection, interlocks, safe defaults"), ("Elegant", "Subsystems never reference each other; clean CAD")]
    for i, (a, b) in enumerate(sec):
        x = 0.4 + (i % 3) * 2.58
        y = 2.78 + (i // 3) * 0.62
        p.text(x, y, 2.5, 0.56, [dict(text=a.upper(), head=True, size=7, color=ORANGE), dict(text=b, size=6.7, color=INK)], fill="FFFFFF", line=LG, r=0.06, margin=(0.08, 0.03, 0.06, 0.03), anchor="m", gap=1)
    # evolution table
    h2(p, 0.4, 4.1, 7.7, "What we changed after DECODE, and why (design evolution)")
    cols = [("SYSTEM", 0.95), ("DECODE ROBOT (2025-26)", 2.15), ("BIOBUZZ ROBOT (now)", 2.4), ("WHY", 2.2)]
    x = 0.4
    for c, w in cols:
        p.text(x, 4.4, w - 0.04, 0.2, c, size=6.2, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.08, 0, 0.04, 0), r=0.04)
        x += w
    ev = [("Intake", "**Double-sided** intake with full-width vectored wheels feeding a **5-stage** feeder", "**One nose intake** (305 mm reach, 300 mm mouth) lowered by pivot servos; 2 motors; holds 4", "Sim: AI scored about the same with one intake (**≈459 vs ≈450**); one fewer assembly to build and tune"),
          ("Ball sensing", "**Color sensors** at each feeder stage identified ball colors", "**4 beam-break switches** count 0-4; jams flagged from motor speed", "BIOBUZZ has **no color pattern**; the rule limit is 4, so an exact count is enough"),
          ("Turret", "**360° chain-driven** turret on two synchronized servos", "**Motor-driven**, 32:1 gears, ±200° soft limits, motor + absolute encoders", "A motor allows a **velocity loop with feedforward** (p13)"),
          ("Hood & shot", "Servo-driven hood on **herringbone gears**; lookup table of angle and power", "Hood servo **45-85°**; the game needs **70-85°**. Tuned shot table + physics fills the gaps", "The HIVE opening must be entered **falling steeply** (p12)"),
          ("Flywheel", "4 in TPU flywheel with added weights; **dynamic PIDF** raised gains after each shot", "Single 4 in flywheel, 6000 rpm motor: **bang-bang** outside ±75 rpm, **PID + feedforward** inside, full power while feeding", "PID alone **recovered too slowly** between balls"),
          ("Vision & odometry", "**Limelight** AprilTag tracking trims the turret; **Pinpoint** computer for odometry", "**No camera** on the competition robot (prototype only); two 4-bar dead-wheel pods into an **OctoQuad** hub", "HIVE position is fixed and known from CAD, so odometry aims; one bulk read gets every encoder")]
    y = 4.62
    for (a_, b_, c_, d_) in ev:
        p.rect(0.4, y, 7.7, 0.5, fill="FFFFFF", line=LG, r=0.04)
        x = 0.4
        for txt, (cn, w), bold, col in zip((a_, b_, c_, d_), cols, (True, False, False, False), (BLUE, GRAY, INK, INK)):
            p.text(x, y, w - 0.04, 0.5, txt, size=6.4 if not bold else 7, color=col, bold=bold, anchor="m", margin=(0.07, 0.01, 0.03, 0.01))
            x += w
        y += 0.52
    # lessons log
    h2(p, 0.4, 7.82, 7.7, "Lessons learned log (and what we did about each)")
    ls_ = [("DECODE: intake slipped on the ramp", "Grip tape on the ramp edge and isopropyl alcohol on every wheel before each match, now standard."),
           ("DECODE: flywheel speed dipped between shots", "Moved from dynamic PIDF to a hybrid that holds full power while a ball is in the wheel (p12)."),
           ("Our model of the HIVE was wrong", "We corrected the swing time from 0.85 s to 4.5 s. The old AI fell from **499 to 329** points under the new timing; retrained, it reached **450**. We now re-check every rule and retrain."),
           ("Measured CAD angles disagreed", "Two measured HIVE travel angles (116.66°, 81.07°) were wrong; the true **60.03°** came from mirror symmetry. Verify before trusting a number."),
           ("Update order created lag", "Applying the path follower late in the loop added about one loop of stick lag; the loop order is now fixed and documented (p14)."),
           ("Turret zero must be reliable", "The absolute encoder is wired but seeding is off until verified; the stow procedure is the fallback (p13).")]
    for i, (a, b) in enumerate(ls_):
        x = 0.4 + (i % 2) * 3.88
        y = 8.14 + (i // 2) * 0.82
        p.text(x, y, 3.8, 0.78, [dict(text=a, bold=True, size=7.1, color=ORANGE), dict(text=b, size=6.8, color=INK)], fill="FFFFFF", line=LG, r=0.06, margin=(0.1, 0.04, 0.08, 0.04), anchor="m", gap=1)


# =========================================================== 11 ROBOT OVERVIEW
def p11():
    p = D.page(name="p11")
    chrome(p, 11, "Robot Overview", "eng", ["DESIGN", "INNOVATE", "THINK"], "Engineering")
    p.rect(0.4, 0.92, 7.7, 3.35, fill="D6EAF8", r=0.14)
    p.image(A + 'robot_hero.png', 0.45, 0.97, 4.85, 3.25, fit='cover', r=0.1)
    p.image(A + 'robot_explode.png', 5.38, 0.97, 2.67, 1.6, fit='cover', r=0.08)
    p.image(A + 'turret.png', 5.38, 2.62, 1.3, 1.6, fit='cover', r=0.08)
    p.image(A + 'flower.png', 6.75, 2.62, 1.3, 1.6, fit='cover', r=0.08)
    p.text(0.5, 3.9, 4.6, 0.3, "Rendered from our Onshape CAD in the simulator's pit display", size=6.3, color=NAVY, fill="FFFFFF", alpha=0.7, anchor="m")
    p.text(5.4, 0.99, 2.6, 0.2, "EXPLODED VIEW", size=6, color=NAVY, head=True, margin=(0.06, 0, 0, 0))
    p.text(5.4, 4.0, 1.3, 0.2, "TURRET", size=6, color=NAVY, head=True, margin=(0.06, 0, 0, 0))
    p.text(6.77, 4.0, 1.3, 0.2, "FLOWER RAMP", size=6, color=NAVY, head=True, margin=(0.06, 0, 0, 0))
    h2(p, 0.4, 4.4, 7.7, "The robot at a glance")
    specs = [("DRIVE", "Mecanum, 4 motors. Footprint 320 × 334 mm (12.6 × 13.15 in), 289 mm tall stowed: well inside the 18 in limit. Tuned path-following top speed 72 in/s forward, 46 in/s strafe.", BLUE),
             ("ODOMETRY", "Two goBILDA 4-bar dead-wheel pods into an OctoQuad MK2 hub, read once per loop; Pedro Pathing localizer with on-hub IMU fusion.", "0E9AA7"),
             ("SHOOTER", "One 4 in flywheel on a 6000 rpm motor with a 28 tick/rev encoder. Hood servo 45-85°. An index gate servo in front of the wheel holds balls until we are ready to shoot.", ORANGE),
             ("TURRET", "One motor, two-stage gear train 9→60 and 15→72 (32:1), ±200° travel, 4:1-up absolute encoder, tracks the HIVE CELL.", "6C4BC1"),
             ("INTAKE", "Single nose intake, 2 motors (pickup and transfer) and 2 pivot servos that lower and stow it. Holds 4 POLLEN, counted by 4 switches.", "2E9E5B"),
             ("FLOWER RAMP", "One servo swings the ramp 32° down to the tiles with about a 12 in stand-off. Interlocked with the intake: they take turns.", "D6457A"),
             ("ELECTRONICS", "Control Hub + Expansion Hub, OctoQuad, REV Blinkin LED driver. 8 motors, 5 servos in total. Limelight exists only in a prototype config.", GRAY),
             ("SOFTWARE", "SolversLib command-based, Pedro Pathing 3 with Foresight, Panels live tuning, AdvantageScope logging. ~99 Java files (p14).", NAVY)]
    for i, (a, b, c) in enumerate(specs):
        x = 0.4 + (i % 2) * 3.88
        y = 4.72 + (i // 2) * 0.82
        p.rect(x, y, 3.8, 0.76, fill="FFFFFF", line=LG, r=0.06)
        p.rect(x, y, 0.07, 0.76, fill=c)
        p.text(x + 0.1, y + 0.02, 0.9, 0.72, a, size=7.4, color=c, head=True, anchor="m")
        p.text(x + 1.0, y + 0.02, 2.78, 0.72, b, size=6.6, color=INK, anchor="m")
    h2(p, 0.4, 8.06, 7.7, "Design analysis: elegant, efficient, practical to maintain")
    cols = [("ELEGANT", "One ball path from nose to flywheel. Each subsystem has one job and never talks to another directly; commands combine them.", ORANGE),
            ("EFFICIENT", "8 motors and 5 servos cover drive, intake, transfer, turret, flywheel, hood, gate, ramp. We removed the second intake instead of adding capability we cannot score with.", BLUE),
            ("PRACTICAL TO MAINTAIN", "We plan assembly and repair order in the exploded CAD view. Hardware names are fixed in one config, and a Driver Station checklist runs every subsystem before a match.", "2E9E5B")]
    for i, (a, b, c) in enumerate(cols):
        x = 0.4 + i * 2.58
        p.rect(x, 8.38, 2.5, 0.22, fill=c, r=0.05)
        p.text(x, 8.38, 2.5, 0.22, a, size=6.8, color="FFFFFF", head=True, align="c", anchor="m")
        p.text(x, 8.64, 2.5, 1.0, b, size=7.5, color=INK)
    h2(p, 0.4, 9.34, 7.7, "Design risks we are managing")
    p.text(0.4, 9.64, 7.7, 0.5,
           "**Hood range and turret zero** are the two mechanisms the strategy depends on, so both have a bench in the pit display and a desk-test OpMode before any on-robot tuning. "
           "**A single intake** means we must face the POLLEN; the sim shows the AI driver does this without a scoring loss.", size=7.1, color=INK)
    note(p, 0.4, 10.16, 7.7, 0.4, "Robot weight, drive wheel type / size / gearing, and a photo of the built robot")
    note(p, 5.55, 9.0, 0, 0, "") if False else None



from ballistics import solve, g as GRAV, h0 as H0, ht as HT


def box(p, x, y, w, h, title, body, fill="FFFFFF", line=BLUE, tc=INK, tsize=7.2, bsize=6.4):
    p.text(x, y, w, h, [dict(text=title, bold=True, size=tsize, color="FFFFFF" if fill in (NAVY,) else line), dict(text=body, size=bsize, color=tc)],
           fill=fill, line=line, lw=1.0, r=0.07, margin=(0.07, 0.03, 0.05, 0.03), anchor="m", gap=1, align="c")


# =========================================================== 12 SHOOTER
def p12():
    p = D.page(name="p12")
    chrome(p, 12, "Shooter & Hood", "eng", ["INNOVATE", "CONTROL", "THINK"], "Engineering")
    p.text(0.4, 0.9, 7.7, 0.5, "**Problem:** the up CELL's opening is a 20 in mouth, 53-60 in off the floor and tilted. A ball must arrive **falling steeply** to drop in. "
           "**Our answer:** a 4 in flywheel that holds one speed band, and a hood that does the distance work (70-85°).", size=8.2, color=INK)
    # trajectory card
    card(p, 0.4, 1.46, 4.05, 3.08, fill="F4F7FC")
    p.text(0.45, 1.48, 3.95, 0.2, "TRAJECTORY TO THE UP CELL, 72 in AWAY (drag-free model)", size=6.2, color=GRAY, head=True, anchor="m", margin=(0.04, 0, 0, 0))
    ox, oy, k = 0.7, 4.4, 0.029
    def P(xi, yi):
        return (ox + xi * k, oy - yi * k)
    p.line(*P(-14, 0), *P(112, 0), color=GRAY, w=1)
    rx, ry = P(-12, 10.6)
    p.rect(rx, ry, 12 * k, 10.6 * k, fill=NAVY, r=0.02)
    p.text(rx - 0.1, oy + 0.0, 0.8, 0.14, "robot", size=5.6, color=NAVY, bold=True)
    d = 72
    for th, col, dash_ in [(75, "2E9E5B", False), (50, "D64545", True)]:
        r = solve(d, th)
        v = r["v"]
        t = math.radians(th)
        pts = []
        T = r["tof"]
        for i in range(0, 61):
            tt = T * i / 60
            pts.append(P(v * math.cos(t) * tt, H0 + v * math.sin(t) * tt - 0.5 * GRAV * tt * tt))
        p.curve(pts, color=col, w=2, dash=dash_)
    cx_, cy_ = P(d, HT)
    p.poly([(cx_ - 10 * k, cy_ - 4 * k), (cx_ - 10 * k, cy_ + 3 * k), (cx_ + 10 * k, cy_ + 3 * k), (cx_ + 10 * k, cy_ - 4 * k), (cx_ + 8 * k, cy_ - 4 * k), (cx_ + 8 * k, cy_ + 1 * k), (cx_ - 8 * k, cy_ + 1 * k), (cx_ - 8 * k, cy_ - 4 * k)], fill=HONEY, line=NAVY, lw=1)
    p.text(cx_ + 0.32, cy_ - 0.12, 1.1, 0.2, "up CELL, ~20 in wide", size=5.8, color=NAVY, bold=True)
    r75, r50 = solve(d, 75), solve(d, 50)
    p.text(3.0, 1.8, 1.4, 0.7, [dict(text="75° hood", bold=True, size=7, color="2E9E5B"), dict(text="drops in at %d° descent" % round(r75["desc"]), bold=True, size=6.4, color="2E9E5B"),
                                dict(text="%d in/s · ≈%d rpm · %.1f s" % (round(r75["v"]), round(r75["rpm"], -1), r75["tof"]), size=5.8, color=GRAY)], gap=0)
    p.text(3.0, 3.35, 1.4, 0.7, [dict(text="50° hood", bold=True, size=7, color="D64545"), dict(text="arrives nearly level (%d° descent)" % round(r50["desc"]), bold=True, size=6.4, color="D64545"),
                                dict(text="the basket cannot take it", size=5.8, color=GRAY)], gap=0)
    # table
    cols = [("DISTANCE", 0.72), ("HOOD", 0.55), ("EXIT SPEED", 0.8), ("WHEEL", 0.7), ("FLIGHT", 0.55), ("DESCENT", 0.7)]
    x = 0.4
    for c, w in cols:
        p.text(x, 4.62, w - 0.03, 0.2, c, size=5.8, color="FFFFFF", head=True, fill=NAVY, anchor="m", align="c", margin=(0, 0, 0, 0), r=0.03)
        x += w
    y = 4.84
    for d_, th in [(24, 85), (48, 80), (72, 75), (96, 70)]:
        r = solve(d_, th)
        vals = ["%d in" % d_, "%d°" % th, "%d in/s" % round(r["v"]), "%d rpm" % round(r["rpm"], -1), "%.1f s" % r["tof"], "%d°" % round(r["desc"])]
        x = 0.4
        for (c, w), vv in zip(cols, vals):
            p.text(x, y, w - 0.03, 0.2, vv, size=6.6, color=INK, align="c", anchor="m", margin=(0, 0, 0, 0), fill="F4F7FC" if d_ in (24, 72) else "FFFFFF")
            x += w
        y += 0.21
    p.text(0.4, 5.7, 4.05, 0.52, "**Insight:** with the hood scheduled 85° → 70°, the wheel stays near 2,300-2,450 rpm from 24 to 96 in, so the flywheel only has to hold **one speed band** and the hood does the distance work. "
           "Wheel rpm assumes the 52% ball-to-wheel speed transfer seen in our sim.", size=6.7, color=INK)
    # right column: flywheel control
    h2(p, 4.6, 1.42, 3.5, "Flywheel control", size=10)
    card(p, 4.6, 1.74, 3.5, 1.62, fill="F4F7FC")
    p.text(4.65, 1.76, 3.4, 0.18, "POWER vs. SPEED ERROR (control law, schematic)", size=6, color=GRAY, head=True, anchor="m")
    ax0, ay0, aw, ah = 4.9, 3.15, 3.0, 0.82
    p.line(ax0, ay0, ax0 + aw, ay0, color=GRAY, w=0.8)
    p.line(ax0 + aw / 2, ay0 - ah - 0.05, ax0 + aw / 2, ay0 + 0.04, color=GRAY, w=0.8)
    # error axis: left = above target (negative error), right = below target
    xl, xr = ax0 + aw * 0.28, ax0 + aw * 0.72
    p.curve([(ax0, ay0 - 0.05), (xl, ay0 - 0.05), (xl + 0.05, ay0 - 0.3), (xr - 0.05, ay0 - 0.7), (xr, ay0 - ah), (ax0 + aw, ay0 - ah)], color=ORANGE, w=2.4)
    p.text(ax0 - 0.05, ay0 - 0.3, 0.9, 0.24, "cut power", size=5.6, color=GRAY, gap=0)
    p.text(ax0, ay0 + 0.02, 0.8, 0.16, "above target", size=5.4, color=GRAY)
    p.text(ax0 + aw - 0.8, ay0 + 0.02, 0.8, 0.16, "below target", size=5.4, color=GRAY, align="r")
    p.text(ax0 + aw - 0.85, ay0 - ah - 0.28, 1.0, 0.2, "FULL POWER", size=6, color=ORANGE, head=True, align="c")
    p.text(ax0 + aw * 0.28, ay0 - ah - 0.26, aw * 0.44, 0.18, "±75 rpm: PID + feedforward", size=6, color=BLUE, bold=True, align="c")
    p.rect(xl, ay0 - ah - 0.02, xr - xl, ah + 0.02, fill=BLUE, alpha=0.08)
    p.text(4.7, 3.36, 3.35, 0.1, "", size=4)
    p.text(4.6, 3.4, 3.5, 1.2,
           ["• **Far below target:** full power for the fastest spin-up. **Inside ±75 rpm:** PID + feedforward holds speed (kP 0.0006, kI 0.0005). **Above:** cut power (never reverse).",
            "• **While feeding:** stay at full power and cut at 60 rpm over target, so each ball's speed dip is refilled before the next ball arrives.",
            "• **Ready** when measured speed is within 90 rpm, the hood has arrived and the turret is on target. Idle at 3,000 rpm so spin-up is short."],
           size=6.7, color=INK, gap=2)
    h2(p, 4.6, 4.7, 3.5, "Error budget at 60 in", size=10)
    bud = [("Opening half-width", 10.1, "±10.1 in", GRAY), ("Flywheel ±90 rpm", 6.6, "±6.6 in", ORANGE), ("Turret ±1.5°", 1.6, "±1.6 in", BLUE), ("Both, combined", 6.8, "±6.8 in", "2E9E5B")]
    for i, (a, v, t, c) in enumerate(bud):
        yy = 5.02 + i * 0.26
        p.text(4.6, yy, 1.2, 0.22, a, size=6.5, color=INK, bold=True, anchor="m")
        p.rect(5.85, yy + 0.04, 1.6 * v / 10.1, 0.14, fill=c, r=0.03)
        p.text(5.9 + 1.6 * v / 10.1, yy, 0.8, 0.22, t, size=6.4, color=c, head=True, anchor="m")
    p.text(4.6, 6.08, 3.5, 0.3, "Range scales with speed²: ±75 rpm moves a 60 in shot about ±5.5 in. Together the errors use about two thirds of the opening.", size=6.5, color=GRAY)
    # bottom
    h2(p, 0.4, 6.5, 7.7, "What is different, how it works, what could go wrong")
    cols3 = [("WHAT IS DIFFERENT", ORANGE, ["Hood angle is **re-solved every loop from the measured wheel speed**, so a slightly slow wheel **still lands the ball**.",
                                      "A **tuned shot table** stores anchors at three distances (min / ideal / max); **projectile physics fills the gaps** instead of straight-line interpolation.",
                                      "Off-robot sim with drag and slip: lands within 0.4 in between anchors, where linear interpolation missed by up to 38 in."]),
             ("HOW IT WORKS", BLUE, ["For each tuned shot we store the ball speed per rpm (c). The planner solves the high-arc angle for the needed speed, converts it to a hood servo position through a calibration table, and offers a MIN, IDEAL and MAX shot.",
                                      "An index gate in front of the wheel releases balls only when we are ready; it blocks accidental feeds while the robot drives."]),
             ("RISKS WE MANAGE", "D64545", ["Servo positions drift, so hood calibration is a table with a tuner OpMode, not a formula.",
                                              "Drag and spin are not in the math, so the physics only fills between measured anchors.",
                                              "Hood arrival is not yet awaited in code; it is on our open list (p14)."])]
    for i, (t, c, items) in enumerate(cols3):
        x = 0.4 + i * 2.58
        p.rect(x, 6.82, 2.5, 0.22, fill=c, r=0.05)
        p.text(x, 6.82, 2.5, 0.22, t, size=6.8, color="FFFFFF", head=True, align="c", anchor="m")
        p.text(x, 7.08, 2.5, 2.1, ["• " + z for z in items], size=7.3, color=INK, gap=4)
    h2(p, 0.4, 8.4, 7.7, "A ball is released only when all four checks pass")
    flow(p, 0.4, 8.72, 7.7, [("IN RANGE", "Inside a legal launch distance for the shot table"), ("SPEED IN BAND", "Measured wheel speed within 90 rpm of target"),
                              ("HOOD THERE", "Hood re-solved from measured speed and arrived"), ("TURRET ON", "Within 1.5° of the aim point, including the lead")],
         colors=["6C4BC1", ORANGE, BLUE, "2E9E5B"])
    note(p, 0.4, 9.68, 3.75, 0.48, "Flywheel step-response / recovery trace from the FlywheelTuner (rpm vs. time, ball-by-ball dip)")
    note(p, 4.25, 9.68, 3.85, 0.48, "Shot-table anchors and hood calibration points measured on the robot (distance, rpm, hood)")
    p.text(0.4, 10.2, 7.7, 0.4, "Numbers on this page are derived from the CAD field geometry (muzzle height 10.63 in, opening center 56.7 in) and drag-free projectile motion: v² = g·d² / (2cos²θ(d·tanθ − Δh)). "
           "They size the hood and flywheel; the shot table replaces them with measured values.", size=6.6, color=GRAY)


# =========================================================== 13 TURRET + INTAKE
def p13():
    p = D.page(name="p13")
    chrome(p, 13, "Turret, Intake & FLOWER", "eng", ["CONTROL", "INNOVATE", "DESIGN"], "Engineering")
    h2(p, 0.4, 0.92, 7.7, "Turret: a cascade controller that leads a moving target")
    p.text(0.4, 1.22, 7.7, 0.4, "**Problem:** the HIVE moves and so do we. A turret that only chases the angle error lags; one that is told how the chassis is moving can lead. "
           "**How it works:** an outer position loop sets a velocity, feedforward adds the motion we already know about, and an inner velocity loop drives the motor.", size=7.6, color=INK)
    bx_y = 1.82
    box(p, 0.4, bx_y, 1.3, 0.78, "TARGET", "Which CELL (by field half) → aim at the middle of the opening", line="6C4BC1")
    box(p, 1.95, bx_y, 1.3, 0.78, "ERROR", "Bearing to target minus turret angle (wrapped)", line=BLUE)
    box(p, 3.5, bx_y, 1.45, 0.78, "POSITION LOOP", "kP 9.0 rad/s per rad, max 8 rad/s, tolerance 1.5°", line=BLUE)
    box(p, 5.2, bx_y, 1.35, 0.78, "VELOCITY LOOP", "kP 0.02 · kV 0.033 · kS 0.06 · kA 0.002, accel limit 60 rad/s²", line=ORANGE)
    box(p, 6.8, bx_y, 1.3, 0.78, "MOTOR", "Power capped at 0.85; 32:1 gear train; ±200°", fill=NAVY, line=NAVY, tc="FFFFFF")
    for x1, x2 in [(1.7, 1.95), (3.25, 3.5), (4.95, 5.2), (6.55, 6.8)]:
        p.line(x1, bx_y + 0.39, x2, bx_y + 0.39, color=NAVY, w=1.5, arrow=True)
    box(p, 3.5, 2.85, 3.05, 0.62, "FEEDFORWARD STACK", "Chassis rotation + chassis translation (line-of-sight sweep) + driver input × 0.5", fill="FFF6E0", line=ORANGE)
    p.line(5.0, 2.85, 5.6, bx_y + 0.78, color=ORANGE, w=1.5, arrow=True)
    box(p, 0.4, 2.85, 2.8, 0.62, "SENSORS", "Motor encoder (28 tick/rev) and absolute encoder (4,000 tick/rev, 4:1 up); velocity = 50/50 blend, motor reading dropped if they disagree by > 1.5 rad/s", fill="EAF6EF", line="2E9E5B", bsize=6)
    p.line(2.9, 2.85, 2.6, bx_y + 0.78, color="2E9E5B", w=1.5, arrow=True)
    p.image(A + 'turret.png', 6.7, 2.8, 1.4, 0.72, fit='cover', r=0.06)
    # lower: turret facts / intake
    h2(p, 0.4, 3.62, 3.75, "Turret: why and what we risk")
    p.text(0.4, 3.94, 3.75, 1.8,
           ["• **Why a turret:** tracking the HIVE without turning the chassis lets the driver keep scoring while being pushed, and enables shooting on the move (p14).",
            "• **Why a motor and 32:1 gears (9→60, 15→72):** speed and torque for a velocity loop, and soft limits at ±200° protect the cable chain.",
            "• **Unique feedforward:** the line-of-sight sweep term predicts how fast the target bearing changes as the robot translates.",
            "• **Risk:** zeroing. The absolute encoder is wired, but seeding is off until verified, so we stow the turret by hand before INIT. A CSV-logging tuner (721 lines) tunes the gains."],
           size=6.9, color=INK, gap=2)
    h2(p, 4.35, 3.62, 3.75, "Intake & transfer")
    # chain diagram
    chain = [("NOSE", "pivot servos"), ("STAGE 1-2", "intake motor"), ("STAGE 3-4", "transfer motor"), ("GATE", "servo"), ("FLYWHEEL", "4 in")]
    for i, (a, b) in enumerate(chain):
        x = 4.35 + i * 0.76
        p.text(x, 3.96, 0.72, 0.5, [dict(text=a, size=5.8, head=True, color="FFFFFF"), dict(text=b, size=5.4, color="FFFFFF")], fill=[BLUE, BLUE, BLUE, ORANGE, NAVY][i], r=0.05, align="c", anchor="m", gap=0, margin=(0.01, 0, 0.01, 0))
        if i < 4:
            p.line(x + 0.72, 4.21, x + 0.76, 4.21, color=NAVY, w=1.2, arrow=True)
    for i in range(4):
        p.oval(4.62 + i * 0.5, 4.52, 0.13, 0.13, fill="2E9E5B")
        p.text(4.5 + i * 0.5, 4.64, 0.4, 0.15, "ball%d" % (i + 1), size=5.2, color=GRAY, align="c", margin=(0, 0, 0, 0))
    p.text(4.35, 4.84, 3.75, 0.9,
           ["• **4 beam-break switches count 0-4 exactly** (the rule limit is 4), so there is no color guessing and no inferred count.",
            "• **Jam detection** from intake / transfer encoder speed; EJECT reverses the path.",
            "• Modes: IDLE · COLLECT · EJECT · SHOOT, run only through commands."],
           size=6.9, color=INK, gap=2)
    h2(p, 0.4, 5.78, 3.75, "FLOWER ramp")
    p.text(0.4, 6.1, 3.75, 1.3,
           ["One servo swings a ramp 32° down to the tiles (about 12 in stand-off) so POLLEN in a FLOWER can be harvested.",
            "**Interlock:** the ramp and the intake take turns in software, so they can never fight over the same space. Our sim says FLOWER harvesting is worth little, so it stays light.",
            "**How harvesting works:** with the ramp out, the intake stays stowed and **holding collect** spins the rollers, which pulls POLLEN up the ramp out of a FLOWER's retrieval opening, one at a time from the bottom. We **park nose-in, about 12 in from the FLOWER**."],
           size=7.2, color=INK, gap=3)
    p.image(A + 'flower.png', 4.35, 5.84, 1.85, 1.28, fit='cover', r=0.07)
    p.image(A + 'mech1.png', 6.25, 5.84, 1.85, 1.28, fit='cover', r=0.07)
    p.text(4.35, 7.14, 3.75, 0.2, "FLOWER ramp (left) · another CAD view (right), from the pit display", size=5.8, color=GRAY, align="c")
    h2(p, 0.4, 7.5, 7.7, "What makes it dependable")
    rows = [("Hood + turret + feedforward as one aiming system", "The hood solves where the ball must go, the turret leads the target, the planner re-solves each loop: aim is a calculation, not a feel."),
            ("One speed band, hood does distance", "Fewer large speed changes means shorter spin-up between shots (p12)."),
            ("Exact count by switches, no sensors guessing", "Four cheap switches replaced color sensors; the count is a fact."),
            ("Safe behaviors", "Over-speed cuts power and never reverses the wheel; intake and FLOWER ramp are interlocked; a stale pose (over 5 min) is flagged, never silently reused.")]
    y = 7.8
    for (a, b) in rows:
        p.rect(0.4, y, 7.7, 0.4, fill="FFFFFF", line=LG, r=0.04)
        p.text(0.5, y, 2.5, 0.4, a, size=7, color=BLUE, bold=True, anchor="m")
        p.text(3.05, y, 5.0, 0.4, b, size=6.9, color=INK, anchor="m")
        y += 0.43
    note(p, 0.4, 9.6, 3.75, 0.55, "Turret tracking log: error (deg) while driving and while pushed; tuned gains")
    note(p, 4.35, 9.6, 3.75, 0.55, "Intake test results: cycle time, jam rate, balls per second from the robot")
    p.text(0.4, 10.24, 7.7, 0.32, "All gains above are the values in our current code; Panels edits are pasted back into code after tuning so the repository stays the source of truth.", size=6.5, color=GRAY)


# =========================================================== 14 SOFTWARE
def p14():
    p = D.page(name="p14")
    chrome(p, 14, "Software & Controls", "eng", ["CONTROL", "THINK", "INNOVATE"], "Engineering")
    h2(p, 0.4, 0.92, 3.9, "Software architecture")
    layers = [("OPMODES", "TeleOp Red / Blue · Auto Red / Blue · tuners · Tune-0 checklist", "6C4BC1"),
              ("COMMANDS", "FireCommand · TrackHive · TeleOpDrive · TriggerIntake · FollowPath · HarvestFlower", BLUE),
              ("SUBSYSTEMS", "Drivetrain · Intake · Turret · Shooter (+hood, gate) · FLOWER · LEDs · OctoQuad hub", ORANGE),
              ("SERVICES", "ShotPlanner · ShotTable · field model (HIVE, CELLs) · feedforward stack · pose storage", "2E9E5B"),
              ("HARDWARE", "Control Hub + Expansion Hub · 8 motors · 5 servos · OctoQuad · pods · switches", NAVY)]
    for i, (a, b, c) in enumerate(layers):
        y = 1.26 + i * 0.5
        p.rect(0.4, y, 3.9, 0.45, fill=c, r=0.06)
        p.text(0.45, y, 0.95, 0.45, a, size=6.8, color="FFFFFF", head=True, anchor="m")
        p.text(1.4, y, 2.88, 0.45, b, size=6.4, color="FFFFFF", anchor="m")
    p.text(0.4, 3.78, 3.9, 0.55, "Subsystems never reference each other, so a failing mechanism cannot crash another; commands combine them. FTC SDK 12 · SolversLib command-based · Pedro Pathing 3 (Foresight) · Panels · AdvantageScope logging.", size=6.6, color=GRAY)
    h2(p, 4.45, 0.92, 3.65, "Loop order (the 20 ms lesson)")
    seq = [("1", "Clear bulk-read caches; one OctoQuad bulk read"), ("2", "Scheduler: subsystems READ, commands EXECUTE, subsystems WRITE"), ("3", "Apply path follower update after commands decide"), ("4", "Telemetry flush (20 Hz, rate-limited)")]
    for i, (n, t) in enumerate(seq):
        y = 1.26 + i * 0.5
        p.hexa(4.45, y, 0.42, 0.4, fill=ORANGE)
        p.text(4.45, y, 0.42, 0.4, n, size=9, color="FFFFFF", head=True, align="c", anchor="m", margin=(0, 0, 0, 0))
        p.text(4.95, y, 3.15, 0.42, t, size=6.9, color=INK, anchor="m")
        if i < 3:
            p.line(4.66, y + 0.4, 4.66, y + 0.5, color=NAVY, w=1.2)
    p.text(4.45, 3.3, 3.65, 1.0, "**Why:** putting the follower update inside the drivetrain subsystem applies the previous loop's sticks, about one loop (20 ms) of avoidable input lag. We fixed the order and wrote down why.", size=6.9, color=INK, fill=CREAM, line=ORANGE, r=0.07, margin=(0.1, 0.04, 0.08, 0.04), anchor="m")
    # control table
    h2(p, 0.4, 4.45, 7.7, "Problem and solution, system by system")
    cols = [("COMPONENT", 1.35), ("PROBLEM IT SOLVES", 2.3), ("HOW IT WORKS", 4.05)]
    x = 0.4
    for c, w in cols:
        p.text(x, 4.76, w - 0.04, 0.2, c, size=6.3, color="FFFFFF", head=True, fill=NAVY, anchor="m", margin=(0.08, 0, 0.04, 0), r=0.04)
        x += w
    rows = [("Localization", "Know where we are within an inch, all match", "**Two dead-wheel pods → OctoQuad MK2 → Pedro localizer** with IMU fusion; pose **handed from AUTO to TELEOP** and marked stale after 5 min"),
            ("Path following", "Follow curved paths without overshoot", "Pedro 3 Foresight: tuned top speed 72 in/s fwd / 46 in/s strafe, decel 30 in/s², heading kP 6.8 (piecewise translational gains)"),
            ("Shot planner", "Pick turret angle, hood and speed for any spot, even moving", "**Virtual goal** = goal − robot velocity × flight time; **3 fixed-point iterations**; **0.08 s** latency lead; pivot velocity includes ω × r"),
            ("Target selector", "The HIVE flips, so the target moves ~21 in", "Pick the CELL on our half of the field (split at y = 72 in with 4 in hysteresis); aim at the bisector of the opening"),
            ("Ball logic", "Never hold more than 4; clear jams", "4 switches count; encoder speed flags a jam; commands gate SHOOT on count and ready state"),
            ("Autonomous", "Score a preload volley, then park, every time", "State machine: preload shoot → pickups → shoot → park; a clock override parks with a 3 s reserve (LEAVE 3 + PARK 5). Timings are being tuned on the robot")]
    y = 4.98
    for (a, b, c) in rows:
        p.rect(0.4, y, 7.7, 0.44, fill="FFFFFF", line=LG, r=0.04)
        p.text(0.4, y, 1.31, 0.44, a, size=7, color=BLUE, bold=True, anchor="m", margin=(0.08, 0, 0.02, 0))
        p.text(1.75, y, 2.26, 0.44, b, size=6.6, color=INK, anchor="m")
        p.text(4.05, y, 4.0, 0.44, c, size=6.4, color=INK, anchor="m")
        y += 0.47
    # SOTM diagram
    h2(p, 0.4, 7.86, 3.9, "Shoot on the move: the virtual goal")
    card(p, 0.4, 8.18, 3.9, 1.45, fill="F4F7FC")
    p.text(0.45, 8.2, 3.8, 0.22, "virtual = goal − v_pivot × time-of-flight(distance)", size=6.6, color=NAVY, bold=True, anchor="m")
    gy = 8.95
    def cell(cx, cy, fill, line, lw):
        p.poly([(cx - 0.25, cy - 0.12), (cx - 0.25, cy + 0.1), (cx + 0.25, cy + 0.1), (cx + 0.25, cy - 0.12), (cx + 0.18, cy - 0.12), (cx + 0.18, cy + 0.02), (cx - 0.18, cy + 0.02), (cx - 0.18, cy - 0.12)], fill=fill, line=line, lw=lw)
    cell(3.65, gy, HONEY, NAVY, 1)
    cell(2.55, gy, None, ORANGE, 1.4)
    p.text(3.25, gy - 0.4, 0.85, 0.2, "real CELL", size=6, color=NAVY, bold=True, align="c")
    p.text(2.05, gy - 0.4, 1.0, 0.2, "virtual goal", size=6, color=ORANGE, bold=True, align="c")
    p.line(3.35, gy - 0.18, 2.88, gy - 0.18, color=ORANGE, w=1.2, arrow=True)
    p.rect(0.65, 9.22, 0.34, 0.26, fill=NAVY, r=0.03)
    p.line(1.0, 9.35, 2.0, 9.35, color="2E9E5B", w=2.2, arrow=True)
    p.text(1.05, 9.38, 1.1, 0.18, "v = 30 in/s", size=6.2, color="2E9E5B", bold=True)
    p.line(0.85, 9.22, 2.5, gy + 0.14, color=ORANGE, w=1.2, dash=True)
    p.text(2.15, 9.2, 2.1, 0.4, "At 30 in/s and ~1 s of flight the ball drifts ~30 in, more than the 20 in opening.", size=6, color=GRAY)
    h2(p, 4.45, 7.86, 3.65, "UML: structure at a glance")
    p.image(A + 'uml3.png', 4.45, 8.18, 3.65, 1.45, fit='contain', border=LG)
    p.text(4.45, 9.65, 3.65, 0.3, "Shooting, feedforward, field and math packages (1 of 4 class diagrams, Oct 12).", size=5.8, color=GRAY, align="c")
    h2(p, 0.4, 9.97, 7.7, "Tuning workflow")
    p.text(0.4, 10.25, 7.7, 0.34, "TUNING.md bring-up order: desk work first (ShotSolverBench needs no robot) → drive & odometry → turret → flywheel → shot table → autonomous. Tune-0 OpMode shows DONE / STOCK / TODO / CHECK.", size=6.6, color=INK)
    note(p, 5.0, 9.99, 0, 0, "") if False else None


# =========================================================== 15 SIMULATION
def p15():
    p = D.page(name="p15")
    chrome(p, 15, "Simulation & Validation", "eng", ["THINK", "CONTROL", "INNOVATE"], "Engineering")
    p.text(0.4, 0.9, 7.7, 0.55, "We built **BiobuzzSim**, a driver-practice and engineering simulator of the BIOBUZZ field, because the best test is **the one you can run 30,000 times before cutting metal.** "
           "The field and robot come from our own CAD, and the game rules come from the manual, so the sim is a model we can argue with.", size=8.2, color=INK)
    p.image(A + 'sim_ai.png', 0.4, 1.55, 4.7, 2.6, fit='cover', r=0.08, border=LG)
    p.image(A + 'sim_path.png', 5.2, 1.55, 2.9, 1.28, fit='cover', r=0.08, border=LG)
    p.image(A + 'robot_explode.png', 5.2, 2.87, 2.9, 1.28, fit='cover', r=0.08, border=LG)
    p.text(0.4, 4.17, 7.7, 0.2, "WATCH-AI page with the bot's reasoning panel · an AI driver's path (green/orange) · exploded CAD in the pit display", size=5.8, color=GRAY, align="c")
    h2(p, 0.4, 4.4, 7.7, "Pipeline: CAD → physics → rules → AI → decisions")
    pipe = [("ONSHAPE CAD", "Field 138 MB → 0.65 MB; robot 310 MB → 4 MB, split into chassis / turret / hood / intake / ramp", "6C4BC1"),
            ("PHYSICS", "Rapier at 120 Hz; HIVE latch, swing 4.5 s, tip model; shot feasibility with worst-case error corners", BLUE),
            ("RULES", "Scoring from manual 10.5; defenders at 3 strengths; 4 drivers in multiplayer", ORANGE),
            ("AI DRIVERS", "CMA-ES (156 params) and a residual neural network trained with PPO in plain JavaScript", "2E9E5B"),
            ("DECISIONS", "Hood 70-85°, one intake, turret feedforward, shot planner design", "D6457A")]
    for i, (a, b, c) in enumerate(pipe):
        x = 0.4 + i * 1.54
        p.hexa(x, 4.74, 1.5, 0.36, fill=c)
        p.text(x, 4.74, 1.5, 0.36, a, size=6.6, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.1, 0, 0.1, 0))
        p.text(x, 5.14, 1.5, 0.88, b, size=6.3, color=INK, align="c")
    h2(p, 0.4, 6.08, 3.8, "What the AI learned")
    res = [("AI vs. no defense", 458, "458", "2E9E5B"), ("AI vs. Light", 397, "397", "2E9E5B"), ("AI vs. Medium", 385, "385", ORANGE), ("AI vs. Lockdown", 379, "379", "D64545"), ("Human-reflex baseline", 361, "361", GRAY)]
    for i, (a, v, t, c) in enumerate(res):
        yy = 6.4 + i * 0.28
        p.text(0.4, yy, 1.35, 0.24, a, size=6.6, color=INK, anchor="m")
        p.rect(1.8, yy + 0.04, 1.8 * v / 458, 0.16, fill=c, r=0.03)
        p.text(1.85 + 1.8 * v / 458, yy, 0.5, 0.24, t, size=6.6, color=c, head=True, anchor="m")
    p.text(0.4, 7.82, 3.8, 0.4, "Average points per match, held-out random seeds, 4.5 s TIP rule. These are simulated scores from our AI driver, not robot results.", size=6.2, color=GRAY)
    h2(p, 4.35, 6.08, 3.75, "Insights we acted on")
    ins = [("+111", "points from shooting on the move, so we built the turret feedforward", "2E9E5B"), ("−181", "points if the driver reacts 250 ms late, so more automation, less reflex", "D64545"),
           ("0", "FLOWER pickups in the best run, so the ramp stays small", ORANGE), ("25/25", "of 25 reachable grid spots go in; 25 of 35 positions have any shot", BLUE)]
    for i, (a, b, c) in enumerate(ins):
        yy = 6.4 + i * 0.4
        p.hexa(4.35, yy, 0.7, 0.34, fill=c)
        p.text(4.35, yy, 0.7, 0.34, a, size=8, color="FFFFFF", head=True, align="c", anchor="m", margin=(0.08, 0, 0.08, 0))
        p.text(5.12, yy - 0.02, 2.98, 0.38, b, size=6.6, color=INK, anchor="m")
    h2(p, 0.4, 8.3, 7.7, "How we trust a model: verification")
    chk = [("check:shots", "Every shot is swept against real colliders with worst-case launch error"), ("field:verify", "Fails if decimating the CAD moves any surface more than 6 mm"),
           ("Measured HIVE", "Sag 0.10°, drift 0.15° at 97% load, swing 4.42 s for 60°"), ("npm test", "Smoke, API, AI, multiplayer and worker tests; UI checked at 5 window sizes"),
           ("Gradient check", "Neural-net backprop verified against numerical gradients"), ("Held-out seeds", "Scores reported on matches the AI never trained on")]
    for i, (a, b) in enumerate(chk):
        x = 0.4 + (i % 3) * 2.58
        y = 8.62 + (i // 3) * 0.55
        p.text(x, y, 2.5, 0.5, [dict(text=a, bold=True, size=6.9, color=BLUE), dict(text=b, size=6.3, color=INK)], fill="FFFFFF", line=LG, r=0.05, margin=(0.08, 0.02, 0.05, 0.02), anchor="m", gap=0)
    h2(p, 0.4, 9.76, 7.7, "Limits, and how the robot closes the loop")
    p.text(0.4, 10.06, 7.7, 0.52, "The sim is not the robot: its drivers are AIs, scores are not match results, and drag/spin are simplified. Next, we compare simulated and measured shots at the same positions "
           "and feed the shot table and cycle times back into the model so both agree.", size=7, color=INK)



import sys
_names = ["cover", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15"]
for _n in _names:
    ORANGE = ACCENT[_n]
    globals()[_n]()
