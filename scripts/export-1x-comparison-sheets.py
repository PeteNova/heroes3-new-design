"""Build original-versus-New Design 1× comparison sheets for the mods site."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MODULE_PATH = Path(__file__).with_name("export-roster-sprites.py")
SPEC = importlib.util.spec_from_file_location("export_roster_sprites", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
ROSTER_EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROSTER_EXPORT)

BUILD = ROSTER_EXPORT.BUILD
HPL = ROSTER_EXPORT.HPL
MODS_JSON = ROSTER_EXPORT.MODS_JSON
ROOT = ROSTER_EXPORT.ROOT
SHEET_DIR = ROSTER_EXPORT.SHEET_DIR
flatten_roster = ROSTER_EXPORT.flatten_roster
slugify = ROSTER_EXPORT.slugify


SCALE = 4
PORTRAIT_SIZE = (58 * SCALE, 64 * SCALE)
EXTRACTED = ROOT / "staging" / "hero-portraits-v1" / "extracted"


def load_original(hero: str) -> Image.Image:
    hpl = HPL[hero]
    for extension in (".bmp", ".png", ".PNG"):
        source = EXTRACTED / f"{hpl}{extension}"
        if source.is_file():
            with Image.open(source) as image:
                return image.convert("RGB").copy()
    raise FileNotFoundError(f"Missing original portrait for {hero}: {hpl}")


def load_new_design_1x(build_name: str, hero: str) -> Image.Image:
    hpl = HPL[hero]
    source = ROOT / "build" / build_name / "Content" / "Data" / f"{hpl}.PNG"
    if not source.is_file():
        raise FileNotFoundError(f"Missing 1× portrait for {hero}: {source}")
    with Image.open(source) as image:
        return image.convert("RGB").copy()


def write_sheet(
    pairs: list[tuple[str, Image.Image, Image.Image]], destination: Path
) -> None:
    columns = 8
    padding = 10
    gap = 6
    label_height = 28
    rows = (len(pairs) + columns - 1) // columns
    cell_width = PORTRAIT_SIZE[0] * 2 + gap + 2 * padding
    cell_height = PORTRAIT_SIZE[1] + label_height + 2 * padding
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (16, 14, 30))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=16)

    for index, (name, original, redesigned) in enumerate(pairs):
        column = index % columns
        row = index // columns
        x = column * cell_width + padding
        y = row * cell_height + padding
        sheet.paste(original.resize(PORTRAIT_SIZE, Image.Resampling.NEAREST), (x, y))
        sheet.paste(
            redesigned.resize(PORTRAIT_SIZE, Image.Resampling.NEAREST),
            (x + PORTRAIT_SIZE[0] + gap, y),
        )
        box = draw.textbbox((0, 0), name, font=font)
        draw.text(
            (x + (PORTRAIT_SIZE[0] * 2 + gap - (box[2] - box[0])) // 2, y + PORTRAIT_SIZE[1] + 6),
            name,
            fill=(235, 231, 255),
            font=font,
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, format="PNG", optimize=True)


def main() -> None:
    catalog = json.loads(MODS_JSON.read_text(encoding="utf-8"))
    for mod in catalog["mods"]:
        slug = mod["slug"]
        build_name = BUILD[slug]
        pairs = [
            (
                slugify(name),
                load_original(slugify(name)),
                load_new_design_1x(build_name, slugify(name)),
            )
            for name in flatten_roster(mod)
        ]
        destination = SHEET_DIR / f"{slug}-original-vs-1x.png"
        write_sheet(pairs, destination)
        print(f"{slug}: {destination.name}")


if __name__ == "__main__":
    main()
