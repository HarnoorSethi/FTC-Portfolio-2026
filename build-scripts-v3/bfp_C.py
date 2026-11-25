from bfkit import *
import math
OUTD = '/Users/sumeetsethi/FTC-Portfolio-2026/images/outreach/'

INK = "231F20"
CAPC = "3A3A3A"
PURPLE = "7664B8"
MAG = "D452B0"
SKY = "38BFF2"
CHIPTXT = "2E2A2B"
LS = 1.12      # line spacing so 7.6pt text sits on the reference 22px pitch
BODY = 7.9


def dm(n):
    return dummy(n).replace(",.", ".")


def chips(k, odd, specs):
    """specs = [(label, fill, x, w, y)], connector lines like the reference"""
    k.line(0 if not odd else 250, 49, 1010 if not odd else 1010, 49, color="231F20", w=1.2)
    for lab, fill, x, w, y in specs:
        k.rect(x, y, w, 39, fill=fill, line="231F20", lw=1.4, r=19.5)
        k.text(x, y, w, 39, lab, pt=9.2, color=CHIPTXT, bold=True, head=True, align="c", anchor="m")


def head(k, n, odd, specs):
    k.header(n, [(lab, fill, CHIPTXT) for lab, fill, x, w, y in specs])


def card(k, x, y, col, title, num, s1, s2, photo, cap, desc, desc_h, w=296, th=128, ph=167, pgap=57,
         white=False, photo_focus=(0.5, 0.5), tpt=12.2, show_title=True):
    """ByteForce numbered card: coloured title box, big thin number + dashed rule + 2-line stat, photo, caption, text"""
    if show_title:
        k.rect(x, y, w, th, fill=col, r=18)
        k.text(x, y, w, th, title, pt=tpt, color="FFFFFF", anchor="t", margin=(10, 12, 8, 4), ls=1.18)
    ny = y + th + 2
    k.text(x + 6, ny - 4, 70, 80, str(num), pt=27, color=col, anchor="t", margin=(0, 0, 0, 0))
    two = len(str(num)) > 1
    ox = 72 if two else 49
    k.line(x + ox, ny + 8, x + ox, ny + 46, color=col, w=0.7, dash=True)
    k.text(x + ox + 4, ny + 2, w - ox - 6, 48, [s1, s2], pt=7.6, color=col, bold=True, gap=0, anchor="m", ls=1.05)
    py = y + th + pgap
    if photo:
        k.image(photo if photo.startswith('/') else A + photo, x, py, w, ph, fit="cover", r=12, focus=photo_focus)
    else:
        k.photo_ph(x, py, w, ph, label=cap, r=12)
    k.text(x, py + ph + 3, w, 20, cap, pt=6.6, color=CAPC, align="c", anchor="m")
    k.text(x, py + ph + 28, w, desc_h, desc, pt=BODY, color=INK, ls=LS, gap=0)


def mini_card(k, x, y, col, title, num, s1, s2, logo, desc, desc_h, w=296, th=56):
    """a compact version of card(): no photo, the organisation's logo sits in the title box"""
    k.rect(x, y, w, th, fill=col, r=18)
    k.text(x, y, w - 66, th, title, pt=11.2, color="FFFFFF", anchor="m", margin=(10, 0, 4, 0), ls=1.1)
    k.rect(x + w - 54, y + 5, 46, 46, fill="FFFFFF", r=10)
    k.image(OUTD + logo, x + w - 51, y + 8, 40, 40, fit="contain")
    ny = y + th + 2
    k.text(x + 6, ny - 4, 70, 80, str(num), pt=27, color=col, anchor="t", margin=(0, 0, 0, 0))
    ox = 72
    k.line(x + ox, ny + 8, x + ox, ny + 46, color=col, w=0.7, dash=True)
    k.text(x + ox + 4, ny + 2, w - ox - 6, 48, [s1, s2], pt=7.6, color=col, bold=True, gap=0, anchor="m", ls=1.05)
    k.text(x, ny + 52, w, desc_h, desc, pt=BODY, color=INK, ls=LS, gap=0)


def rot(pts, cx, cy, ang):
    a = math.radians(ang)
    return [(cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a), cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a)) for px, py in pts]


