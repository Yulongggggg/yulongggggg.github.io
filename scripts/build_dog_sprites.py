"""Build the companion sprite sheets from kyafu's free "Shiba Inu" character chip.

Source: https://kyafupaca.itch.io/shiba-inu (shibainu.png, 192x192, 3 columns x 4 rows of 64x48;
rows: front, left, right, back). Licence: commercial use and modification allowed, redistribution of
modified data allowed, credit "kyafu" appreciated. The unmodified file is not stored in this repository;
download it and run:
    python scripts/build_dog_sprites.py path/to/shibainu.png site/dog

Output (8 frames of 80x64 px each, shown at 2x by site/style.css):
  IDLE.png  standing side view, tongue out, panting (head and back rise one pixel on alternate beats)
  RUN.png   left-facing walk cycle 0-1-2-1, twice (the page mirrors it when running right)
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

CELL_W, CELL_H, FW, FH = 64, 48, 80, 64

def cell(sheet, row, col):
    return np.array(sheet.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)))

def frame(c, dx=0):
    f = np.zeros((FH, FW, 4), np.uint8)
    y0, x0 = FH - CELL_H - 2, (FW - CELL_W) // 2 + dx
    f[y0:y0 + CELL_H, x0:x0 + CELL_W] = c
    return f

def breathe(c, split):
    """Lift everything above row `split` by one pixel (head and shoulders rise)."""
    out = c.copy(); out[0:split - 1] = c[1:split]; out[split - 1] = c[split - 1]
    return out

def main(src, out):
    sheet = Image.open(src).convert('RGBA')
    assert sheet.size == (192, 192), sheet.size
    stand = cell(sheet, 1, 1)
    up = breathe(stand, 32)
    idle = [stand, stand, up, up, stand, stand, up, stand]
    walk = [cell(sheet, 1, c) for c in (0, 1, 2, 1, 0, 1, 2, 1)]
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.concatenate([frame(c) for c in idle], 1), 'RGBA').save(out / 'IDLE.png')
    Image.fromarray(np.concatenate([frame(c) for c in walk], 1), 'RGBA').save(out / 'RUN.png')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
