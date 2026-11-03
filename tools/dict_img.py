#!/usr/bin/env python3
"""4D Dictionary photo pipeline: enhance + optimise photos for mobile.

Usage:
  python3 dict_img.py <input_folder> <output_folder> [--motion] [--gif]
  --motion  also make {n}-anim.mp4: a 4-second silent looping slow zoom-and-drift (~40-120 KB)
  --gif     also make {n}-anim.gif (only if something insists on GIF; much heavier)

Input: images named by 万字图 number 0000-9999, e.g. 0001.jpg, 0027.png, 9999.webp.
       The first number in the file name is used and padded to 4 digits, so "1.jpg", "wzt_0001.png"
       and "0001-tiger.jpg" all become 0001. Duplicates are reported, not overwritten.
Output per number (4:3, centre-cropped):
  0001-320.avif  0001-320.webp   (card thumbnail, ~6-15 KB)
  0001-960.avif  0001-960.webp   (tap-to-zoom view, ~30-70 KB)
  manifest.json  {"0001": {"w":960,"h":720,"lqip":"data:image/webp;base64,..."}, ...}

Enhancement (gentle, keeps photos natural):
  auto-orient (EXIF) -> remove colour cast (autocontrast 0.5% clip) -> slight
  saturation lift -> denoise-safe sharpen after resize (UnsharpMask) ->
  sRGB, metadata stripped.
For blurry/small originals, run an AI upscale first (2x-4x), then this script.
"""
import base64, io, json, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SIZES = (320, 960)
RATIO = 4 / 3


def enhance(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=0.5, preserve_tone=True)
    im = ImageEnhance.Color(im).enhance(1.06)
    return im


def crop43(im: Image.Image) -> Image.Image:
    w, h = im.size
    if w / h > RATIO:
        nw = int(h * RATIO)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / RATIO)
    return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


MOTION = False   # set by --motion
GIF = False      # set by --gif (old-style GIF too; 5-10x heavier, only if a platform demands GIF)


def make_motion(im: Image.Image, out: Path, n: str, w: int = 480, frames: int = 30) -> None:
    """Slow cinematic push-in + drift ("Ken Burns"), looped back and forth: {n}-anim.mp4 (480x360, 4 s)."""
    W, H = im.size
    seq = []
    for i in range(frames):
        t = i / (frames - 1)
        e = t * t * (3 - 2 * t)                     # ease in/out
        z = 1.0 + 0.10 * e                          # zoom 100% -> 110%
        cw, ch = W / z, H / z
        x = (W - cw) * (0.35 + 0.30 * e)            # drift left -> right
        y = (H - ch) * (0.55 - 0.20 * e)            # and slightly upward
        f = im.crop((round(x), round(y), round(x + cw), round(y + ch))).resize((w, round(w / RATIO)), Image.LANCZOS)
        seq.append(f.filter(ImageFilter.UnsharpMask(radius=1.0, percent=50, threshold=2)))
    loop = seq + seq[-2:0:-1]                       # ping-pong, seamless
    tmp = out / f".{n}-frames"
    tmp.mkdir(exist_ok=True)
    for i, f in enumerate(loop):
        f.save(tmp / f"{i:03d}.png")
    # H.264 MP4: plays muted/looping inline on every phone; ~10x smaller than animated WebP, ~30x smaller than GIF
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "15", "-i", str(tmp / "%03d.png"),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", "-an", str(out / f"{n}-anim.mp4")], check=True)
    if GIF:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "15", "-i", str(tmp / "%03d.png"),
                        "-vf", "split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer",
                        "-loop", "0", str(out / f"{n}-anim.gif")], check=True)
    shutil.rmtree(tmp)


def main(src: str, dst: str) -> None:
    out = Path(dst)
    out.mkdir(parents=True, exist_ok=True)
    manifest, warn = {}, []
    files = sorted((p for p in Path(src).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}), key=lambda p: p.name)
    for p in files:
        m = re.search(r"\d+", p.stem)
        if not m or int(m.group()) > 9999:
            warn.append(f"skipped (no number 0-9999 in name): {p.name}")
            continue
        n = f"{int(m.group()):04d}"
        if n in manifest:
            warn.append(f"duplicate number {n}: {p.name} skipped")
            continue
        im = crop43(enhance(Image.open(p)))
        if im.width < 960:
            warn.append(f"{p.name}: only {im.width}px wide - upscale for sharp zoom view")
        for s in SIZES:
            r = im.resize((s, round(s / RATIO)), Image.LANCZOS)
            r = r.filter(ImageFilter.UnsharpMask(radius=1.0 if s == 320 else 1.4, percent=60, threshold=2))
            r.save(out / f"{n}-{s}.webp", "WEBP", quality=78 if s == 320 else 80, method=6)
            r.save(out / f"{n}-{s}.avif", "AVIF", quality=55 if s == 320 else 60)
        if MOTION:
            make_motion(im, out, n)
        tiny = im.resize((16, 12), Image.LANCZOS)
        b = io.BytesIO()
        tiny.save(b, "WEBP", quality=40)
        manifest[n] = {"w": 960, "h": 720, "lqip": "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()}
        if MOTION:
            manifest[n]["anim"] = 1
    (out / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")))
    total = sum(f.stat().st_size for f in out.iterdir())
    print(f"{len(manifest)} photos -> {out}  ({total/1024:.0f} KB total)")
    for w in warn:
        print("  !", w)


if __name__ == "__main__":
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2 or flags - {"--motion", "--gif"}:
        sys.exit(__doc__)
    MOTION = "--motion" in flags or "--gif" in flags
    GIF = "--gif" in flags
    main(args[0], args[1])
