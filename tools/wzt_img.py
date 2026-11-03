#!/usr/bin/env python3
"""Enhance + optimise square 万字图 pictures for the 4D Dictionary.

Usage: python3 wzt_img.py <input_folder(s)...> <output_folder>
Input: NNNN.jpg (0000-9999), any sub-folder depth. Other files are ignored.
Output per number (originals are 200px; nothing real is lost at 240):
  NNNN-240.avif  grid thumbnail          ~4 KB
  NNNN-400.avif  enlarged view (2x)      ~7 KB
  NNNN.webp      400px fallback for older phones without AVIF  ~12 KB
Enhance: 2x Lanczos upscale -> edge-preserving smooth of JPEG noise -> gentle sharpen of line art
         -> slight colour lift -> metadata stripped.
"""
import re, sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SIZE = 400


def enhance(base: Image.Image, size: int) -> Image.Image:
    im = base.resize((size, size), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6 if size > 300 else 1.0, percent=80, threshold=3))
    im = ImageEnhance.Color(im).enhance(1.08)
    return ImageEnhance.Contrast(im).enhance(1.04)


def process(src: Path, out: Path, n: str) -> int:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im = ImageOps.fit(im, (min(im.size),) * 2, Image.LANCZOS)          # make square if needed
    im = im.filter(ImageFilter.MedianFilter(3))                          # remove JPEG speckle
    small, big = enhance(im, 240), enhance(im, SIZE)
    small.save(out / f"{n}-240.avif", "AVIF", quality=45, speed=6)
    big.save(out / f"{n}-400.avif", "AVIF", quality=50, speed=6)
    big.save(out / f"{n}.webp", "WEBP", quality=75, method=6)
    return sum((out / f).stat().st_size for f in (f"{n}-240.avif", f"{n}-400.avif", f"{n}.webp"))


def main(args: list[str]) -> None:
    *ins, out = args
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    seen = {}
    for d in ins:
        for p in sorted(Path(d).rglob("*.jpg")):
            m = re.fullmatch(r"(\d{4})", p.stem)
            if not m:
                continue
            n = m.group(1)
            if n in seen:
                print(f"  ! duplicate {n}: {p} (kept {seen[n]})")
                continue
            seen[n] = p
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as ex:
        total = sum(ex.map(process, seen.values(), [out] * len(seen), seen.keys(), chunksize=20))
    print(f"{len(seen)} pictures -> {out}  ({total/1048576:.1f} MB all formats; a visitor downloads ~4 KB per grid picture)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1:])
