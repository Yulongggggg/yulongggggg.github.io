"""Pixel Shiba Inu sprites for the website companion (replaces the pixel cat).

IDLE.png and RUN.png: 8 frames of 80x64 px side by side (640x64), dog facing left, feet on row 47.
TOY.png: 31x31 px tennis ball scaled 6x (186x186). Pure geometry; no third-party artwork.
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

W, H = 80, 64
PAL = dict(out=(64, 40, 26), orange=(226, 142, 62), shade=(190, 108, 44), cream=(251, 240, 222),
           creamd=(228, 210, 186), black=(34, 28, 28), pink=(238, 146, 152), red=(204, 52, 62),
           gold=(246, 198, 70), white=(255, 255, 255))

class Frame:
    def __init__(self):
        self.c = np.zeros((H, W), dtype=object)  # palette key or 0
    def ellipse(self, cx, cy, rx, ry, col, where=None):
        ys, xs = np.mgrid[0:H, 0:W]
        m = ((xs + .5 - cx) / rx) ** 2 + ((ys + .5 - cy) / ry) ** 2 <= 1
        if where is not None: m &= where
        self.c[m] = col
        return m
    def poly(self, pts, col):
        im = Image.new('L', (W, H), 0); ImageDraw.Draw(im).polygon(pts, fill=1)
        m = np.array(im, bool); self.c[m] = col; return m
    def line(self, p, q, width, col):
        im = Image.new('L', (W, H), 0); ImageDraw.Draw(im).line([p, q], fill=1, width=width)
        m = np.array(im, bool); self.c[m] = col; return m
    def px(self, x, y, col):
        self.c[int(y), int(x)] = col
    def filled(self):
        return self.c != 0
    def render(self):
        filled = self.filled()
        img = np.zeros((H, W, 4), np.uint8)
        # 1-px outline around the silhouette (8-neighbourhood).
        pad = np.pad(filled, 1)
        near = np.zeros_like(filled)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                near |= pad[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx]
        outline = near & ~filled
        for y in range(H):
            for x in range(W):
                k = self.c[y, x]
                if k: img[y, x] = (*PAL[k], 255)
                elif outline[y, x]: img[y, x] = (*PAL['out'], 255)
        return img

def head(f, cx, cy, blink=False, ears_back=0):
    # ears first so the head overlaps their base
    f.poly([(cx - 6, cy - 4), (cx - 5 - ears_back, cy - 11), (cx - 1, cy - 5)], 'orange')
    f.poly([(cx - 5, cy - 5), (cx - 4.5 - ears_back, cy - 9), (cx - 2.5, cy - 5)], 'pink')
    f.poly([(cx, cy - 5), (cx + 3 - ears_back, cy - 12), (cx + 6, cy - 4)], 'orange')
    f.poly([(cx + 1.5, cy - 5), (cx + 3 - ears_back, cy - 10), (cx + 4.5, cy - 5)], 'pink')
    f.ellipse(cx, cy, 7.5, 6.5, 'orange')
    f.ellipse(cx - 3.5, cy + 3, 5, 3.2, 'cream')               # cheek
    f.ellipse(cx - 7.5, cy + 2.5, 3.6, 2.6, 'cream')           # muzzle
    nx, ny = int(cx - 11), int(cy + 1)
    for dx in (0, 1):
        for dy in (0, 1): f.px(nx + dx, ny + dy, 'black')
    f.px(nx + 2, ny + 3, 'black'); f.px(nx + 3, ny + 3, 'black')  # mouth
    ex, ey = int(cx - 5), int(cy - 1)
    if blink:
        f.px(ex, ey + 1, 'black'); f.px(ex + 1, ey + 1, 'black')
    else:
        for dx in (0, 1):
            for dy in (0, 1): f.px(ex + dx, ey + dy, 'black')
        f.px(ex, ey, 'white')
    f.px(ex + 1, ey - 2, 'cream')                               # Shiba eyebrow dot

def tail_curl(f, cx, cy, r=4.6):
    ring = f.ellipse(cx, cy, r, r, 'orange')
    f.ellipse(cx + .4, cy - .3, r - 2.2, r - 2.2, 'cream')

def idle_frame(i):
    f = Frame()
    dy = [0, 0, 1, 1, 1, 1, 0, 0][i]
    tx = [0, 1, 1, 0, -1, -1, 0, 1][i]
    tail_curl(f, 49 + tx, 28 + dy * .5)
    f.ellipse(41, 37, 8, 9.5, 'orange')                        # torso
    f.ellipse(45.5, 42, 7.5, 5.5, 'orange')                    # haunch
    f.ellipse(47, 44, 5, 3, 'shade')
    f.ellipse(40.5, 46.5, 3.2, 1.6, 'cream')                   # hind paw
    f.line((38, 38), (38, 46), 3, 'shade')                     # far front leg
    f.ellipse(38, 46.5, 2, 1.2, 'creamd')
    f.ellipse(35, 37.5, 4.6, 7.5, 'cream')                     # chest
    f.line((33, 39), (33, 46), 3, 'orange')                    # near front leg
    f.ellipse(32.6, 46.5, 2.2, 1.2, 'cream')
    head(f, 33, 25 + dy, blink=(i == 6))
    for x in range(31, 39): f.px(x, 32 + dy, 'red')            # collar
    f.px(33, 33 + dy, 'gold'); f.px(34, 33 + dy, 'gold')
    return f.render()

def leg(f, hip, angle, length, near=True):
    a = math.radians(angle)
    foot = (hip[0] - length * math.sin(a), hip[1] + length * math.cos(a))
    f.line(hip, foot, 3, 'orange' if near else 'shade')
    f.ellipse(foot[0] + .5, foot[1] + .5, 1.8, 1.2, 'cream' if near else 'creamd')

def run_frame(i):
    f = Frame()
    bob = [0, -1, -2, -1, 0, -1, -2, -1][i]
    ph = i / 8 * 2 * math.pi
    fa, ba = 38 * math.sin(ph), 38 * math.sin(ph + math.pi)
    # far legs (drawn first, darker)
    leg(f, (38, 35 + bob), fa + 25, 10, near=False)
    leg(f, (51, 34 + bob), ba + 25, 10.5, near=False)
    tail_curl(f, 56, 26 + bob, 4.2)
    f.ellipse(44, 32.5 + bob, 12, 5.3, 'orange')              # torso
    f.ellipse(42, 35.3 + bob, 7.5, 2.3, 'cream')              # belly
    leg(f, (36, 35 + bob), fa, 10, near=True)
    leg(f, (50, 34 + bob), ba, 10.5, near=True)
    head(f, 29, 26 + bob, ears_back=2)
    for y in range(28, 34): f.px(35, y + bob, 'red')
    f.px(34, 33 + bob, 'gold')
    return f.render()

def sheet(frames):
    return Image.fromarray(np.concatenate(frames, axis=1), 'RGBA')

def toy():
    n = 31; img = np.zeros((n, n, 4), np.uint8)
    ys, xs = np.mgrid[0:n, 0:n]; r = np.hypot(xs + .5 - n / 2, ys + .5 - n / 2)
    ball, ring = r <= 14, (r > 14) & (r <= 15)
    img[ball] = (206, 226, 72, 255); img[ring] = (92, 110, 30, 255)
    shade = ball & ((xs + ys) > 36); img[shade] = (176, 198, 52, 255)
    for cx in (-3.5, n + 3.5):                              # felt seams: two arcs bowing inward
        seam = ball & (np.abs(np.hypot(xs + .5 - cx, ys + .5 - n / 2) - 13.2) < .7) & (r <= 13.4)
        img[seam] = (250, 250, 236, 255)
    img[7:9, 9:11] = (238, 248, 170, 255)                  # highlight
    return Image.fromarray(img, 'RGBA').resize((186, 186), Image.NEAREST)

if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    sheet([idle_frame(i) for i in range(8)]).save(out / 'IDLE.png')
    sheet([run_frame(i) for i in range(8)]).save(out / 'RUN.png')
    toy().save(out / 'TOY.png')