def rrpoly(x, y, w, h, r, n=6):
    pts = []
    for (cx, cy, a0) in [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ============================================================ PAGE 7
def page_07(D):
    p = D.page(name='p07'); k = K(p)
    head(k, 7, True, [("inspire", SKY, 300, 135, 30), ("connect", PURPLE, 464, 153, 29)])
    # headline
    k.text(33, 190, 350, 100, "300+h", pt=33, color="231F20", head=True, margin=(0, 0, 0, 0))
    k.text(33, 275, 470, 100, "outreach", pt=31, color="231F20", margin=(0, 0, 0, 0))
    k.image(R + "hero_front_right.png", 360, 130, 280, 230, fit="contain")
    P = PURPLE
    # left columns
    L = [
        (25, 390, 7, "Rose Garden Library", "Monthly program,", "First Thursday, 4:30 pm", "ev_lib.png", "A small field in a library room",
         "We bring our robot to the Rose Garden Library on the **first Thursday of every month**, from 4:30 to 5:30 pm. Kids and parents come to drive the robot. We tell families about FLL and FTC so older kids know what to do next. " + dm(10), 300),
        (346, 390, 8, "Berryessa Library", "Monthly program,", "Starting October 11, 3 pm", None, "ADD: photo from Berryessa",
         "We also run a monthly event at the **Berryessa Library**. The first one was on October 11 at 3 pm. Kids drive the robot and ask us how it works. " + dm(30), 300),
        (25, 1050, 9, "San Jose Public Library branches", "200+ attendees,", "10 volunteers, 90 hours", "ev_simple.png", "Two kids driving a small robot",
         "We visited other **San Jose Public Library** branches too, including Joyce Ellington, Dr. MLK, Biblioteca Latinoamericana, Willow Glen and Hillview. About **200 people** came to see the robot across nine branches, and 10 of our volunteers put in **90 hours**. The libraries have **invited us back**.", 250, (0.5, 0.9)),
        (346, 1050, 10, "Scout-O-Rama and Boy Scouts", "50+ attendees,", "20 volunteer hours", "ev_tent.png", "Outdoor booth with a robot on the ground",
         "At **Scout-O-Rama** we ran a booth for Boy Scouts and their families. We also run robotics merit badge workshops for scouts. Across the event we welcomed **50+ attendees** and put in **20 volunteer hours**.", 250),
    ]
    R_ = [
        (668, 122, 11, "The Tech Interactive", "100+ people,", "Date: ADD", "ev_demo.png", "A parent and kid at a robot demo table",
         "We brought our robot to **The Tech Interactive** in San Jose. Visitors could drive it and talk with our students about how it works. " + dm(32), 310),
        (989, 122, 12, "Chabot Space & Science Center", "Oakland,", "Date: ADD", None, "ADD: photo from Chabot",
         "We took our robot to the **Chabot Space & Science Center** in Oakland. " + dm(54), 310),
        (668, 857, 13, "Agami / Switch School in Bangladesh", "6 months,", "Virtual class", OUTD + "bangladesh_class.png", "Our virtual class with Switch School",
         "We taught a virtual coding class for **Agami / Switch School** in Bangladesh, together with codeMane and the nonprofit **Agami**. It ran for **6 months**, with a unit on game development.", 290),
        (989, 857, 14, "Taipei STEAM delegation", "Hosted with 23224,", "International", "ev_taiwan.png", "The delegation at our site",
         "We hosted a **STEAM delegation from Taipei** together with team 23224. It was **international collaboration through FIRST**.", 290),
    ]
    for it in L + R_:
        (x, y, n, t, s1, s2, ph, cap, d, dh) = it[:10]
        card(k, x, y, P, t, n, s1, s2, ph, cap, d, dh, photo_focus=(it[10] if len(it) > 10 else (0.5, 0.5)))
    mini_card(k, 668, 1412, P, "Stratford Fremont", 15, "First Middle School event,", "Alumni on the team", "stratford_logo.png",
              "We demonstrated our robot at **Stratford Fremont**, a First Middle School event with **alumni on our team**. Kids drove the robot, and we found new drivers.", 74)
    mini_card(k, 989, 1412, P, "St. Frances Cabrini", 16, "Robot demo,", "Date: ADD", "cabrini_logo.png",
              "We gave a **robot demo** at St. Frances Cabrini Catholic School. Students drove the robot and asked how it works.", 70)
    # bottom stat with phone
    k.text(745, 1600, 260, 80, "---", pt=30, color="231F20", head=True, margin=(0, 0, 0, 0))
    k.text(748, 1665, 300, 80, "posts", pt=28, color="231F20", margin=(0, 0, 0, 0))
    cx, cy, ang, sc_ = 1160, 1688, 20, 0.68
    def T(pts):
        return [(a_ * sc_ + cx, b_ * sc_ + cy) for a_, b_ in rot(pts, 0, 0, ang)]
    k.poly(T(rrpoly(-135, -70, 270, 140, 20)), fill="FFFFFF", line="231F20", lw=1.8)
    for r_ in range(3):
        for c_ in range(4):
            k.poly(T(rrpoly(-40 + c_ * 42, -60 + r_ * 42, 40, 40, 2, 2)), fill="FFFFFF", line="9AA0A6", lw=0.8)


# ============================================================ PAGE 8
def heart(k, cx, cy, s, color, lw=3.0):
    pts = []
    for i in range(61):
        t = math.pi * 2 * i / 60
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s, cy - y * s))
    k.curve(pts, color=color, w=lw)


