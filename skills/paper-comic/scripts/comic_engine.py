"""comic_engine.py — reusable engine for comic-magazine explainers of research papers.

Coordinates: each panel is placed in mm on an A4 page (210 x 297 mm). Inside a panel,
SVG drawing uses U = 4 units per mm (a 96 x 70 mm panel has viewBox 0 0 384 280).
Characters are drawn with their FEET at (x, y); s = scale (1.0 is about 30 mm tall).
"""
import os, subprocess, glob
import numpy as np

U = 4
INK = "#141414"
FONT_DIR = os.environ.get("COMIC_FONT_DIR", "/tmp/comic_fonts")


# ---------------------------------------------------------------- fonts
def ensure_fonts():
    """Download Bangers + Comic Neue (via npm) once. Falls back to system fonts if offline."""
    want = ["bangers-latin-400-normal.woff2", "comic-neue-latin-400-normal.woff2", "comic-neue-latin-700-normal.woff2"]
    found = {os.path.basename(p): p for p in glob.glob(f"{FONT_DIR}/**/*.woff2", recursive=True)}
    if all(w in found for w in want):
        return found
    os.makedirs(FONT_DIR, exist_ok=True)
    try:
        subprocess.run(["npm", "pack", "@fontsource/bangers", "@fontsource/comic-neue"], cwd=FONT_DIR,
                       check=True, capture_output=True)
        for t in glob.glob(f"{FONT_DIR}/*.tgz"):
            d = t[:-4]
            os.makedirs(d, exist_ok=True)
            subprocess.run(["tar", "xzf", t, "-C", d], check=True)
    except Exception as e:
        print("font download failed, using fallbacks:", e)
    return {os.path.basename(p): p for p in glob.glob(f"{FONT_DIR}/**/*.woff2", recursive=True)}


# ---------------------------------------------------------------- characters
def robot(x, y, s=1.0, mood="happy", arms="down", color="#29b6f6", label="1 RF", antenna=True, light="#e1f5fe"):
    """Hero robot (the system / device the paper studies). moods: happy worried surprised determined joy.
    arms: down up think. antenna=True draws a rail of ports on its head."""
    mouths = {
        "happy": f'<path d="M-11,-75 Q0,-64 11,-75" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
        "worried": f'<path d="M-10,-70 Q0,-78 10,-70" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                   f'<path d="M-18,-97 L-6,-94 M18,-97 L6,-94" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
        "surprised": f'<ellipse cx="0" cy="-72" rx="4.5" ry="6" fill="{INK}"/>',
        "determined": f'<path d="M-9,-72 L9,-72" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                      f'<path d="M-18,-96 L-6,-92 M18,-96 L6,-92" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>',
        "joy": f'<path d="M-12,-76 Q0,-60 12,-76 Z" fill="#c62828" stroke="{INK}" stroke-width="2.5"/>',
    }
    a = {"up": "M-30,-52 L-48,-80 M30,-52 L48,-80", "think": "M-30,-52 L-44,-30 M30,-52 L22,-70"}.get(
        arms, "M-30,-52 L-44,-30 M30,-52 L44,-30")
    top = ""
    if antenna:
        dots = "".join(f'<circle cx="{-52 + k*11.5}" cy="-118" r="3" fill="#0277bd"/>' for k in range(10))
        top = (f'<rect x="-62" y="-125" width="124" height="14" rx="7" fill="#b2ebf2" stroke="{INK}" stroke-width="3"/>{dots}'
               f'<circle cx="{-52 + 6*11.5}" cy="-118" r="6" fill="#ffeb3b" stroke="{INK}" stroke-width="1.5"/>')
    else:
        top = f'<circle cx="0" cy="-122" r="7" fill="#ffeb3b" stroke="{INK}" stroke-width="2.5"/>'
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="2" rx="40" ry="6" fill="#000" opacity=".15"/>
<rect x="-21" y="-14" width="13" height="14" rx="3" fill="#455a64" stroke="{INK}" stroke-width="3"/>
<rect x="8" y="-14" width="13" height="14" rx="3" fill="#455a64" stroke="{INK}" stroke-width="3"/>
<path d="{a}" stroke="{INK}" stroke-width="11" stroke-linecap="round" fill="none"/>
<path d="{a}" stroke="{color}" stroke-width="6" stroke-linecap="round" fill="none"/>
<rect x="-32" y="-64" width="64" height="52" rx="12" fill="{color}" stroke="{INK}" stroke-width="3"/>
<rect x="-17" y="-54" width="34" height="20" rx="4" fill="#01579b" stroke="{INK}" stroke-width="2"/>
<text x="0" y="-39.5" font-size="10" fill="#fff" text-anchor="middle" font-family="Bangers">{label}</text>
<rect x="-6" y="-116" width="12" height="12" fill="#90a4ae" stroke="{INK}" stroke-width="2.5"/>
<rect x="-31" y="-106" width="62" height="44" rx="15" fill="{light}" stroke="{INK}" stroke-width="3"/>
<ellipse cx="-11" cy="-87" rx="6" ry="8" fill="{INK}"/><ellipse cx="11" cy="-87" rx="6" ry="8" fill="{INK}"/>
<circle cx="-9" cy="-90" r="2.2" fill="#fff"/><circle cx="13" cy="-90" r="2.2" fill="#fff"/>
<circle cx="-22" cy="-76" r="4" fill="#f48fb1" opacity=".7"/><circle cx="22" cy="-76" r="4" fill="#f48fb1" opacity=".7"/>
{mouths[mood]}{top}</g>'''


def scientist(x, y, s=1.0, point=False, mood="smile", flip=False, scarf="#7e57c2", headwear="hijab",
              skin="#f1c27d", hair="#3e2723"):
    """Mentor / narrator who explains. headwear: 'hijab' or 'hair'. moods: smile open serious.
    point=True holds a pointer stick toward the upper right (flip=True mirrors)."""
    mouth = {"smile": f'<path d="M-6,-82 Q0,-77 6,-82" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>',
             "open": f'<path d="M-6,-83 Q0,-74 6,-83 Z" fill="#c62828" stroke="{INK}" stroke-width="2"/>',
             "serious": f'<path d="M-5,-81 L5,-81" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'}[mood]
    arm = (f'<path d="M18,-60 L40,-82" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
           f'<path d="M18,-60 L40,-82" stroke="#fafafa" stroke-width="6" stroke-linecap="round"/>'
           f'<path d="M40,-82 L66,-108" stroke="#6d4c41" stroke-width="3.5" stroke-linecap="round"/>'
           f'<circle cx="40" cy="-82" r="5" fill="{skin}" stroke="{INK}" stroke-width="2"/>') if point else \
          (f'<path d="M20,-60 L28,-30" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
           f'<path d="M20,-60 L28,-30" stroke="#fafafa" stroke-width="6" stroke-linecap="round"/>')
    if headwear == "hijab":
        head = (f'<path d="M-25,-92 Q-30,-66 -15,-62 L15,-62 Q30,-66 25,-92 Z" fill="{scarf}" stroke="{INK}" stroke-width="3"/>'
                f'<circle cx="0" cy="-94" r="25" fill="{scarf}" stroke="{INK}" stroke-width="3"/>')
    else:
        head = f'<path d="M-19,-86 Q-22,-116 0,-114 Q22,-116 19,-86 Q12,-104 0,-102 Q-12,-104 -19,-86 Z" fill="{hair}" stroke="{INK}" stroke-width="2.5"/>'
    fl = ' scale(-1,1)' if flip else ''
    body = f'''<ellipse cx="0" cy="2" rx="34" ry="6" fill="#000" opacity=".15"/>
