#!/usr/bin/env python3
"""Render setiap .html di posts/ menjadi PNG 1080x1350 via chrome headless.

Usage:
    python3 render.py              # semua slide
    python3 render.py p1           # hanya file yang namanya mengandung 'p1'
"""
import os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "exports")

CANDIDATES = [
    os.environ.get("CHROME_BIN", ""),
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"),
]


def find_chrome():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    hits = sorted(glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome")))
    return hits[-1] if hits else "google-chrome"


CHROME = find_chrome()


def render(html_path, png_path):
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--window-size=1080,1350",
        f"--screenshot={png_path}",
        "--default-background-color=FFFFFFFF",
        f"file://{html_path}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(png_path):
        print("FAIL", html_path, r.stderr[-800:])
        return False
    # Ratakan RGBA transparan ke putih — Instagram menolak PNG transparan
    try:
        from PIL import Image
        im = Image.open(png_path)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            bg.save(png_path, optimize=True)
    except ImportError:
        pass
    return True


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(ROOT, "posts", "*.html")))
    if only:
        files = [f for f in files if only in os.path.basename(f)]
    if not files:
        print("Tidak ada file di posts/")
        return

    ok = 0
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        png = os.path.join(OUT, name + ".png")
        if render(f, png):
            try:
                from PIL import Image
                im = Image.open(png)
                size = f"{im.size[0]}x{im.size[1]}"
            except ImportError:
                size = "?"
            print(f"OK  {name:42s} {size}  {os.path.getsize(png)//1024}KB")
            ok += 1
    print(f"\n{ok}/{len(files)} rendered -> {OUT}")


if __name__ == "__main__":
    main()
