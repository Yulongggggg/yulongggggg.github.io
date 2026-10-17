"""Hand-placed chibi Shiba Inu pixel sprites for the website companion.

IDLE.png / RUN.png: 8 frames of 80x64 px (640x64), shown at 3x. Front-facing puppy, paws on row 47.
RUN is a hop cycle (squash, stretch, tongue out), so it reads correctly in either direction.
TOY.png: 31x31 px tennis ball scaled 6x. Original artwork; no third-party images.
Usage: python shiba.py OUTDIR
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

PAL = {
    'k': (112, 64, 36),    # outline, warm brown
    'O': (238, 152, 68),   # fur
    'o': (214, 124, 50),   # fur shade
    'C': (254, 245, 231),  # cream
    'c': (238, 220, 198),  # cream shade
    'e': (50, 36, 32),     # eye / nose
    'w': (255, 255, 255),  # eye highlight
    'p': (249, 166, 160),  # blush
    'i': (247, 184, 172),  # inner ear
    'r': (214, 66, 74),    # collar
    'y': (250, 206, 84),   # tag
    't': (238, 112, 122),  # tongue
}

def mirror(rows):
    """Each row gives the left 13 columns; the right half is its mirror image (26 columns total)."""
    return [r + r[::-1] for r in rows]

HEAD = mirror([
    "....kk.......",
    "...kOOk......",
    "..kOiiOk.....",
    "..kOiiiOk....",
    ".kOOiiiOOkkkk",
    ".kOOiiOOOOOOO",
    "kOOOOOOOOOOOO",
    "kOOOOOOCOOOOO",   # eyebrow dot
    "kOOOOOOOOOOOO",
    "kOOOOOOweOOOO",   # eyes
    "kOOOOOOeeOOOO",
    "kOCCCCCCCCCee",   # nose top
    "kCCCCppCCCCCe",   # blush, nose bottom
    "kCCCCCCCCCCke",   # mouth
    "kcCCCCCCCCCCC",
    ".kcCCCCCCCCCC",
    "..kkcCCCCCCCC",
])
# centre rows: 4-wide nose over a 2-wide tip, then a small mouth
HEAD[11] = "kOCCCCCCCCCeeeeCCCCCCCCCOk"
HEAD[12] = "kCCCCppCCCCCeeCCCCCppCCCCk"
HEAD[13] = "kCCCCCCCCCCkCCkCCCCCCCCCCk"

BODY = mirror([
    "...krrrrrrrrr",   # collar
    "...kOOOOCCCCy",   # cream bib narrowing to a V, tag
    "..kOOOOOOCCCC",
    "..kOOOOOOOCCC",
    ".kOOOOOOOOOCC",
    ".kOOOOOkOOOkC",   # two slim front legs start
    "kOOOOOOkOOOko",   # shadow between the legs
    "kOOOOOOkOOOko",
    "kOOOOOkCCCCko",   # white socks
    "kCCCCCkCcCCko",   # hind foot, toe line
    ".kkkkk.kkkkkk",
])

def tail_overlay(shift=0):
    """Curled tail peeking out on the right shoulder; drawn only where the body is empty or outline."""
    t = {(1, 24): 'k', (1, 25): 'k', (1, 26): 'k',
         (2, 23): 'k', (2, 24): 'O', (2, 25): 'O', (2, 26): 'O', (2, 27): 'k',
         (3, 23): 'k', (3, 24): 'O', (3, 25): 'C', (3, 26): 'O', (3, 27): 'k',
         (4, 24): 'O', (4, 25): 'O', (4, 26): 'k',
         (5, 24): 'k', (5, 25): 'k'}
    return {(r, c + shift): v for (r, c), v in t.items()}

def compose(head_dy=0, body_rows=None, blink=False, tongue=False, wag=0):
    head = [list(r) for r in HEAD]
    body = [list(r) for r in (body_rows or BODY)]
    if blink:
        for c in range(26):
            if head[9][c] in 'we': head[9][c] = 'O'
            if head[10][c] == 'e': head[10][c] = 'O'
        for c in (7, 8, 17, 18): head[10][c] = 'e'
    if tongue:
        head[14][12] = 't'; head[14][13] = 't'
    h = len(head); b = len(body)
    total = h + head_dy + b
    grid = [['.'] * 28 for _ in range(total + 1)]
    # body first (rows start where the head's last row is), then tail behind, then head on top
    top_body = h + head_dy
    for r, row in enumerate(body):
        for c, v in enumerate(row):
            if v != '.': grid[top_body + r][c] = v
    for (r, c), v in tail_overlay(wag).items():
        rr = top_body + r
        if 0 <= rr < len(grid) and 0 <= c < 28 and grid[rr][c] == '.': grid[rr][c] = v
    for r, row in enumerate(head):
        for c, v in enumerate(row):
            if v != '.':
                grid[r + head_dy][c] = v
    return [''.join(r) for r in grid]

def to_frame(rows, dy=0):
    img = np.zeros((64, 80, 4), np.uint8)
    h = len(rows); x0 = 40 - 13; y0 = 48 - h + dy
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v != '.' and 0 <= y0 + r < 64: img[y0 + r, x0 + c] = (*PAL[v], 255)
    return img

def squash(body):   # one row shorter: drop a chest row
    return body[:3] + body[4:]

def stretch(body):  # one row taller: repeat a chest row
    return body[:3] + [body[3]] + body[3:]

def idle_frames():
    spec = [(0, 0, False), (0, 1, False), (0, 0, False), (1, -1, False), (1, 0, False), (0, 1, True), (0, 0, False), (0, -1, False)]
    return [to_frame(compose(head_dy=hd, wag=w, blink=bl)) for hd, w, bl in spec]

def run_frames():
    spec = [(0, squash, 0), (-3, stretch, 0), (-6, stretch, 0), (-7, None, 1), (-6, None, 0), (-3, stretch, 0), (0, squash, 0), (0, None, 1)]
    out = []
    for dy, f, w in spec:
        body = f(BODY) if f else BODY
        out.append(to_frame(compose(body_rows=body, tongue=True, wag=w), dy))
    return out

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
