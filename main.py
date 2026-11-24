#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Monday 23 November 2026.
Draws a 1024x1024 news broadsheet PNG, stdlib only, no network.
Deterministic: same bytes on every run.
Usage: MAKEFUN_OUTPUT_DIR=/output python3 main.py
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font: 5x7 bitmap, uppercase only
# Each glyph: 7 rows of 5 chars, '#' = ink.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '*': ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    '[': ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    ']': ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    '|': ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    '\\': ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
}

PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (11, 42, 74)
NAVY_LT = (23, 68, 110)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
SKY = (186, 214, 235)
SKY_DK = (120, 165, 205)
GREEN = (27, 120, 60)
GREY = (110, 110, 105)
WHITE = (255, 255, 255)
CREAM = (255, 252, 244)

# ---------------------------------------------------------------- canvas
buf = bytearray(W * H * 3)
for i in range(W * H):
    buf[i * 3:i * 3 + 3] = bytes(PAPER)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        buf[o:o + 3] = bytes(c)


def fill_rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        o = (yy * W + x0) * 3
        buf[o:(o + (x1 - x0) * 3)] = bytes(c) * (x1 - x0)


def hline(x, y, w, c, t=1):
    fill_rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    fill_rect(x, y, t, h, c)


def ellipse(cx, cy, rx, ry, c):
    for dy in range(-ry, ry + 1):
        if rx == 0 or ry == 0:
            continue
        dx = int(rx * (1 - (dy / ry) ** 2) ** 0.5)
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)


def circle(cx, cy, r, c):
    ellipse(cx, cy, r, r, c)


def text(s, x, y, scale=2, c=INK, spacing=None):
    """Draw uppercase text; returns width in px."""
    if spacing is None:
        spacing = scale
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == '1':
                    fill_rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 5 * scale + spacing
    return cx - x - spacing if s else 0


def text_w(s, scale=2, spacing=None):
    if spacing is None:
        spacing = scale
    return len(s) * (5 * scale + spacing) - spacing if s else 0