<ellipse cx="-11" cy="-2" rx="10" ry="5" fill="#3e2723" stroke="{INK}" stroke-width="2"/>
<ellipse cx="11" cy="-2" rx="10" ry="5" fill="#3e2723" stroke="{INK}" stroke-width="2"/>
<path d="M-20,-60 L-28,-30" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>
<path d="M-20,-60 L-28,-30" stroke="#fafafa" stroke-width="6" stroke-linecap="round"/>
<path d="M-27,-4 L-22,-66 Q0,-74 22,-66 L27,-4 Z" fill="#fafafa" stroke="{INK}" stroke-width="3"/>
<path d="M-9,-68 L0,-34 L9,-68 Z" fill="{scarf}" stroke="{INK}" stroke-width="2"/>
<path d="M0,-34 L0,-6" stroke="{INK}" stroke-width="2"/>
<rect x="9" y="-46" width="9" height="11" fill="#90caf9" stroke="{INK}" stroke-width="1.5"/>{arm}'''
    if headwear == "hijab":
        headgrp = head + f'<ellipse cx="0" cy="-89" rx="15" ry="17" fill="{skin}" stroke="{INK}" stroke-width="2.5"/>'
    else:
        headgrp = f'<ellipse cx="0" cy="-89" rx="15" ry="17" fill="{skin}" stroke="{INK}" stroke-width="2.5"/>' + \
                  f'<path d="M-17,-90 Q-20,-114 0,-112 Q20,-114 17,-90 Q12,-104 0,-103 Q-12,-104 -17,-90 Z" fill="{hair}" stroke="{INK}" stroke-width="2.5"/>'
    eyes = (f'<circle cx="-6.5" cy="-89" r="5.5" fill="#fff" fill-opacity=".5" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="6.5" cy="-89" r="5.5" fill="#fff" fill-opacity=".5" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M-1,-89 L1,-89" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="-6.5" cy="-89" r="1.8" fill="{INK}"/><circle cx="6.5" cy="-89" r="1.8" fill="{INK}"/>')
    return f'<g transform="translate({x},{y}) scale({s}){fl}">{body}{headgrp}{eyes}{mouth}</g>'


def explorer(x, y, s=1.0, color="#43a047", label="EP", tool="flash", beam=110, mood="happy"):
    """Adaptive / clever method. tool: 'flash' (flashlight beam to the right, length=beam) or 'lantern' (with '?').
    moods: happy sad shout."""
    mouth = {"happy": f'<path d="M-6,-77 Q0,-71 6,-77" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>',
             "sad": f'<path d="M-6,-73 Q0,-79 6,-73" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>',
             "shout": f'<path d="M-7,-78 Q0,-66 7,-78 Z" fill="#c62828" stroke="{INK}" stroke-width="2"/>'}[mood]
    if tool == "flash":
        t = ((f'<polygon points="44,-56 {44+beam},-{56+beam*0.38} {44+beam},-{56-beam*0.38}" fill="#fff59d" opacity=".75"/>' if beam else "")
             + f'<rect x="26" y="-62" width="20" height="12" rx="3" fill="#616161" stroke="{INK}" stroke-width="2.5"/>')
    else:
        t = (f'<circle cx="40" cy="-50" r="{beam*0.35}" fill="#fff59d" opacity=".5"/>'
             f'<path d="M40,-72 L40,-64" stroke="{INK}" stroke-width="2.5"/>'
             f'<rect x="31" y="-64" width="18" height="22" rx="5" fill="#ffe082" stroke="{INK}" stroke-width="2.5"/>'
             f'<text x="40" y="-47" font-size="15" text-anchor="middle" font-family="Bangers" fill="{INK}">?</text>')
    fs = 17 if len(label) <= 3 else 12
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="2" rx="30" ry="6" fill="#000" opacity=".15"/>{t}
<rect x="-16" y="-16" width="11" height="16" rx="3" fill="#33691e" stroke="{INK}" stroke-width="2.5"/>
<rect x="5" y="-16" width="11" height="16" rx="3" fill="#33691e" stroke="{INK}" stroke-width="2.5"/>
<path d="M-20,-50 L-32,-30 M20,-52 L30,-56" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
<path d="M-20,-50 L-32,-30 M20,-52 L30,-56" stroke="{color}" stroke-width="5.5" stroke-linecap="round"/>
<ellipse cx="0" cy="-40" rx="24" ry="28" fill="{color}" stroke="{INK}" stroke-width="3"/>
<text x="0" y="-31" font-size="{fs}" text-anchor="middle" font-family="Bangers" fill="#fff" stroke="{INK}" stroke-width=".8">{label}</text>
<circle cx="0" cy="-82" r="18" fill="#ffcc80" stroke="{INK}" stroke-width="3"/>
<circle cx="-6" cy="-84" r="2.6" fill="{INK}"/><circle cx="6" cy="-84" r="2.6" fill="{INK}"/>{mouth}
<ellipse cx="0" cy="-97" rx="30" ry="6.5" fill="#8d6e63" stroke="{INK}" stroke-width="2.5"/>
<path d="M-17,-98 Q0,-122 17,-98 Z" fill="#a1887f" stroke="{INK}" stroke-width="2.5"/>
<path d="M-16,-101 L16,-101" stroke="{color}" stroke-width="3"/></g>'''


