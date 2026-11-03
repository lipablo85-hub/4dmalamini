"""Pack the 10,000 dictionary pictures into sprite sheets: 25 pictures (5x5) per AVIF file.
Cuts 30,000 picture files to 800, which keeps the whole site under Cloudflare's 20,000-file limit.

    python3 tools/sprite_img.py --src enhanced --out sprites

Writes sprites/240/000.avif ... 399.avif (grid) and sprites/400/000.avif ... (enlarged view).
Sheet for number n = n // 25; cell = n % 25 -> column cell % 5, row cell // 5.
Run once (takes a few minutes); build.py only copies the result.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

PER, COLS = 25, 5


def one(job):
    src, out, sheet = job
    big = Image.new("RGB", (400 * COLS, 400 * COLS), (23, 42, 77))
    have = False
    for i in range(PER):
        n = sheet * PER + i
        f = Path(src) / f"{n:04d}.webp"
        if not f.exists():
            f = Path(src) / f"{n:04d}-400.avif"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB").resize((400, 400), Image.LANCZOS)
        big.paste(im, ((i % COLS) * 400, (i // COLS) * 400))
        have = True
    if not have:
        return 0
    big.save(Path(out) / "400" / f"{sheet:03d}.avif", "AVIF", quality=52, speed=6)
    big.resize((240 * COLS, 240 * COLS), Image.LANCZOS).save(Path(out) / "240" / f"{sheet:03d}.avif", "AVIF", quality=50, speed=6)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    for s in ("240", "400"):
        (Path(a.out) / s).mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor() as ex:
        n = sum(ex.map(one, [(a.src, a.out, s) for s in range(10000 // PER)]))
    print(f"{n} sheets written to {a.out}")


if __name__ == "__main__":
    main()
