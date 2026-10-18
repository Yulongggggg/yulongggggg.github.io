"""Hand-placed chibi Shiba Inu pixel sprites for the website companion.

IDLE.png / RUN.png: 8 frames of 80x64 px (640x64), shown at 3x; the dog faces left (the page mirrors it).
IDLE: sitting, glancing left, then at the viewer, tail wagging, one blink.
RUN: side-view gallop with legs in four phases, body bob, tail wag and tongue out.
TOY.png: 31x31 px tennis ball scaled 6x. Original artwork; no third-party images.
Usage: python shiba.py OUTDIR
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

PAL = {
    'k': (112, 64, 36), 'O': (238, 152, 68), 'o': (214, 124, 50), 'C': (254, 245, 231), 'c': (238, 220, 198),
    'e': (50, 36, 32), 'w': (255, 255, 255), 'p': (249, 166, 160), 'i': (247, 184, 172), 'r': (214, 66, 74),
    'y': (250, 206, 84), 't': (238, 112, 122),
}

def mirror(rows):
    return [r + r[::-1] for r in rows]

# Featureless head (26 x 17); faces are painted on per pose.
HEAD = mirror([
    "....kk.......",
    "...kOOk......",
    "..kOiiOk.....",
    "..kOiiiOk....",
    ".kOOiiiOOkkkk",
    ".kOOiiOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOCCCCCCCCCCC",
    "kCCCCCCCCCCCC",
    "kCCCCCCCCCCCC",
    "kcCCCCCCCCCCC",
    ".kcCCCCCCCCCC",
    "..kkcCCCCCCCC",
])

def face(look, blink=False, tongue=False):
    """look: 0 = at the viewer, positive = turned left by that many pixels."""
    g = [list(r) for r in HEAD]
    s = look
    for ec in (7 - s, 17 - s):                       # eyes (2x2) with highlight, eyebrow dot above
        g[7][ec] = 'C'
        if blink:
            g[10][ec] = g[10][ec + 1] = 'e'
        else:
            g[9][ec], g[9][ec + 1], g[10][ec], g[10][ec + 1] = 'w', 'e', 'e', 'e'
    n = 11 - s                                         # nose: 4 wide over a 2-wide tip, then the mouth
    for c in range(n, n + 4): g[11][c] = 'e'
    g[12][n + 1] = g[12][n + 2] = 'e'
    g[13][n] = g[13][n + 3] = 'k'
    if tongue: g[14][n + 1] = g[14][n + 2] = 't'
    for c in (5 - s, 6 - s, 19 - s, 20 - s):           # blush
        if 1 <= c <= 24: g[12][c] = 'p'
    return [''.join(r) for r in g]

SIT_BODY = mirror([
    "...krrrrrrrrr",
    "...kOOOOCCCCy",
    "..kOOOOOOCCCC",
    "..kOOOOOOOCCC",
    ".kOOOOOOOOOCC",
    ".kOOOOOkOOOkC",
    "kOOOOOOkOOOko",
    "kOOOOOOkOOOko",
    "kOOOOOkCCCCko",
    "kCCCCCkCcCCko",
    ".kkkkk.kkkkkk",
])

class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h; self.g = [['.'] * w for _ in range(h)]
    def stamp(self, rows, r0, c0):
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                if v != '.' and 0 <= r0 + r < self.h and 0 <= c0 + c < self.w: self.g[r0 + r][c0 + c] = v
    def shape(self, mask, fill, outline='k'):
        """Paint a filled mask with a 1-px outline drawn over whatever is behind it."""
        m = np.asarray(mask, bool); pad = np.pad(m, 1); edge = np.zeros_like(m)
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): edge |= pad[1 + dy:self.h + 1 + dy, 1 + dx:self.w + 1 + dx]
        for y, x in zip(*np.nonzero(edge & ~m)): self.g[y][x] = outline
        for y, x in zip(*np.nonzero(m)): self.g[y][x] = fill if isinstance(fill, str) else fill(y, x)
    def ellipse(self, cx, cy, rx, ry):
        ys, xs = np.mgrid[0:self.h, 0:self.w]; return ((xs + .5 - cx) / rx) ** 2 + ((ys + .5 - cy) / ry) ** 2 <= 1
    def line(self, p, q, width):
        im = Image.new('L', (self.w, self.h), 0); ImageDraw.Draw(im).line([p, q], fill=1, width=width); return np.array(im, bool)
    def rows(self): return [''.join(r) for r in self.g]

def sit(look=2, blink=False, wag=0, dy=0):
    G = Grid(30, 30)
    top = 1
    # curled tail behind the right shoulder
    tx, ty = 26.5 + wag, top + 19.5
    G.shape(G.ellipse(tx, ty, 2.7, 2.7), lambda y, x: 'C' if (x + .5 - tx + 1) ** 2 + (y + .5 - ty + 1) ** 2 < 1.1 else 'O')
    G.stamp(SIT_BODY, top + 17, 0)
    G.stamp(face(look, blink), top + dy, 0)
    return G.rows()

def run(i):
    G = Grid(48, 30)
    ph = 2 * math.pi * i / 8
    bob = [0, -1, -2, -1, 0, -1, -2, -1][i]
    by = 19 + bob                                     # body centre row
    def leg(hip_x, angle, near):
        a = math.radians(angle); hx, hy = hip_x, by + 2.5
        fx, fy = hx - 6 * math.sin(a), hy + 6 * math.cos(a)
        G.shape(G.line((hx, hy), (fx, fy), 3), 'O' if near else 'o')
        G.shape(G.ellipse(fx + .5 - .8 * math.sin(a), fy + .4, 1.9, 1.3), 'C' if near else 'c')
    swing = lambda off: 40 * math.sin(ph + off)
    leg(24, swing(math.pi + .8), False); leg(37, swing(.8), False)       # far legs, behind
    wag = [0, 1, 1, 0, 0, -1, -1, 0][i]
    tx, ty = 42.5, by - 5.5 + wag * .6
    G.shape(G.ellipse(tx, ty, 3.1, 3.1), lambda y, x: 'C' if (x + .5 - tx + 1.1) ** 2 + (y + .5 - ty + 1.1) ** 2 < 1.2 else 'O')
    G.shape(G.ellipse(31, by, 12.5, 5.4), lambda y, x: 'C' if y + .5 > by + 2.4 and abs(x + .5 - 30) < 9 else 'O')
    leg(22, swing(math.pi), True); leg(39, swing(0), True)
    hr = by - 18 + (1 if bob == 0 else 0)             # head raised and forward, glancing left
    G.stamp(face(3, tongue=True), hr, 1)
    for c in range(15, 21):
        if 0 <= hr + 17 < G.h and G.g[hr + 17][c] in 'OCo': G.g[hr + 17][c] = 'r'
    return G.rows()

def to_frame(rows, x_anchor, dy=0):
    img = np.zeros((64, 80, 4), np.uint8)
    used = [r for r in range(len(rows)) if rows[r].strip('.')]
    bottom = used[-1]; y0 = 47 - bottom + dy
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v != '.' and 0 <= y0 + r < 64 and 0 <= x_anchor + c < 80: img[y0 + r, x_anchor + c] = (*PAL[v], 255)
    return img

def idle_frames():
    spec = [(3, False, 0), (3, False, 1), (3, False, 0), (3, True, -1), (1, False, 0), (0, False, 1), (0, False, 0), (2, False, -1)]
    return [to_frame(sit(look, bl, w), 26) for look, bl, w in spec]

def run_frames():
    return [to_frame(run(i), 16) for i in range(8)]

def toy():
    n = 31; img = np.zeros((n, n, 4), np.uint8)
    ys, xs = np.mgrid[0:n, 0:n]; r = np.hypot(xs + .5 - n / 2, ys + .5 - n / 2)
    ball, ring = r <= 14, (r > 14) & (r <= 15)
    img[ball] = (206, 226, 72, 255); img[ring] = (92, 110, 30, 255)
    img[ball & ((xs + ys) > 36)] = (176, 198, 52, 255)
    for cx in (-3.5, n + 3.5):
        img[ball & (np.abs(np.hypot(xs + .5 - cx, ys + .5 - n / 2) - 13.2) < .7) & (r <= 13.4)] = (250, 250, 236, 255)
    img[7:9, 9:11] = (238, 248, 170, 255)
    return Image.fromarray(img, 'RGBA').resize((186, 186), Image.NEAREST)

if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.concatenate(idle_frames(), 1), 'RGBA').save(out / 'IDLE.png')
    Image.fromarray(np.concatenate(run_frames(), 1), 'RGBA').save(out / 'RUN.png')
    toy().save(out / 'TOY.png')