def page_08(D):
    p = D.page(name='p08'); k = K(p)
    k.rect(0, 100, 656, 1652, fill=MAG)
    head(k, 8, False, [("inspire", SKY, 385, 135, 30), ("mentor", MAG, 548, 152, 28)])
    k.oval(28, 133, 107, 107, fill="FFFFFF")
    heart(k, 81, 187, 2.15, MAG)
    k.line(66, 183, 96, 205, color=MAG, w=2.2)
    k.line(71, 176, 101, 198, color=MAG, w=2.2)
    k.text(160, 118, 480, 100, "Mentoring", pt=29, color="FFFFFF", margin=(0, 0, 0, 0))
    k.text(158, 200, 480, 44, "5 mentored teams, 3 schools, 2 rookie teams", pt=9.5, color="FFFFFF", margin=(0, 0, 0, 0), anchor="m")
    k.rect(12, 266, 630, 196, fill="FFFFFF", r=14)
    k.text(12, 266, 630, 196,
           "The main goal of our mentoring is to help new teams start and keep going. **Exhibits spark interest, but teams make it last.** We help schools, coaches and parents start **FIRST programs**, from FLL to FTC. "
           "Our own team started three years ago, when we branched from our FRC program. We walked that journey on our own, so we know how hard it is to start. "
           "We **show up every week**.",
           pt=8.4, color=INK, margin=(14, 8, 14, 6), anchor="m", ls=1.08)
    k.rect(25, 472, 617, 84, fill="FFFFFF", r=14)
    k.text(25, 466, 617, 96, "We founded / mentored 5 teams this season", pt=12.5, color=MAG, anchor="m", margin=(12, 0, 10, 0), ls=1.18)
    # item 1 CHA
    k.text(33, 556, 40, 70, "1", pt=27, color="FFFFFF", margin=(0, 0, 0, 0))
    k.line(68, 572, 68, 610, color="FFFFFF", w=0.7, dash=True)
    k.text(76, 565, 566, 48, ["CHA middle school team, every Thursday at 3:40 pm,", "since September 10, 2026, one hour per session"], pt=8.4, color="FFFFFF", bold=True, gap=0, anchor="m", ls=1.05)
    k.text(25, 616, 297, 440,
           "Canyon Heights Academy (CHA) had no robotics team, so we helped start one. Our mentors meet the students **every Thursday at 3:40 pm** for one hour. By October 29 we had run **6 sessions**. On September 29 the students visited our lab for a tour. "
           "The mentors who work with students have completed VIRTUS safe-environment training. This is part of our plan to bring robotics to Catholic middle schools and the Jesuit school network, so students can move on to FLL and FTC later. " + dm(20),
           pt=BODY, color="FFFFFF", ls=LS, gap=0)
    k.text(347, 616, 297, 440,
           ["How do we mentor them?",
            "",
            "The students **own the build**. Our mentors ask questions instead of giving answers. We use starter kits and manuals, because building a drivebase from raw parts was not realistic. We come every week, because that helps more than one big event. "
            "We also look for a **local champion**, like a teacher or a parent, who keeps the team going. Number of students: ADD. " + dm(30)],
           pt=BODY, color="FFFFFF", ls=LS, gap=0)
    k.photo_ph(25, 1068, 297, 167, label="CHA students with our mentors", r=12)
    k.text(25, 1238, 297, 20, "ADD: CHA team photo", pt=6.6, color="FFFFFF", align="c", anchor="m")
    k.photo_ph(347, 1068, 297, 167, label="Lab tour on September 29", r=12)
    k.text(347, 1238, 297, 20, "ADD: lab tour photo", pt=6.6, color="FFFFFF", align="c", anchor="m")
    # item 2 rookies
    k.rect(25, 1277, 617, 84, fill="FFFFFF", r=14)
    k.text(25, 1271, 617, 96, "Rookie teams 23229 Cheesy Strings and 23230 Cheesy Wheels.", pt=12.5, color=MAG, anchor="m", margin=(12, 0, 10, 0), ls=1.18)
    k.text(33, 1360, 40, 70, "2", pt=27, color="FFFFFF", margin=(0, 0, 0, 0))
    k.line(68, 1376, 68, 1412, color="FFFFFF", w=0.7, dash=True)
    k.text(76, 1366, 566, 52, ["2 rookie FTC teams from Bellarmine,", "templates, tools and mentoring"], pt=8.4, color="FFFFFF", bold=True, gap=0, anchor="m", ls=1.05)
    k.text(25, 1418, 297, 335,
           "Our rookie pipeline has four steps. First, students join an **open build**. Then they apply. In year one they run their **own team**, 23229 Cheesy Strings or 23230 Cheesy Wheels. After that they join a veteran team, and later they can lead a team or become a mentor. "
           "We give the rookie teams our templates and tools, and we mentor them.",
           pt=BODY, color="FFFFFF", ls=LS, gap=0)
    k.text(347, 1418, 297, 124, "Both teams are new to FTC. " + dm(10), pt=BODY, color="FFFFFF", ls=LS, gap=0)
    k.image(A + "ev_open.png", 347, 1542, 297, 167, fit="cover", r=12)
    k.text(347, 1712, 297, 20, "Students building at a table", pt=6.6, color="FFFFFF", align="c", anchor="m")
    # right cards
    P = MAG
    cards = [
        (668, 148, 3, "Code Crackers at St. Clare Middle School", "Dec 1 and 12, 2025,", "and Sept 24, 2026", None, "ADD: photo from St. Clare",
         "Code Crackers is the robotics team at St. Clare Middle School, with a staff moderator. Our software and outreach members visit in small groups. Four of our members came in December. We **coach the students** on their own robot and code. We do not drive. The students keep ownership.", 310),
        (989, 148, 4, "Graham Middle School starts FLL", "9 month mentorship,", "Mountain View", None, "ADD: photo from Graham",
         "We introduced robotics to **Graham Middle School** in Mountain View and inspired them to start a **FIRST LEGO League** team. We helped students design and build drivebases. We mentor their FLL team in a **9 month long mentorship**, through the whole season. Day 1: form teams, start drivebase. Day 2: finish it and drive. Day 3: program it. Day 4: first challenge.", 310),
        (668, 857, 5, "Summer robotics camp", "6 weeks,", "Dates: ADD", "ev_camp.png", "Overhead view of a robot match",
         "We ran a **6 week robotics camp** with groups by age. Students built robots and competed with them. " + dm(36), 310),
        (989, 857, 6, "Joint library event with two teams", "3 teams, Oct 11,", "Fremont Main Library", None, "ADD: photo from the joint event",
         "On October 11 we ran a joint event with **Astrobruins** and **Quixilver** at the Fremont Main Library. Three Bay Area teams shared one exhibit. " + dm(34), 310),
    ]
    for (x, y, n, t, s1, s2, ph_, cap, d, dh) in cards:
        card(k, x, y, P, t, n, s1, s2, ph_, cap, d, dh, tpt=12.2)
    # bottom stat
    k.text(727, 1520, 380, 90, "---", pt=32, color="231F20", head=True, margin=(0, 0, 0, 0))
    k.text(727, 1585, 380, 70, "hours of", pt=24, color="231F20", margin=(0, 0, 0, 0))
    k.text(727, 1640, 380, 70, "mentoring", pt=24, color="231F20", margin=(0, 0, 0, 0))
    people(k)


