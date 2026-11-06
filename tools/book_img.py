"""Pack a 1,000-entry book (Tua Pek Kong 000-999, Guan Yin Ma 000-999) into 40 AVIF sprite sheets of 25 (5x5).
One size only: the originals are 100-200 px, so 200 px cells serve the grid and the enlarged view alike.

    python3 tools/book_img.py SRC_DIR OUT_DIR      # SRC has 000.webp ... 999.webp

Sheet for number n = n // 25; cell = n % 25 -> column cell % 5, row cell // 5.
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image

PER, COLS, CELL = 25, 5, 200


def one(job):
    src, out, sheet = job
    big = Image.new("RGB", (CELL * COLS, CELL * COLS), (255, 255, 255))
    for i in range(PER):
        f = Path(src) / f"{sheet * PER + i:03d}.webp"
        if f.exists():
            im = Image.open(f).convert("RGB")
            if im.size != (CELL, CELL):
                im = im.resize((CELL, CELL), Image.LANCZOS)
            big.paste(im, ((i % COLS) * CELL, (i // COLS) * CELL))
    big.save(Path(out) / f"{sheet:02d}.avif", "AVIF", quality=55, speed=6)
    return (Path(out) / f"{sheet:02d}.avif").stat().st_size


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    Path(out).mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor() as ex:
        sizes = list(ex.map(one, [(src, out, s) for s in range(1000 // PER)]))
    print(f"{len(sizes)} sheets, {sum(sizes) / 1024:.0f} KB total, avg {sum(sizes) / len(sizes) / 1024:.1f} KB")