def sergeant(x, y, s=1.0, mood="stern", color="#fb8c00", label="GRID"):
    """Baseline / classic / fixed method: disciplined soldier with a ruler. moods: stern smug."""
    mouth = {"stern": "", "smug": f'<path d="M-2,-71 Q6,-67 10,-72" fill="none" stroke="{INK}" stroke-width="2.2"/>'}[mood]
    ticks = "".join(f'<path d="M{18+k*8},-56 L{18+k*8},-{50 if k%2 else 47}" stroke="{INK}" stroke-width="1.5"/>' for k in range(9))
    fs = 12 if len(label) <= 5 else 9
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="2" rx="34" ry="6" fill="#000" opacity=".15"/>
<rect x="-20" y="-14" width="13" height="14" rx="2" fill="#3e2723" stroke="{INK}" stroke-width="2.5"/>
<rect x="7" y="-14" width="13" height="14" rx="2" fill="#3e2723" stroke="{INK}" stroke-width="2.5"/>
<rect x="-27" y="-68" width="54" height="56" rx="7" fill="{color}" stroke="{INK}" stroke-width="3"/>
<rect x="-19" y="-40" width="38" height="13" rx="2" fill="#fff3e0" stroke="{INK}" stroke-width="2"/>
<text x="0" y="-29.5" font-size="{fs}" text-anchor="middle" font-family="Bangers" fill="{INK}">{label}</text>
<path d="M-27,-58 L-38,-34" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
<path d="M-27,-58 L-38,-34" stroke="{color}" stroke-width="5.5" stroke-linecap="round"/>
<rect x="10" y="-60" width="80" height="10" fill="#fff176" stroke="{INK}" stroke-width="2.5"/>{ticks}
<circle cx="22" cy="-55" r="6" fill="#ffcc80" stroke="{INK}" stroke-width="2"/>
<rect x="-20" y="-104" width="40" height="37" rx="10" fill="#ffcc80" stroke="{INK}" stroke-width="3"/>
<path d="M-12,-88 L-4,-88 M4,-88 L12,-88" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M-12,-77 Q-6,-82 0,-78 Q6,-82 12,-77 Q6,-74 0,-76 Q-6,-74 -12,-77 Z" fill="#4e342e" stroke="{INK}" stroke-width="1.5"/>{mouth}
<rect x="-23" y="-114" width="46" height="13" rx="3" fill="#1565c0" stroke="{INK}" stroke-width="2.5"/>
<path d="M-23,-101 L30,-101 L24,-97 L-23,-97 Z" fill="#0d47a1" stroke="{INK}" stroke-width="2"/>
<circle cx="0" cy="-108" r="3.5" fill="#ffd54f" stroke="{INK}" stroke-width="1.2"/></g>'''


def monster(x, y, s=1.0, mood="angry", color="#546e7a", label=""):
    """Villain = the problem (outage, error, attack, noise...). Drawn CENTERED at (x, y), about 140 units wide.
    moods: angry (with lightning) hurt. label: short word written on its belly."""
    circles = [(0, 0, 34), (-34, 8, 26), (34, 8, 26), (-18, -24, 26), (20, -22, 28), (-52, 22, 16), (52, 22, 16), (0, 22, 28)]
    outline = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{INK}" stroke="{INK}" stroke-width="7"/>' for a, b, r in circles)
    fill = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{color}"/>' for a, b, r in circles)
    if mood == "angry":
        face = (f'<ellipse cx="-14" cy="-2" rx="9" ry="7" fill="#fff"/><ellipse cx="14" cy="-2" rx="9" ry="7" fill="#fff"/>'
                f'<circle cx="-12" cy="0" r="3.5" fill="#d50000"/><circle cx="12" cy="0" r="3.5" fill="#d50000"/>'
                f'<path d="M-26,-14 L-6,-6 M26,-14 L6,-6" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'
                f'<path d="M-16,20 L-10,13 L-4,20 L2,13 L8,20 L14,13 L18,20 Z" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        bolt = f'<path d="M-6,46 L8,46 L0,62 L12,62 L-10,92 L-2,70 L-12,70 Z" fill="#ffeb3b" stroke="{INK}" stroke-width="2.5"/>'
    else:
        face = (f'<path d="M-20,-2 L-8,2 M-20,4 L-8,0 M20,-2 L8,2 M20,4 L8,0" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                f'<ellipse cx="0" cy="17" rx="7" ry="5" fill="{INK}"/>'
                f'<path d="M30,-30 q4,-8 8,0 q4,8 8,0" fill="none" stroke="#90a4ae" stroke-width="2"/>')
        bolt = ""
    lab = f'<text x="0" y="40" font-size="13" text-anchor="middle" font-family="Bangers" fill="#fff">{label}</text>' if label else ""
    return f'<g transform="translate({x},{y}) scale({s})">{bolt}{outline}{fill}{face}{lab}</g>'


def gatekeeper(x, y, s=1.0, label="D", sub="99"):
    """Decision rule / switch / threshold: a stone gate with eyes and a plaque. Feet at (x, y), ~190 units tall."""
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="3" rx="80" ry="8" fill="#000" opacity=".15"/>
<rect x="-70" y="-120" width="28" height="120" fill="#9575cd" stroke="{INK}" stroke-width="3"/>
<rect x="42" y="-120" width="28" height="120" fill="#9575cd" stroke="{INK}" stroke-width="3"/>
<path d="M-74,-118 Q0,-178 74,-118 L74,-108 Q0,-160 -74,-108 Z" fill="#7e57c2" stroke="{INK}" stroke-width="3"/>
<path d="M-62,-100 L-50,-100 M-62,-70 L-50,-70 M-62,-40 L-50,-40 M50,-100 L62,-100 M50,-70 L62,-70 M50,-40 L62,-40" stroke="{INK}" stroke-width="2"/>
<rect x="-38" y="-176" width="76" height="40" rx="8" fill="#ffd54f" stroke="{INK}" stroke-width="3"/>
<text x="0" y="-147" font-size="28" text-anchor="middle" font-family="Bangers" fill="{INK}">{label}<tspan font-size="17" dy="5">{sub}</tspan></text>
<ellipse cx="-14" cy="-188" rx="9" ry="10" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<ellipse cx="14" cy="-188" rx="9" ry="10" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<circle cx="-12" cy="-186" r="4" fill="{INK}"/><circle cx="16" cy="-186" r="4" fill="{INK}"/></g>'''


