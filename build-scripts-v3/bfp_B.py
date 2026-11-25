from bfkit import *
import math

INK = "1D2433"
SKY, PUR = ("38BFF2", "7664B8")
TXT = "353132"


OUTD = '/Users/sumeetsethi/FTC-Portfolio-2026/images/outreach/'


def logo_ph(k, x, y, w, h, r=6, fill="F2F4F7"):
    k.rect(x, y, w, h, fill=fill, line="C5CCD6", lw=0.6, r=r, dash=True)
    k.text(x, y, w, h, "LOGO", pt=5.5, color="8A94A3", head=True, align="c", anchor="m")


def pie(k, cx, cy, r, parts, start=-90):
    """parts: [(frac, color)] clockwise from start deg"""
    a = start
    for fr, col in parts:
        n = max(6, int(fr * 90))
        pts = [(cx, cy)]
        for i in range(n + 1):
            t = math.radians(a + 360 * fr * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        k.poly(pts, fill=col, line=None)
        a += 360 * fr


def dot_leg(k, x, y, d, col, label, pt=9.5, w=260):
    k.dot(x + d / 2, y + d / 2, d, col)
    k.text(x + d + 8, y - 4, w, d + 8, label, pt=pt, color="1A3F28", head=True, anchor="m")


# ======================================================================= 04
def page_04(D):
    p = D.page(name='p04'); k = K(p)
    G, GL = "00A561", "2EA957"
    k.rect(0, 99, 655, 1653, fill=G)
    k.rect(48, 127, 98, 145, fill=GL)
    k.dot(97, 200, 106, "FFFFFF")
    k.text(45, 130, 104, 140, "$", pt=34, color=G, head=True, align="c", anchor="m")
    k.text(168, 118, 480, 120, "Business", pt=42, color="FFFFFF", anchor="m")
    k.text(168, 232, 480, 34, "2025-26: +$14,761.74 net, --- sponsors", pt=10.5, color="FFFFFF", anchor="m")
    # media coverage
    k.text(30, 277, 330, 46, "Media Coverage", pt=16, color="FFFFFF", anchor="m")
    W = "FFFFFF"
    k.text(25, 325, 298, 585, ["We have made efforts to create a **local brand**. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud **exercitation** ullamco laboris. " + dummy(8),
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu **fugiat nulla** pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt.",
        "Sed ut perspiciatis unde omnis iste natus error sit **voluptatem** accusantium doloremque laudantium, totam rem aperiam."], pt=8.4, color=W, gap=14)
    for (y, h) in [(287, 143), (466, 148), (656, 148)]:
        k.photo_ph(346, y, 297, h, "article or press photo")
        k.text(346, y + h + 2, 297, 22, "Caption (to add)", pt=7, color=W, align="c", anchor="m")
    # statistics panel
    k.rect(10, 925, 635, 820, fill="FFFFFF")
    k.text(32, 934, 300, 50, "Statistics", pt=17.5, color=TXT, anchor="m")
    D1, D2, D3 = "1E5B32", "2FA24D", "1A4528"
    pie(k, 158, 1112, 119, [(0.82, D1), (0.18, D2)])
    k.text(70, 1032, 90, 44, "18%", pt=13, color="FFFFFF", head=True, align="c", anchor="m")
    k.text(128, 1100, 110, 50, "82%", pt=17, color="6BC86C", head=True, align="c", anchor="m")
    dot_leg(k, 322, 1084, 32, D1, "Sponsors")
    dot_leg(k, 322, 1119, 32, D2, "Member dues")
    cols = ["1A4528", "1E5B32", "258543", "2EA958", "6BC86C", "91D686", "AFE1A2"]
    pie(k, 158, 1366, 119, [(0.585, cols[0]), (0.415, cols[2])])
    k.text(150, 1325, 100, 50, "58%", pt=16, color="6BC86C", head=True, align="c", anchor="m")
    k.text(76, 1385, 100, 50, "42%", pt=16, color="FFFFFF", head=True, align="c", anchor="m")
    ly = 1252
    for c, lab in zip(cols[:5], ["Robot parts", "Registration", "Travel (to add)", "Outreach (to add)", "Tools (to add)"]):
        dot_leg(k, 322, ly, 32, c, lab, w=250)
        ly += 35 if lab != "Travel (to add)" else 35
    # area chart (placeholder shape)
    cx0, cx1, cy0, cy1 = 78, 620, 1522, 1678
    k.line(cx0, cy0, cx0, cy1, color=TXT, w=1.0)
    k.line(cx0, cy1, cx1, cy1, color=TXT, w=1.0)
    for i, lab in enumerate(["50k", "40k", "30k", "20k", "10k", "0"]):
        k.text(20, cy0 - 12 + i * 31.2, 50, 24, "---", pt=7, color=TXT, align="r", anchor="m")
    for i in (1, 2, 3):
        k.line(cx0, cy0 + 31 * i, cx1, cy0 + 31 * i, color=TXT, w=0.8, dash=True)
    ms = ["May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"]
    n = len(ms)
    xs = [cx0 + 12 + i * (cx1 - cx0 - 24) / (n - 1) for i in range(n)]
    top = [1645, 1622, 1648, 1630, 1618, 1638, 1580, 1552, 1602]
    low = [1658, 1645, 1665, 1660, 1630, 1650, 1665, 1630, 1650]
    k.poly([(xs[i], top[i]) for i in range(n)] + [(xs[-1], cy1), (xs[0], cy1)], fill="1E5B32")
    k.poly([(xs[i], low[i]) for i in range(n)] + [(xs[-1], cy1), (xs[0], cy1)], fill="2FA24D")
    for x, m in zip(xs, ms):
        k.text(x - 25, cy1 + 2, 50, 22, m, pt=7, color=TXT, align="c", anchor="m")
    k.text(88, 1494, 400, 24, "Monthly spending (USD, data to add)", pt=8, color=TXT, head=True, anchor="m")
    k.dot(154, 1716, 30, D1); k.text(176, 1702, 180, 30, "Spending", pt=9.5, color="1A3F28", head=True, anchor="m")
    k.dot(396, 1716, 30, D2); k.text(418, 1702, 200, 30, "Income", pt=11, color="1A3F28", head=True, anchor="m")

    # right column
    k.text(675, 142, 600, 60, "How we raised", pt=18, color=TXT, anchor="m")
    k.text(672, 192, 620, 76, "$18,300 USD?", pt=24, color=G, head=True, anchor="m")
    for (x, y, t) in [(675, 292, "Objectives"), (675, 668, "Planning"), (996, 592, "Portfolio"), (996, 980, "Discussions"), (675, 1035, "Fundraising")]:
        k.text(x, y, 330, 46, t, pt=17.5, color=TXT, anchor="m")
    B = dict(pt=8.4, color=TXT)
    k.text(668, 338, 298, 300, "Performance also involves **efficient management** of financial resources. Every penny of our budget represents not just a simple economic value, but also **an investment in innovation**. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore **magna aliqua**.", **B)
    k.text(989, 338, 298, 240, "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. **Excepteur sint** occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.", **B)
    k.text(668, 713, 298, 300, "Starting from the belief that **a well-forecasted budget** is a powerful tool, lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in **reprehenderit** in voluptate velit esse cillum.", **B)
    k.text(989, 634, 298, 340, "For approaching sponsors via email or other forms of contact, we have created a **personalized sponsorship portfolio**. This season **SendCutSend, Fabworks, 3Dconnexion, OnlineMetals, Apple and Costco** support us with discounts, CAD tools, and funding for parts and travel. " + dummy(6), **B)
    k.text(989, 1022, 298, 320, "Alongside our mentors, we created **our own marketing strategy**. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse **cillum dolore**.", **B)
    # quote
    quote_mark(k, 668, 1122, "007199", bar=False)
    k.text(745, 1100, 222, 100, "Quote about asking for support (to add) -Name", pt=11, color="007199", ls=1.0)
    k.line(668, 1205, 964, 1205, color="555555", w=0.8, dash=True)
    k.text(668, 1219, 298, 140, "Through periodic visits, event invitations, and updates on the team's progress, we **keep previous season sponsors** alongside us. Lorem ipsum.", **B)
    # logo grid: this season's sponsors first, then slots for earlier sponsors
    SP = "/Users/sumeetsethi/FTC-Portfolio-2026/images/sponsors/"
    def sp_logo(x, y, w, h, name, pad=8):
        k.rect(x, y, w, h, fill="FFFFFF", line="C5CCD6", lw=0.6, r=6)
        k.image(SP + name + ".png", x + pad, y + pad, w - 2 * pad, h - 2 * pad, fit="contain")
    k.text(668, 1346, 298, 22, "This season", pt=7.5, color=TXT, head=True, anchor="m")
    sp_logo(668, 1372, 145, 50, "sendcutsend"); sp_logo(821, 1372, 145, 50, "fabworks")
    sp_logo(668, 1430, 145, 50, "3dconnexion"); sp_logo(821, 1430, 145, 50, "onlinemetals")
    sp_logo(668, 1488, 60, 62, "apple", pad=6); sp_logo(736, 1488, 145, 62, "costco")
    logo_ph(k, 889, 1488, 77, 62)
    k.text(668, 1560, 298, 22, "Earlier seasons", pt=7.5, color=TXT, head=True, anchor="m")
    for y, h, items in [(1586, 62, [(668 + i * 123, 112) for i in range(5)]),
                        (1656, 62, [(668 + i * 77, 70) for i in range(4)])]:
        for x, w in items:
            logo_ph(k, x, y, w, h)
    k.header(4, [("inspire", SKY, "000000"), ("connect", PUR, "000000")])


def ev_img(n):
    return n + ".png"


def quote_mark(k, x, y, col, bar=True):
    for dx in (0, 34):
        k.dot(x + 14 + dx, y + 18, 28, col)
        k.poly([(x + dx + 2, y + 22), (x + dx + 28, y + 22), (x + dx + 14, y + 52)], fill=col)
    if bar: k.rect(x + 60, y - 40, 3, 100, fill=col)


# ======================================================================= 05
def cap_in(k, x, y, w, h, t):
    k.rect(x + 8, y + h - 32, w - 16, 24, fill="000000", r=6, alpha=0.55)
    k.text(x + 8, y + h - 32, w - 16, 24, t, pt=6.5, color="FFFFFF", align="c", anchor="m")


def pin(k, x, y, col="2E2A2B"):
    k.poly([(x - 7, y - 22), (x + 7, y - 22), (x + 7, y - 8), (x + 14, y - 8), (x, y + 8), (x - 14, y - 8), (x - 7, y - 8)], fill=col)


def map_shape(k, ox, oy, sc=1.0):
    """clean simplified placeholder map of the Bay Area region (ox,oy = top-left, 270 x 400 px)"""
    land = [(60, 0), (200, 20), (262, 110), (270, 250), (220, 370), (110, 400), (20, 330), (0, 180), (20, 60)]
    k.poly([(ox + a, oy + b) for a, b in land], fill="FED304", line="000000", lw=2.2)
    for (px, py, lab) in [(50, 50, "North Bay"), (50, 115, "East Bay"), (50, 180, "Peninsula"), (50, 245, "San José"), (50, 310, "Fremont")]:
        pin(k, ox + px, oy + py + 20)
        k.text(ox + px + 26, oy + py + 8, 130, 22, lab, pt=7.5, color="2E2A2B", anchor="m")


def hdr5(k):
    s = 1.4396
    k.text(25 * s, 14 * s, 300, 44 * s, [dict(text="FIRST® TECH CHALLENGE", head=True, size=7 * FONT, color="1D2433"), dict(text="BIOBUZZ presented by RTX", size=6.5 * FONT, color="3A3F4A")], anchor="m", gap=0)
    k.image(LOGO, 1178, 16, 114, 71, fit="contain")
    k.text(870, 14, 295, 36, "%s **%s**" % (TEAM, NUM), pt=11, color="1D2433", anchor="m", align="r")
    k.text(870, 48, 295, 30, SEASON, pt=9.5, color="3A3F4A", anchor="m", align="r")
    x = 330
    for lab, fill, w in [("inspire", SKY, 133), ("connect", PUR, 152), ("motivate", "D452B0", 152)]:
        k.rect(x, 30, w, 37, fill=fill, line="000000", lw=1.25, r=18.5)
        k.text(x, 30, w, 37, lab, pt=10, color="000000", bold=True, head=True, align="c", anchor="m")
        k.line(x + w, 49, x + w + 25, 49, color="000000", w=1.5)
        x += w + 25
    k.line(x, 49, 915, 49, color="000000", w=1.5)
    k.line(0, 98, SW, 98, color="000000", w=1.0)
    k.oval(SW - 52 - 27, 1785 - 27, 54, 54, fill="000000")
    k.text(SW - 52 - 27, 1785 - 27, 54, 54, "5", pt=9, color="FFFFFF", head=True, align="c", anchor="m")


def page_05(D):
    p = D.page(name='p05'); k = K(p)
    k.header(5, [("inspire", SKY, "000000"), ("connect", PUR, "000000"), ("motivate", "D452B0", "000000")])
    def stripes(y, h):
        k.rect(0, y, 1310, h, fill="214BA0")
    stripes(100, 17); stripes(1331, 17); stripes(1738, 14)
    # title block
    k.dot(148, 146, 30, "FED304")
    k.rect(140, 160, 16, 10, fill="2E2A2B", r=2)
    k.text(38, 150, 400, 70, [dict(text="Inspire Bay Area", head=True)], pt=19, color="2E2A2B", anchor="m")
    k.text(40, 210, 520, 40, "1000+ people, 300+ hours, 20+ venues", pt=10, color="2E2A2B", head=True, anchor="m")
    for i, lg in enumerate(["basf_logo", "chm_logo", "cdm_logo", "svreads_logo", "scouts_logo", "stratford_logo"]):
        k.rect(435 + i * 144, 152, 130, 66, fill="F2F4F7", line="D5DAE0", lw=0.8, r=6)
        k.image(OUTD + lg + ".png", 435 + i * 144 + 8, 156, 114, 58, fit="contain")
    k.line(25, 175, 25, 232, color="777777", w=0.8, dash=True)
    # banner and column photos
    k.image(A + "ev_camp.png", 25, 251, 939, 319, r=14)
    caps = ["Kids driving a robot with controllers", "Library room with a small field", "Students building at an open build", "Two kids driving a small robot", "Stratford Fremont demo: new drivers found", "Featured on KQED News"]
    for i, f in enumerate(["ev_kids", "ev_lib", "ev_open", "ev_simple", OUTD + "stratford_event", OUTD + "kqed_science_festival"]):
        y = [251, 429, 607, 782, 957, 1132][i]
        if f:
            k.image((f if f.startswith('/') else A + f) + ".png", 989, y, 297, 166, r=14, focus=(0.5, 0.5))
            cap_in(k, 989, y, 297, 166, caps[i])
        else: k.photo_ph(989, y, 297, 166, "event photo")
    # quote
    quote_mark(k, 25, 668, "007199")
    k.text(102, 596, 222, 140, "Quote from a partner, teacher or parent (to add). -Name, Role, Organization", pt=9.5, color="007199")
    k.line(25, 760, 322, 760, color="555555", w=0.8, dash=True)
    B = dict(pt=8.4, color=TXT)
    k.text(25, 783, 298, 360, "Our team started three years ago when we branched from our FRC program, FRC team 254, Bellarmine's Cheesy Poofs. We have **walked the journey on our own** since then. This season we focused on **new connections with our community**: museums, schools, San Jose public services and, through FIRST, partners across the world. At the Stratford Fremont demo, a First Middle School event with alumni on our team, we even found new drivers for our robot.", **B)
    k.text(347, 596, 250, 220, "We went to the **World Championship** after being finalists in the Silicon division. Many of our former partners have invited us back, including the **San Jose libraries** and the **Computer History Museum**.", pt=8.4, color=TXT)
    k.text(668, 596, 298, 260, "We mentor teams outside our own. Every week we help the **CHA middle school team**. We also coach **Code Crackers** at St. Clare MS and mentor the Graham MS FLL team in a **9 month long mentorship**. We also taught programming basics to students in Bangladesh for 6 months, with the nonprofit Agami.", **B)
    k.rect(350, 850, 246, 310, fill="F2F4F7", line="D5DAE0", lw=0.8, r=10)
    k.image(OUTD + "outreach_poster.png", 356, 856, 234, 298, fit="contain")
    # outreach by the numbers (from the outreach poster)
    k.rect(612, 880, 354, 280, fill="F2F4F7", line="D5DAE0", lw=0.8, r=10)
    k.text(626, 884, 330, 36, "Outreach by the numbers", pt=11, color="2E2A2B", head=True, anchor="m")
    for i, (n, l1, l2) in enumerate([("400+", "Bay Area Science Festival", "40 volunteer hours"), ("200+", "Discovery Museum", "90 volunteer hours"),
                                     ("200+", "San Jose Public Libraries", "10 volunteers, 90 hours"), ("100+", "CHM Techfest", "50 volunteer hours"),
                                     ("50+", "Scout-O-Rama", "20 volunteer hours")]):
        y = 926 + i * 46
        k.text(624, y, 100, 46, n, pt=17, color=PUR, head=True, anchor="m")
        k.line(726, y + 6, 726, y + 40, color=PUR, w=0.8, dash=True)
        k.text(736, y - 2, 224, 22, l1, pt=8.6, color="2E2A2B", bold=True, anchor="m")
        k.text(736, y + 20, 224, 22, l2, pt=8, color=TXT, anchor="m")
    k.text(25, 1183, 298, 140, "Rookie teams 23229 Cheesy Strings and 23230 Cheesy Wheels started from our open builds. **Lorem ipsum** dolor sit amet.", **B)
    k.text(347, 1183, 250, 140, "Our rookie pipeline: **open builds, apply, own team** in year one, then veteran team, then lead or mentor.", pt=8.4, color=TXT)
    # event block
    k.text(38, 1355, 700, 66, "Techfest @ CHM", pt=21, color="2E2A2B", head=True, anchor="m")
    k.text(38, 1404, 940, 40, "Computer History Museum, 100+ attendees, 50 volunteer hours", pt=11, color="2E2A2B", head=True, anchor="m")
    k.line(25, 1370, 25, 1440, color="777777", w=0.8, dash=True)
    k.text(25, 1462, 298, 280, "Techfest was a **major Silicon Valley tech showcase**. We hosted a booth and showed our robot to more than 100 attendees. Our students put in **50 volunteer hours** across the event, explaining the robot to visitors of all ages.", **B)
    k.text(347, 1462, 298, 280, "We were **personally invited** to return every year, and we will be **returning next month**. Techfest is one of our best chances to show the public what a FIRST robot can do.", **B)
    k.text(668, 1462, 298, 280, "Visitors drove the robot and asked how to join FIRST. Lorem ipsum dolor sit amet, consectetur **adipiscing elit**, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.", **B)
    k.image(A + "ev_demo.png", 989, 1381, 297, 342, r=14, focus=(0.5, 0.5))


# ======================================================================= 06
def reactions(k, ox, oy):
    k.dot(1073, 1655, 130, "EF335F")
    for dx in (-17, 17):
        k.dot(1073 + dx, 1640, 38, "FFFFFF")
    k.poly([(1042, 1648), (1104, 1648), (1073, 1690)], fill="FFFFFF")
    k.dot(1166, 1617, 60, "6680C8")
    k.rect(1153, 1612, 8, 22, fill="FFFFFF"); k.rect(1163, 1604, 14, 30, fill="FFFFFF", r=4)
    k.dot(1012, 1700, 62, "F9D54D")
    k.dot(1131, 1690, 62, "F9D54D")
    for dx in (-12, 12):
        k.dot(1131 + dx, 1683, 14, "EF335F")
    k.rect(1119, 1698, 24, 14, fill="3A2A2A", r=6)
    k.dot(1190, 1668, 40, "F9D54D")


def card_title(k, x, y, w, h, t, pt=15):
    k.rect(x, y, w, h, fill="FFFFFF" if x < 100 else PUR, r=20)
    k.text(x + 10, y, w - 14, h, t, pt=pt, color=PUR if x < 100 else "FFFFFF", anchor="m", ls=1.0)


def num_stat(k, x, y, n, l1, l2, white=False):
    c = "FFFFFF" if white else PUR
    k.text(x, y - 33, 50, 100, n, pt=30, color=c, anchor="m")
    k.line(x + 38, y + 4, x + 38, y + 44, color=c, w=0.8, dash=True)
    k.text(x + 48, y - 2, 270, 26, l1, pt=9, color=c, bold=True, anchor="m")
    k.text(x + 48, y + 20, 270, 26, l2, pt=9, color=c, bold=True, anchor="m")


def page_06(D):
    p = D.page(name='p06'); k = K(p)
    k.rect(0, 99, 655, 1653, fill=PUR)
    k.dot(97, 195, 106, "FFFFFF")
    for (cx, cy) in [(88, 160), (100, 190), (92, 220)]:
        k.oval(cx - 12, cy - 15, 26, 30, line=PUR, lw=3.0)
    k.text(168, 125, 480, 120, "Connect", pt=42, color="FFFFFF", anchor="m")
    k.text(168, 226, 480, 34, "6 events, 1000+ people, --- likes", pt=10.5, color="FFFFFF", anchor="m")
    k.rect(12, 291, 630, 187, fill="FFFFFF", r=10)
    k.text(28, 296, 606, 178, "In the past year, Cheesy Chips has become a **visible part** of the FIRST community in the Bay Area, with collaborations with museums, libraries and schools. We spread interest in engineering through **engaging demonstrations**: in local museums, at schools, with San Jose public services and internationally through FIRST. Many of our former partners, including the **San Jose libraries** and the **Computer History Museum**, have reached out to invite us back. In the future we hope to sustain these connections and increase our influence in our local community.", pt=8.7, color=TXT, anchor="m")
    B = dict(pt=8.4, color=TXT)
    W = dict(pt=8.4, color="FFFFFF")
    # card 1
    card_title(k, 20, 487, 622, 97, "Techfest at the Computer History Museum", pt=13)
    num_stat(k, 28, 604, "1", "100+ attendees", "50 volunteer hours", True)
    k.text(25, 664, 296, 330, "We hosted a booth at a major Silicon Valley tech showcase and were **personally invited back** to return every year. We showed the robot to more than 100 attendees, and our students put in **50 volunteer hours** at the booth. Visitors drove the robot and asked how to join FIRST. We are **returning next month**. Techfest is one of our best chances to show the public what FIRST students can build, and we hope to sustain this connection and increase our influence in our local community.", **W)
    k.rect(25, 1010, 296, 183, fill="FFFFFF", r=14)
    k.image(OUTD + "chm_logo.png", 40, 1022, 125, 125, fit="contain", r=8)
    k.image(OUTD + "techfest_logo.png", 181, 1022, 125, 125, fit="contain", r=8)
    k.text(25, 1152, 296, 36, "Computer History Museum Techfest", pt=7, color="231F20", align="c", anchor="m")
    k.image(A + "ev_demo.png", 346, 657, 297, 168, r=14)
    k.photo_ph(346, 841, 297, 168, "Techfest photo")
    k.photo_ph(346, 1025, 297, 168, "Techfest photo")
    # card 2
    card_title(k, 20, 1225, 622, 85, "Bay Area Science Festival")
    num_stat(k, 28, 1319, "2", "400+ attendees", "40 volunteer hours", True)
    k.text(25, 1388, 296, 345, "Visitors drove our robot. We told elementary families about **FLL** and invited rookie teams. The festival drew **400+ attendees**, and our team put in **40 volunteer hours**. We were **featured on KQED News**, which brought more families to our exhibit. It was a great way to meet the community and share what robotics can do.", **W)
    k.image(OUTD + "kqed_science_festival.png", 346, 1347, 297, 168, r=14)
    k.text(346, 1517, 297, 22, "Featured on KQED News", pt=7, color="FFFFFF", align="c", anchor="m")
    k.rect(346, 1540, 297, 168, fill="FFFFFF", r=14)
    k.image(OUTD + "basf_logo.png", 396, 1548, 197, 152, fit="contain")
    k.text(346, 1710, 297, 22, "Bay Area Science Festival exhibitor", pt=7, color="FFFFFF", align="c", anchor="m")
    # right cards
    def rcard(x, ty, th, title, n, l1, l2, img, cap, text):
        card_title(k, x, ty, 296, th, title, pt=13.5)
        num_stat(k, x - 1, ty + th + 8, n, l1, l2)
        if img: k.image(A + img, x, ty + th + 58, 296, 167, r=14)
        else: k.photo_ph(x, ty + th + 58, 296, 167, "event photo")
        k.text(x, ty + th + 227, 296, 22, cap, pt=7, color=TXT, align="c", anchor="m")
        k.text(x, ty + th + 252, 296, 345, text, **B)
    rcard(668, 122, 128, "Fremont Main Library joint event", "3", "3 Bay Area teams", "October 11", "ev_lib.png", "Library room with a small field",
          "On October 11 we held a joint event with **Astrobruins** and **Quixilver**. Three Bay Area teams shared one exhibit. Kids and families drove each team's robot and compared the designs, so one visit showed several ways to solve the same game.")
    rcard(989, 122, 128, "ChezyHacks hackathon", "4", "7 teams", "Date (to add)", None, "Caption (to add)",
          "We hosted **ChezyHacks**, a schoolwide hackathon. It was about **teamwork**, time management and presenting new ideas. A **Meta engineer from New York** mentored the teams and judged. Students left with working projects and a clearer idea of what engineers do.")
    rcard(668, 745, 128, "Children's Discovery Museum", "5", "200+ attendees", "90 volunteer hours", "ev_kids.png", "Kids driving a robot with controllers",
          "We spent two weekends supporting the **23224 exhibit** at the Children's Discovery Museum. We built a kit so kids could assemble a drivebase and drive it. **200+ attendees** visited, and our team put in **90 volunteer hours** over the two weekends.")
    rcard(989, 745, 128, "Autumn Cleanup with Beautify SJ", "6", "Off-season robot", "Date (to add)", None, "Caption (to add)",
          "We reused an off-season robot to **pick up trash**. It showed kids that robotics can solve real-world problems, and it gave our team a way to give back to the city of San Jose. We joined the **Beautify SJ** autumn cleanup with a robot built for the job.")
    k.rect(668, 1340, 300, 395, fill="FFFFFF", line="D5DAE0", lw=0.8, r=10)
    k.image(OUTD + "outreach_poster.png", 676, 1347, 284, 380, fit="contain")
    k.text(995, 1380, 300, 200, [dict(text="--- ", head=True), dict(text="likes")], pt=36, color="000000", ls=0.95, gap=0)
    reactions(k, 988, 1585)
    k.header(6, [("inspire", SKY, "000000"), ("connect", PUR, "000000")])
