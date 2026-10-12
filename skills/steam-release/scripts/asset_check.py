#!/usr/bin/env python3
"""Checks Steam store and library art in a folder for size and completeness.

File names (case-insensitive, .png or .jpg):
  header, small, main, vertical, background,
  library_capsule, library_header, library_hero, library_logo,
  screenshot_01, screenshot_02, ...

Example: python3 asset_check.py marketing/steam
Standard library only, runs on Windows too. Sizes as of 2026-10-12.
"""
import struct
import sys
from pathlib import Path

# name: (width, height, required)
EXACT = {
    "header": (920, 430, True),
    "small": (462, 174, True),
    "main": (1232, 706, True),
    "vertical": (748, 896, True),
    "background": (1438, 810, False),
    "library_capsule": (600, 900, True),
    "library_header": (920, 430, False),
    "library_hero": (3840, 1240, True),
}
MIN_SCREENSHOTS = 5


def png_info(data: bytes):
    w, h = struct.unpack(">II", data[16:24])
    color_type = data[25]
    alpha = color_type in (4, 6) or b"tRNS" in data[:4096]
    return w, h, alpha


def jpg_size(data: bytes):
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    raise ValueError("JPEG size not found")


def read_image(path: Path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return (*png_info(data), "png")
    if data[:2] == b"\xff\xd8":
        return (*jpg_size(data), False, "jpg")
    raise ValueError("neither PNG nor JPEG")


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) == 2 else 2
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        return 2

    errors, ok, found, shots = [], [], set(), 0
    for f in sorted(folder.iterdir()):
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        name = f.stem.lower()
        try:
            w, h, alpha, kind = read_image(f)
        except (ValueError, struct.error) as e:
            errors.append(f"{f.name}: unreadable ({e})")
            continue
        if name.startswith("screenshot"):
            shots += 1
            if w < 1920 or h < 1080 or w * 9 != h * 16:
                errors.append(f"{f.name}: {w}x{h}, needs at least 1920x1080 at 16:9")
            else:
                ok.append(f"{f.name}: {w}x{h}")
        elif name == "library_logo":
            found.add(name)
            if kind != "png" or not alpha:
                errors.append(f"{f.name}: must be a transparent PNG")
            elif w != 1280 and h != 720:
                errors.append(f"{f.name}: {w}x{h}, needs 1280 wide or 720 tall")
            else:
                ok.append(f"{f.name}: {w}x{h}, transparent")
        elif name in EXACT:
            found.add(name)
            ew, eh, _ = EXACT[name]
            if (w, h) != (ew, eh):
                errors.append(f"{f.name}: {w}x{h}, needs {ew}x{eh}")
            else:
                ok.append(f"{f.name}: {w}x{h}")
        else:
            errors.append(f"{f.name}: unknown name, see --help")

    required = {n for n, (_, _, req) in EXACT.items() if req} | {"library_logo"}
    for n in sorted(required - found):
        errors.append(f"missing: {n}")
    if shots < MIN_SCREENSHOTS:
        errors.append(f"only {shots} screenshots, needs at least {MIN_SCREENSHOTS}")

    for line in ok:
        print(f"OK     {line}")
    for line in errors:
        print(f"ERROR  {line}")
    print(f"\n{len(ok)} OK, {len(errors)} errors. Check content by eye (title as only text, gameplay only).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