def text_center(s, y, scale=2, c=INK, spacing=None, cx=W // 2):
    w = text_w(s, scale, spacing)
    text(s, cx - w // 2, y, scale, c, spacing)


def wrap(s, max_chars):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(s, x, y, max_chars, scale=2, c=INK, spacing=None, leading=2):
    lines = wrap(s, max_chars)
    lh = 7 * scale + leading
    for i, ln in enumerate(lines):
        text(ln, x, y + i * lh, scale, c, spacing)
    return y + len(lines) * lh


# ---------------------------------------------------------------- PNG encoder
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def write_png(path):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter none
        raw += buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


# ---------------------------------------------------------------- content
LEADS = [
    {
        "kicker": "CLIMATE",
        "head": "COP31 COLLAPSES:",
        "head2": "'WORST COP EVER'",
        "body": "UN CHIEF: DEEP DISAPPOINTMENT. 190 NATIONS FAIL IN ANTALYA. COP32 IN ADDIS ABABA, 2027.",
        "kind": "cop",
    },
    {
        "kicker": "UKRAINE",
        "head": "KYIV REGION:",
        "head2": "AT LEAST 14 DEAD",
        "body": "BOY, 7, PULLED ALIVE FROM DYMER FLATS AS TOLL THERE HITS 11. 23 NOV A DAY OF MOURNING.",
        "kind": "kyiv",
    },
    {
        "kicker": "LIBYA",
        "head": "RUSSIAN WARSHIP",
        "head2": "SINKS AT BENGHAZI",
        "body": "CORVETTE MERKURY BURNS AFTER SUSPECTED DRONE BLAST. UN DEMANDS SWIFT, INDEPENDENT PROBE.",
        "kind": "ship",
    },
]

MEDIUM = [
    ("NATO HOLDS EMERGENCY MEETING", "OVER RUSSIAN MISSILES IN POLAND"),
    ("BAHRAIN SEEKS UN ACTION ON IRAN", "DEMANDS FULL DAMAGES FOR SITRA HIT"),
    ("UKRAINE HITS RUSSIAN OIL SITES", "PUMP STATION, REFINERY STRUCK"),
    ("SAUDI SHADOW OVER COP31 FAILURE", "REUTERS: RIYADH BLOCKED FOSSIL TEXT"),
    ("INDONESIA CANDY FACTORY FIRE: 24 DEAD", "ABOUT 30 STILL MISSING IN CIKANDE"),
    ("HUANG BACK AS NVIDIA CEO", "SHARES SOAR ABOUT 30% ON MONDAY"),
    ("OIL SLIPS AS AI SELL-OFF SPREADS", "BRENT $92.29 IN ASIAN TRADE"),
    ("'EL CHAPO ISIDRO' ARREST RISKS WAR", "CARTEL SUCCESSION FEARS IN MEXICO"),
    ("ASIAN MARKETS SLIDE ON TECH FEARS", "KOSPI SINKS 4% AT THE OPEN"),
    ("TAJIKISTAN QUITS THE ICC", "EU REGRETS MOVE; EFFECTIVE 2027"),
    ("IRAN STILL OPEN TO US DEAL", "FOREIGN MINISTER ARAGHCHI SAYS"),
    ("HOUTHIS TARGET SAUDI ARABIA", "DRONE, MISSILE INTERCEPTED"),
]

ALSO = [
    "ODESA SCHOOLS GO REMOTE",
    "KHARKIV DRONE WOUNDS 2",
    "MALTA SHIP HIT, BENGHAZI",
    "SPARTA II LEAVES FINLAND",
    "GRIPEN PILOT HELD ITS FIRE",
    "2 TANKERS HIT NEAR HORMUZ",
    "IRGC CLAIMS MQ-9 DOWNED",
    "SAUDI CONDEMNS IRAN ATTACK",
    "LEBANON SEIZES EXPLOSIVES",
    "MBS MEETS BULGARIA PM",
    "PAKISTAN EYES US-IRAN DEAL",
    "NEPAL PM MEETS MODI",
    "NZ-INDIA TEST ENDS IN DRAW",
    "MANILA TRANSPORT STRIKE",
    "VISAYAS GRID ON RED ALERT",
    "RAINS OVER LUZON, MINDANAO",
    "49ERS ROUT VIKINGS 35-10",
    "LIONS, BEARS BOTH 8-2",
    "BILLS, COWBOYS WIN BIG",
    "KC, CAROLINA, PHILLY WIN",
    "GIANTS HOLD OFF JAGUARS",
    "CHICAGO FED INDEX -0.06",
    "AP TOP 25: GEORGIA NO. 1",
    "HEAT WIN 7TH STRAIGHT",
    "SABRES BEAT LIGHTNING 6-2",
    "REAL MADRID TOP CELTA 2-1",
    "ALCARAZ REACHES ATP FINAL",
    "KANSAS CITY WIN NWSL",
    "RIEMANN PROOF CERTIFIED",
    "MARIANA TRENCH VOLCANOES",
    "JONATHAN, 194: DNA CLUES",
    "MILKY WAY RECORD SIM",
    "GOOGLE GEOTHERMAL DEAL",
    "ZIPLINE HIRES UBER EXEC",
    "BACTERIA MAKE LIPIDS",
    "PRIME EDITING MATURES",
    "MRI MAPS PEAT MOSS TIPS",
    "BANGLADESH PLANS NEW SMES",
    "GOLD RISES TO $3,604 AM",
    "HERBERT CONCUSSION CHECK",
    "BRONCOS BEAT RAIDERS 38-24",
    "GAZA STRIKE KILLS 3",
    "UN, US SLAM KHARTOUM HIT",
    "SETTLER ARSON CONDEMNED",
    "GERMAN PMI HITS 55.0",
]

# ---------------------------------------------------------------- drawing
def draw_map_strip(y0, y1):
    fill_rect(0, y0, W, y1 - y0, SKY)
    # simple world silhouette: dark navy blobs
    ellipse(150, y0 + 14, 95, 12, NAVY)    # N America
    ellipse(120, y0 + 26, 45, 8, NAVY)
    ellipse(300, y0 + 28, 30, 13, NAVY)    # S America
    ellipse(520, y0 + 12, 35, 9, NAVY)     # Europe
    ellipse(545, y0 + 28, 42, 13, NAVY)    # Africa
    ellipse(700, y0 + 14, 130, 13, NAVY)   # Asia
    ellipse(820, y0 + 20, 70, 9, NAVY)
    ellipse(880, y0 + 30, 32, 7, NAVY)     # Australia
    # graticule ticks
    for gx in range(64, W, 128):
        vline(gx, y0, y1 - y0, SKY_DK, 1)


def draw_lead_art(kind, x, y, w, h):
    fill_rect(x, y, w, h, SKY)
    if kind == "cop":
        # globe with a crack + rising smoke
        circle(x + w // 2, y + h // 2 + 4, 34, NAVY_LT)
        ellipse(x + w // 2 - 20, y + h // 2 - 8, 18, 6, GREEN)
        ellipse(x + w // 2 + 8, y + h // 2 + 12, 16, 5, GREEN)
        fill_rect(x + w // 2 - 2, y + 8, 4, 30, RED)
        fill_rect(x + w // 2 - 10, y + 14, 4, 18, RED)
        fill_rect(x + w // 2 + 6, y + 12, 4, 22, RED)
        circle(x + w // 2, y + h - 6, 3, GOLD)
    elif kind == "kyiv":
        # damaged apartment block + rescue ladder
        fill_rect(x + 28, y + 18, 90, h - 26, NAVY)
        for fy in range(4):
            for fx in range(4):
                fill_rect(x + 36 + fx * 22, y + 24 + fy * 16, 12, 9, GOLD)
        fill_rect(x + 96, y + 18, 22, 22, INK)  # broken corner
        fill_rect(x + 150, y + 30, 60, 8, RED)
        fill_rect(x + 150, y + 44, 44, 8, RED)
        fill_rect(x + 210, y + 58, 26, 8, RED)
        # ladder leaning on the building's right edge
        vline(x + 122, y + 40, h - 48, INK, 3)
        vline(x + 134, y + 40, h - 48, INK, 3)
        for ly in range(y + 48, y + h - 8, 10):
            hline(x + 122, ly, 15, INK, 2)
    else:  # ship
        # sinking corvette, bow up, stern low, smoke
        fill_rect(x + 40, y + 46, 190, 16, NAVY)
        fill_rect(x + 40, y + 30, 60, 16, NAVY)
        fill_rect(x + 180, y + 56, 50, 10, NAVY)
        vline(x + 90, y + 18, 30, INK, 4)
        fill_rect(x + 94, y + 18, 26, 12, RED)
        circle(x + 150, y + 14, 8, GREY)
        circle(x + 166, y + 8, 6, GREY)
        # waves
        for wx in range(x + 8, x + w - 8, 26):
            fill_rect(wx, y + h - 14, 16, 4, SKY_DK)
            fill_rect(wx + 8, y + h - 8, 16, 4, SKY_DK)


def section_label(s, y, c=RED):
    fill_rect(12, y, 8, 14, c)
    text(s, 28, y, scale=2, c=INK)
    hline(12, y + 18, W - 24, INK, 2)


def render():
    # ---- header band
    fill_rect(0, 0, W, 112, NAVY)
    fill_rect(0, 112, W, 4, GOLD)
    text_center("MONDAY 23 NOVEMBER 2026", 16, scale=4, c=WHITE)
    text_center("THE WORLD IN ONE DAY  -  60 STORIES", 62, scale=2, c=GOLD)
    # ---- world map strip
    draw_map_strip(116, 156)
    # ---- LEAD
    section_label("TOP STORIES", 164)
    px0, pw, ph = 12, 324, 224
    py = 188
    for i, lead in enumerate(LEADS):
        x = px0 + i * (pw + 10)
        fill_rect(x, py, pw, ph, CREAM)
        fill_rect(x, py, pw, 4, RED)
        # kicker
        text(lead["kicker"], x + 10, py + 12, scale=2, c=RED)
        draw_lead_art(lead["kind"], x + 10, py + 34, pw - 20, 76)
        yy = py + 120
        text(lead["head"], x + 10, yy, scale=2, c=INK)
        text(lead["head2"], x + 10, yy + 16, scale=2, c=INK)
        para(lead["body"], x + 10, yy + 38, 27, scale=2, c=INK, spacing=1)
    # ---- MEDIUM
    section_label("MORE NEWS", 420)
    mx0, mw, mh, mgap = 12, 494, 36, 12
    my = 444
    for i, (h1, h2) in enumerate(MEDIUM):
        col, row = i % 2, i // 2
        x = mx0 + col * (mw + mgap)
        y = my + row * (mh + 2)
        fill_rect(x, y, 3, mh, NAVY_LT)
        text(h1, x + 10, y + 2, scale=2, c=INK, spacing=1)
        text(h2, x + 10, y + 19, scale=2, c=GREY, spacing=1)
    # ---- ALSO TODAY
    section_label("ALSO TODAY", 676)
    ax0, aw = 12, 328
    ay = 700
    for i, item in enumerate(ALSO):
        col, row = i % 3, i // 3
        x = ax0 + col * (aw + 6)
        y = ay + row * 17
        num = str(16 + i) + "."
        text(num, x, y, scale=2, c=RED, spacing=1)
        text(item, x + 4 * 11, y, scale=2, c=INK, spacing=1)
    # ---- MARKETS strip
    fill_rect(12, 960, W - 24, 2, GOLD)
    text_center("S&P 500 7,237.17 +4.73%   NASDAQ 24,089.56 +6.51%   DOW 49,595.31 +3.01%",
                966, scale=2, c=INK, spacing=1)
    text_center("NVIDIA +31.48% $165.05   KOSPI -3.31% CLOSE   GOLD $3,671.80   BRENT $89.10   15:20 UTC",
                982, scale=2, c=INK, spacing=1)
    # ---- footer
    text_center("ALL STORIES HAPPENED OR FIRST REPORTED 23 NOV 2026",
                1004, scale=2, c=INK, spacing=1)


def main():
    render()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    n = write_png(path)
    print(f"wrote {path} ({n} bytes)")


if __name__ == "__main__":
    main()