# ---------------------------------------------------------------- props & mini charts (all in panel SVG units)
def dot_row(x, y, w, n=50, marked=(), color="#e53935", nums=(), h=16, glow=None):
    """A rail of n dots (ports, antennas, sensors, nodes, time slots...). marked = 1-based indices to highlight."""
    r = min(w / (n * 2.4), h * 0.36)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#b2ebf2" stroke="{INK}" stroke-width="2.5"/>']
    for k in range(1, n + 1):
        cx, cy = dot_x(x, w, k, n, h), y + h / 2
        if k in marked:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.6}" fill="{color}" stroke="{INK}" stroke-width="1.6"/>')
        elif glow == k:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.7}" fill="#ffeb3b" stroke="{INK}" stroke-width="1.6"/>')
        else:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.8}" fill="#0277bd"/>')
        if k in nums:
            out.append(f'<text x="{cx}" y="{y+h+13}" font-size="11" text-anchor="middle" font-family="Comic Neue" font-weight="700">{k}</text>')
    return "".join(out)


def dot_x(x, w, k, n=50, h=16):
    return x + h / 2 + (k - 1) * (w - h) / (n - 1)


def burst(x, y, r, color="#ffeb3b", pts=14):
    p = []
    for i in range(pts * 2):
        a = np.pi * i / pts
        rr = r if i % 2 == 0 else r * 0.68
        p.append(f"{x + rr*np.cos(a):.1f},{y + rr*np.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{color}" stroke="{INK}" stroke-width="3"/>'


def board(x, y, w, h):
    """Dark blackboard rectangle for charts/equations."""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#263238" stroke="{INK}" stroke-width="4"/>'


def text(x, y, t, size=16, color=INK, anchor="start", font="Comic Neue", weight=700):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-family="{font}" font-weight="{weight}">{t}</text>'


def bars(x, y, w, h, values, labels=None, colors=None, light=False, cut=None):
    """Simple bar chart. cut = index after which a dashed line is drawn (e.g. a threshold)."""
    vmax = max(values) or 1
    m = len(values)
    bw = w / m
    axis = "#fff" if light else INK
    out = [f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{axis}" stroke-width="2.5"/>']
    for k, v in enumerate(values):
        bh = max(v / vmax * h, 1.5)
        col = (colors[k] if colors else "#7e57c2")
        out.append(f'<rect x="{x+k*bw+bw*.12}" y="{y+h-bh}" width="{bw*.76}" height="{bh}" fill="{col}" stroke="{INK}" stroke-width="2"/>')
        if labels:
            out.append(text(x + k * bw + bw / 2, y + h + 14, labels[k], 11, axis, "middle"))
    if cut is not None:
        out.append(f'<path d="M{x+cut*bw},{y-4} L{x+cut*bw},{y+h}" stroke="#d81b60" stroke-width="2.5" stroke-dasharray="6 4"/>')
    return "".join(out)


def curve(x, y, w, h, ys, color="#d81b60", light=False, zero_line=True):
    """Line plot of ys (any range) scaled into the box."""
    ys = np.asarray(ys, float)
    lo, hi = ys.min(), ys.max()
    span = (hi - lo) or 1
    pts = " ".join(f"{x + i/(len(ys)-1)*w:.1f},{y + h - (v-lo)/span*h:.1f}" for i, v in enumerate(ys))
    axis = "#fff" if light else INK
    out = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{axis}" stroke-width="2"/>'
    if zero_line and lo < 0 < hi:
        zy = y + h - (0 - lo) / span * h
        out += f'<line x1="{x}" y1="{zy}" x2="{x+w}" y2="{zy}" stroke="#90a4ae" stroke-width="1.5" stroke-dasharray="4 4"/>'
    return out + f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3.5"/>'


def heat(x, y, cw, ch, matrix, row_labels, col_labels, xlab="", ylab="", empty="—"):
    """Heat map; None cells are gray. Values colored yellow→magenta by size."""
    vals = [v for r in matrix for v in r if v is not None]
    vmax = max(vals) if vals else 1
    out = []
    for r, row in enumerate(matrix):
        out.append(text(x - 6, y + r * ch + ch * 0.65, row_labels[r], 13, anchor="end"))
        for c, v in enumerate(row):
            if v is None:
                fill, t, tc = "#e0e0e0", empty, "#757575"
            else:
                f = max(v, 0) / vmax
                col = np.array([255, 241, 118]) * (1 - f) + np.array([216, 27, 96]) * f
                fill, t, tc = "#%02x%02x%02x" % tuple(col.astype(int)), f"{v:g}", INK if f < .6 else "#fff"
            out.append(f'<rect x="{x+c*cw}" y="{y+r*ch}" width="{cw}" height="{ch}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
            out.append(text(x + c * cw + cw / 2, y + r * ch + ch * 0.64, t, 13, tc, "middle"))
    for c, lab in enumerate(col_labels):
        out.append(text(x + c * cw + cw / 2, y + len(matrix) * ch + 15, lab, 13, anchor="middle"))
    if xlab:
        out.append(text(x + len(col_labels) * cw / 2, y + len(matrix) * ch + 32, xlab, 13, anchor="middle", font="Bangers", weight=400))
    if ylab:
        cy = y + len(matrix) * ch / 2
        out.append(f'<text x="{x-34}" y="{cy}" font-size="13" text-anchor="middle" font-family="Bangers" transform="rotate(-90 {x-34} {cy})">{ylab}</text>')
    return "".join(out)


def puzzle(x, y, n, have, size=46, cols=3):
    """n puzzle pieces, the first `have` are filled (good metaphor for dimensions / unknowns / degrees of freedom)."""
    out = ""
    for k in range(n):
        cx, cy = x + (k % cols) * (size + 6), y + (k // cols) * (size + 6)
        f = "#7e57c2" if k < have else "#eceff1"
        dash = 'stroke-dasharray="6 4"' if k >= have else ""
        out += f'<rect x="{cx}" y="{cy}" width="{size}" height="{size}" rx="6" fill="{f}" stroke="{INK}" stroke-width="2.5" {dash}/>'
    return out


def diamond(x, y, t, w=75, h=60):
    """Decision diamond centred at (x, y)."""
    return (f'<polygon points="{x},{y-h} {x+w},{y} {x},{y+h} {x-w},{y}" fill="#ffd54f" stroke="{INK}" stroke-width="4"/>'
            + text(x, y + 9, t, 24, anchor="middle", font="Bangers", weight=400))


def chips(x, y, items, w=140, h=60, gap=20):
    """Row of coloured label chips: items = [(text, color), ...]."""
    out = ""
    for k, (t, c) in enumerate(items):
        cx = x + k * (w + gap)
        out += (f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}" stroke="{INK}" stroke-width="3"/>'
                + text(cx + w / 2, y + h / 2 + 7, t, 18, anchor="middle", font="Bangers", weight=400))
    return out


# ---------------------------------------------------------------- overlays (positions in mm, relative to the panel)
def B(x, y, w, html, tail="bl", cls=""):
    """Speech bubble. tail: bl br bc tl tr l r. cls: '' | 'mentor' (lilac) | 'shout' (yellow, Bangers) | 'small'."""
    return f'<div class="bubble t-{tail} {cls}" style="left:{x}mm;top:{y}mm;width:{w}mm">{html}</div>'


def C(x, y, w, html, cls=""):
    """Caption box. cls: '' (yellow) | 'white' | 'math' (formula box) | 'small'."""
    return f'<div class="cap {cls}" style="left:{x}mm;top:{y}mm;width:{w}mm">{html}</div>'


def SFX(x, y, t, size=16, color="#ffeb3b", rot=-8):
    return f'<div class="sfx" style="left:{x}mm;top:{y}mm;font-size:{size}pt;color:{color};transform:rotate({rot}deg)">{t}</div>'


def RAW(x, y, w, html, cls=""):
    """Free HTML block (tables, lists) positioned inside a panel."""
    return f'<div class="raw {cls}" style="left:{x}mm;top:{y}mm;width:{w}mm">{html}</div>'


def table(header, rows, row_colors=None, title="", foot=""):
    """Comic scoreboard table (HTML). Wrap with RAW(...)."""
    h = "".join(f"<th>{c}</th>" for c in header)
    body = ""
    for i, r in enumerate(rows):
        bg = f' style="background:{row_colors[i]}"' if row_colors else ""
        body += f"<tr{bg}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    t = f'<div class="sbtitle">{title}</div>' if title else ""
    f = f'<div class="foot">{foot}</div>' if foot else ""
    return f'{t}<table class="score"><tr>{h}</tr>{body}</table>{f}'


def panel(x, y, w, h, svg="", items=(), bg="dots-blue"):
    """bg: dots-blue dots-yellow dots-pink dots-gray plain none."""
    return (f'<div class="panel {bg}" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm">'
            f'<svg viewBox="0 0 {w*U} {h*U}" width="100%" height="100%">{svg}</svg>{"".join(items)}</div>')


def page(num, title, panels):
    head = f'<div class="head"><span class="ch">{title}</span><span class="pn">{num}</span></div>'
    return f'<section class="page">{head}{"".join(panels)}</section>'


def cover(title, subtitle, svg, tagline, credit, masthead="RESEARCH COMICS", issue="Issue #1", extra=()):
    """Full cover page. svg is drawn in a 196 x 283 mm frame (784 x 1132 units). Leave the top ~60 mm
    (title) and bottom ~25 mm (credit) free of important art."""
    items = [f'<div class="masthead">{masthead} <span>· {issue} ·</span></div>',
             f'<div class="bigtitle">{title}</div>', f'<div class="subtitle">{subtitle}</div>',
             f'<div class="tag" style="left:12mm;top:68mm">{tagline}</div>',
             f'<div class="basedon">{credit}</div>', *extra]
    bgsvg = ('<defs><radialGradient id="sun" cx="50%" cy="58%" r="70%"><stop offset="0" stop-color="#fff9c4"/>'
             '<stop offset=".45" stop-color="#4fc3f7"/><stop offset="1" stop-color="#0d47a1"/></radialGradient></defs>'
             f'<rect width="{196*U}" height="{283*U}" fill="url(#sun)"/>')
    return f'<section class="page cover">{panel(7, 7, 196, 283, bgsvg + svg, items, bg="none")}</section>'


# ---------------------------------------------------------------- render
def css(fonts):
    def src(name):
        p = fonts.get(name)
        return f"src: url(file://{p});" if p else "src: local('DejaVu Sans');"
    return f"""
@font-face {{ font-family: Bangers; {src('bangers-latin-400-normal.woff2')} }}
@font-face {{ font-family: 'Comic Neue'; font-weight: 400; {src('comic-neue-latin-400-normal.woff2')} }}
@font-face {{ font-family: 'Comic Neue'; font-weight: 700; {src('comic-neue-latin-700-normal.woff2')} }}
@page {{ size: 210mm 297mm; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Comic Neue', 'DejaVu Sans', sans-serif; color: {INK}; }}
.page {{ position: relative; width: 210mm; height: 297mm; overflow: hidden; page-break-after: always; background: #fdf6e3; }}
.page.cover {{ background: {INK}; }}
.head {{ position: absolute; left: 7mm; right: 7mm; top: 5mm; height: 8mm; display: flex; justify-content: space-between;
        align-items: center; border-bottom: 1mm solid {INK}; }}
.head .ch {{ font-family: Bangers; font-size: 17pt; letter-spacing: .6pt; color: #d81b60; -webkit-text-stroke: .3pt {INK}; }}
.head .pn {{ font-family: Bangers; font-size: 14pt; background: {INK}; color: #ffeb3b; padding: 0 2.5mm; border-radius: 1mm; }}
.panel {{ position: absolute; border: .9mm solid {INK}; overflow: hidden; background: #fff; box-shadow: 1.2mm 1.2mm 0 {INK}; }}
.panel svg {{ position: absolute; inset: 0; }}
.dots-blue {{ background: radial-gradient(#b3e5fc 22%, transparent 24%) 0 0/3.2mm 3.2mm, #e1f5fe; }}
.dots-yellow {{ background: radial-gradient(#ffe082 22%, transparent 24%) 0 0/3.2mm 3.2mm, #fff8e1; }}
.dots-pink {{ background: radial-gradient(#f8bbd0 22%, transparent 24%) 0 0/3.2mm 3.2mm, #fce4ec; }}
.dots-gray {{ background: radial-gradient(#90a4ae 22%, transparent 24%) 0 0/3.2mm 3.2mm, #607d8b; }}
.plain, .none {{ background: #fff; }}
.bubble {{ position: absolute; background: #fff; border: .6mm solid {INK}; border-radius: 4mm; padding: 1.6mm 2.4mm;
          font-size: 9.8pt; line-height: 1.22; font-weight: 400; z-index: 3; }}
.bubble b, .cap b {{ font-weight: 700; }}
.small {{ font-size: 8.6pt !important; }}
.bubble.mentor {{ background: #f3e5f5; }}
.bubble.shout {{ background: #fff59d; font-family: Bangers; font-size: 13pt; letter-spacing: .4pt; border-width: .8mm; }}
.bubble::before, .bubble::after {{ content: ""; position: absolute; width: 0; height: 0; border: solid transparent; }}
.t-bl::before {{ left: 5mm; bottom: -4.6mm; border-width: 4.6mm 3mm 0 0; border-top-color: {INK}; }}
.t-bl::after  {{ left: 5.6mm; bottom: -3.4mm; border-width: 3.5mm 2.2mm 0 0; }}
.t-br::before {{ right: 5mm; bottom: -4.6mm; border-width: 4.6mm 0 0 3mm; border-top-color: {INK}; }}
.t-br::after  {{ right: 5.6mm; bottom: -3.4mm; border-width: 3.5mm 0 0 2.2mm; }}
.t-bc::before {{ left: 50%; bottom: -4.6mm; border-width: 4.6mm 2.4mm 0 2.4mm; border-top-color: {INK}; }}
.t-bc::after  {{ left: calc(50% + .6mm); bottom: -3.4mm; border-width: 3.5mm 1.8mm 0 1.8mm; }}
.t-tl::before {{ left: 5mm; top: -4.6mm; border-width: 0 3mm 4.6mm 0; border-bottom-color: {INK}; }}
.t-tl::after  {{ left: 5.6mm; top: -3.4mm; border-width: 0 2.2mm 3.5mm 0; }}
.t-tr::before {{ right: 5mm; top: -4.6mm; border-width: 0 0 4.6mm 3mm; border-bottom-color: {INK}; }}
.t-tr::after  {{ right: 5.6mm; top: -3.4mm; border-width: 0 0 3.5mm 2.2mm; }}
.t-l::before  {{ left: -4.6mm; top: 3mm; border-width: 3mm 4.6mm 0 0; border-right-color: {INK}; }}
.t-l::after   {{ left: -3.4mm; top: 3.6mm; border-width: 2.2mm 3.5mm 0 0; }}
.t-r::before  {{ right: -4.6mm; top: 3mm; border-width: 3mm 0 0 4.6mm; border-left-color: {INK}; }}
.t-r::after   {{ right: -3.4mm; top: 3.6mm; border-width: 2.2mm 0 0 3.5mm; }}
.t-bl::after, .t-br::after, .t-bc::after {{ border-top-color: #fff; }}
.t-tl::after, .t-tr::after {{ border-bottom-color: #fff; }}
.t-l::after {{ border-right-color: #fff; }} .t-r::after {{ border-left-color: #fff; }}
.mentor.t-bl::after, .mentor.t-br::after, .mentor.t-bc::after {{ border-top-color: #f3e5f5; }}
.mentor.t-tl::after, .mentor.t-tr::after {{ border-bottom-color: #f3e5f5; }}
.mentor.t-l::after {{ border-right-color: #f3e5f5; }} .mentor.t-r::after {{ border-left-color: #f3e5f5; }}
.shout.t-bl::after, .shout.t-br::after, .shout.t-bc::after {{ border-top-color: #fff59d; }}
.shout.t-tl::after, .shout.t-tr::after {{ border-bottom-color: #fff59d; }}
.shout.t-l::after {{ border-right-color: #fff59d; }} .shout.t-r::after {{ border-left-color: #fff59d; }}
.cap {{ position: absolute; background: #ffeb3b; border: .6mm solid {INK}; padding: 1.4mm 2.2mm; font-size: 9.4pt; line-height: 1.22; z-index: 3; }}
.cap.white {{ background: #fff; }}
.cap.math {{ background: #e8eaf6; font-size: 9.6pt; text-align: center; }}
.raw {{ position: absolute; z-index: 3; }}
.sfx {{ position: absolute; font-family: Bangers; -webkit-text-stroke: 1.1pt {INK}; letter-spacing: 1pt; z-index: 4; text-shadow: 1mm 1mm 0 {INK}; }}
.masthead {{ position: absolute; left: 0; right: 0; top: 0; height: 11mm; background: #d81b60; color: #fff; font-family: Bangers; font-size: 20pt;
            letter-spacing: 1.5pt; padding: 1mm 4mm; border-bottom: .9mm solid {INK}; z-index: 3; }}
.masthead span {{ font-size: 12pt; color: #ffeb3b; }}
.bigtitle {{ position: absolute; left: 0; right: 0; top: 14mm; text-align: center; font-family: Bangers; font-size: 64pt; color: #ffeb3b;
            -webkit-text-stroke: 2.6pt {INK}; text-shadow: 2mm 2mm 0 {INK}; letter-spacing: 3pt; transform: rotate(-3deg); z-index: 3; line-height: 1; }}
.subtitle {{ position: absolute; left: 22mm; right: 22mm; top: 45mm; text-align: center; font-size: 14pt; font-weight: 700; background: #fff;
            border: .7mm solid {INK}; padding: 1.5mm; transform: rotate(-1.5deg); z-index: 3; }}
.tag {{ position: absolute; font-family: Bangers; font-size: 17pt; background: #ffeb3b; border: .8mm solid {INK}; padding: 2mm 4mm;
       transform: rotate(-4deg); letter-spacing: .6pt; z-index: 3; box-shadow: 1.2mm 1.2mm 0 {INK}; max-width: 80mm; }}
.basedon {{ position: absolute; left: 0; right: 0; bottom: 0; background: #fff; border-top: .9mm solid {INK}; padding: 3mm 5mm;
           font-size: 9pt; line-height: 1.35; text-align: center; z-index: 3; }}
.banner {{ position: absolute; left: 0; right: 0; top: 4mm; text-align: center; font-family: Bangers; font-size: 30pt; color: #ffeb3b;
          -webkit-text-stroke: 1.4pt {INK}; text-shadow: 1.2mm 1.2mm 0 {INK}; letter-spacing: 2pt; z-index: 3; }}
.sbtitle {{ font-family: Bangers; font-size: 20pt; text-align: center; color: #d81b60; -webkit-text-stroke: .5pt {INK}; letter-spacing: 1pt; }}
table.score {{ width: 100%; border-collapse: collapse; font-size: 9.6pt; font-weight: 700; background: #fff; }}
table.score th {{ background: {INK}; color: #ffeb3b; font-family: Bangers; font-weight: 400; font-size: 11pt; letter-spacing: .5pt; padding: 1.2mm; }}
table.score td {{ border: .5mm solid {INK}; padding: 1.4mm 1.2mm; text-align: center; }}
table.score td:first-child {{ text-align: left; }}
.foot {{ font-size: 8pt; margin-top: 1.5mm; background: #fff; border: .4mm solid {INK}; padding: 1mm 1.5mm; }}
.box {{ background: #fff; border: .7mm solid {INK}; padding: 2mm 3.5mm; box-shadow: 1mm 1mm 0 {INK}; }}
.box .lt {{ font-family: Bangers; font-size: 19pt; color: #d81b60; letter-spacing: 1pt; -webkit-text-stroke: .4pt {INK}; text-align: center; }}
.box.lesson {{ font-size: 13pt; font-weight: 700; line-height: 1.5; text-align: center; }}
.box table {{ border-collapse: collapse; font-size: 10.2pt; font-weight: 700; }}
.box td {{ padding: 1.8mm 1mm; border-bottom: .3mm dashed #90a4ae; vertical-align: top; }}
.box td:first-child {{ font-family: Bangers; font-weight: 400; font-size: 13pt; color: #1565c0; white-space: nowrap; padding-right: 2.5mm; }}
.box p {{ margin: 2.2mm 0; font-size: 10pt; line-height: 1.25; }}
"""


def render(pages, pdf_path, preview=True):
    """pages: list of strings from cover()/page(). Writes the PDF and (optionally) 2-up PNG preview sheets."""
    from playwright.sync_api import sync_playwright
    fonts = ensure_fonts()
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css(fonts)}</style></head><body>{''.join(pages)}</body></html>"
    base = os.path.splitext(pdf_path)[0]
    with open(base + ".html", "w") as f:
        f.write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(f"file://{os.path.abspath(base + '.html')}")
        pg.wait_for_timeout(800)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        b.close()
    sheets = []
    if preview:
        from PIL import Image
        d = base + "_preview"
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(f"{d}/*.png"):
            os.remove(f)
        subprocess.run(["pdftoppm", "-r", "80", "-png", pdf_path, f"{d}/pg"], check=True)
        ims = [Image.open(p) for p in sorted(glob.glob(f"{d}/pg-*.png"))]
        w, h = ims[0].size
        for j in range(0, len(ims), 2):
            c = Image.new("RGB", (w * 2, h), "white")
            c.paste(ims[j], (0, 0))
            if j + 1 < len(ims):
                c.paste(ims[j + 1], (w, 0))
            out = f"{d}/sheet{j//2 + 1}.png"
            c.save(out)
            sheets.append(out)
    print("PDF:", pdf_path, "| preview sheets:", sheets)
    return sheets