def people(k, dy=-24):
    # woman (left)
    k.oval(1141, 1578 + dy, 26, 30, fill="E7B48C")
    k.rect(1136, 1572 + dy, 34, 20, fill="2A2A3A", r=10)
    k.rect(1130, 1610 + dy, 44, 74, fill="8AA0B0", r=12)
    k.rect(1136, 1684 + dy, 14, 60, fill="D9DCE0", r=4)
    k.rect(1156, 1684 + dy, 14, 60, fill="D9DCE0", r=4)
    # man (right)
    k.oval(1200, 1570 + dy, 28, 32, fill="E7B48C")
    k.rect(1196, 1562 + dy, 36, 18, fill="2A2A3A", r=9)
    k.rect(1186, 1606 + dy, 56, 78, fill="2E75C0", r=12)
    k.rect(1190, 1684 + dy, 20, 62, fill="1B4F94", r=4)
    k.rect(1218, 1684 + dy, 20, 62, fill="1B4F94", r=4)


# ============================================================ PAGE 9
def laptop(k):
    k.rect(380, 133, 196, 128, fill="2F3F59", r=6)
    k.rect(388, 141, 180, 112, fill="E9EDF2", r=2)
    xs = [392, 442, 492, 536]
    for r_ in range(2):
        for c_ in range(4):
            k.rect(392 + c_ * 44, 146 + r_ * 54, 40, 48, fill=["C9B6A8", "8FA7C4", "D9B8B0", "B7C5A8"][(r_ + c_) % 4], r=2)
    k.poly([(368, 262), (590, 262), (574, 292), (384, 292)], fill="D5D9DF", line="B5BAC2", lw=0.8)


def calendar(k, col):
    k.rect(705, 1600, 140, 124, fill="FFFFFF", line="231F20", lw=2.2, r=14)
    for x in (735, 790):
        k.rect(x, 1585, 22, 34, fill="FFFFFF", line="231F20", lw=2.2, r=7)
    n = 1
    for r_ in range(3):
        for c_ in range(4):
            if n > 10:
                break
            cx = 715 + c_ * 31
            cy = 1631 + r_ * 31
            k.rect(cx, cy, 28, 28, fill="D8EAF7", r=3)
            k.text(cx, cy, 28, 28, str(n), pt=8.5, color="3A8FD0", align="c", anchor="m")
            k.oval(cx - 4, cy - 2, 10, 10, fill=col, line="1F6FB5", lw=0.8)
            n += 1


def page_09(D):
    p = D.page(name='p09'); k = K(p)
    head(k, 9, True, [("inspire", SKY, 300, 135, 30), ("mentor", MAG, 464, 154, 29)])
    k.text(60, 118, 330, 90, "---", pt=28, color="231F20", head=True, margin=(0, 0, 0, 0))
    k.text(60, 178, 340, 70, "followers", pt=26, color="231F20", margin=(0, 0, 0, 0))
    k.text(60, 232, 330, 60, "on Instagram", pt=18, color="231F20", margin=(0, 0, 0, 0))
    laptop(k)
    P = MAG
    cards = [
        (25, 313, 7, "ChezyHacks hackathon", "7 teams,", "Date: ADD", None, "ADD: ChezyHacks photo",
         "We hosted **ChezyHacks**, a schoolwide hackathon. Seven teams took part. It was about teamwork, time management and presenting new ideas. A **Meta engineer from New York** mentored the teams and judged the projects.", 285),
        (346, 313, 8, "OpenSauce invitation", "Invited to bring the robot,", "Date: ADD", None, "ADD: OpenSauce photo",
         "We were invited to bring our robot to **OpenSauce**, a large maker and engineering expo. It lets us reach makers, engineers and families far beyond the FIRST community. " + dm(14), 285),
        (25, 965, 9, "Autumn cleanup with Beautify SJ", "Off-season robot,", "City of San Jose", None, "ADD: cleanup photo",
         "We joined the autumn cleanup with **Beautify SJ**. We used an off-season robot to pick up trash. It showed kids that robotics can solve real-world problems. " + dm(22), 330),
        (346, 965, 10, "Our Instagram page", "--- likes,", "--- followers", None, "ADD: screenshot of our page",
         "We share our events, builds and robot updates on **Instagram**. " + dm(40), 330),
        (668, 127, 11, "Mentoring at the library", "Monthly,", "San Jose libraries", None, "ADD: library mentoring photo",
         "The San Jose Public Library staff host us every month. At these events we also **mentor** kids who want to start a team. " + dm(42), 310),
        (989, 127, 12, "Warm Springs Elementary", "Date: ADD,", "--- students", None, "ADD: photo from Warm Springs",
         "We visited **Warm Springs Elementary**. " + dm(62), 310),
        (668, 865, 13, "Chezy Champs", "Date: ADD,", "--- teams", None, "ADD: Chezy Champs photo",
         "We took part in **Chezy Champs**. " + dm(52), 290),
        (989, 865, 14, "What is next on our plan", "4 ideas,", "More to come", None, "ADD: photo",
         "Our plan includes a **mentor-matching website** that connects mentors with FIRST teams that need them, more scrimmages with many teams, visits to an autism daycare with kitbots for children to build, and outreach in Guatemala through a mission trip and a nonprofit. " + dm(10), 290),
    ]
    for (x, y, n, t, s1, s2, ph_, cap, d, dh) in cards:
        card(k, x, y, P, t, n, s1, s2, ph_, cap, d, dh)
    calendar(k, "2A8FD6")
    k.text(865, 1585, 300, 80, "---", pt=29, color="231F20", head=True, margin=(0, 0, 0, 0))
    k.text(865, 1648, 300, 70, "likes", pt=27, color="231F20", margin=(0, 0, 0, 0))
