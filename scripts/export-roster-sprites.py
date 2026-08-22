"""Build roster sprites and labelled HPL sheets for the mods-site.

Uses Data4x (232×256, lanczos from masters) so every faction has the same
HD standard — not nearest-neighbour upscales of 58×64.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
ROOT = SITE.parent
MODS_JSON = SITE / "mods.json"
OUT_DIR = SITE / "assets" / "portraits"
SHEET_DIR = SITE / "assets" / "sheets"

COLS = 4
CELL = (116, 128)
HPL_CELL = (232, 256)
HPL_LABEL = 30
HPL_PAD = 12
EXTRACTED = ROOT / "staging" / "hero-portraits-v1" / "extracted"
WEB_OVERRIDES = {
    ("fortress", "voy"): OUT_DIR / "voy-fortress-v1-8.png",
}

BUILD = {
    "castle": "vcmi-hero-portraits-castle-v1",
    "rampart": "vcmi-hero-portraits-rampart-v1",
    "tower": "vcmi-hero-portraits-tower-v1",
    "inferno": "vcmi-hero-portraits-inferno-v1",
    "necropolis": "vcmi-hero-portraits-necropolis-v1",
    "dungeon": "vcmi-hero-portraits-dungeon-v1",
    "stronghold": "vcmi-hero-portraits-stronghold-v1",
    "fortress": "vcmi-hero-portraits-fortress-v1",
    "conflux": "vcmi-hero-portraits-conflux-v1",
    "factory": "vcmi-hero-portraits-factory-v1",
    "cove": "vcmi-hero-portraits-cove-v1",
}

FACTORY_EXTRACTED = ROOT / "staging" / "hero-portraits-factory-v1" / "extracted"
COVE_EXTRACTED = ROOT / "staging" / "hero-portraits-cove-v1" / "extracted"
HOTA_SPRITE_FACTIONS = {"factory", "cove"}

HPL = {
    "orrin": "HPL000KN",
    "valeska": "HPL001KN",
    "edric": "HPL002KN",
    "sylvia": "HPL003KN",
    "lord-haart": "HPL004KN",
    "sorsha": "HPL005KN",
    "christian": "HPL006KN",
    "tyris": "HPL007KN",
    "rion": "HPL008CL",
    "adela": "HPL009CL",
    "cuthbert": "HPL010CL",
    "adelaide": "HPL011CL",
    "ingham": "HPL012CL",
    "sanya": "HPL013CL",
    "loynis": "HPL014CL",
    "caitlin": "HPL015CL",
    "mephala": "HPL016RN",
    "ufretin": "HPL017RN",
    "jenova": "HPL018RN",
    "ryland": "HPL019RN",
    "thorgrim": "HPL020RN",
    "ivor": "HPL021RN",
    "clancy": "HPL022RN",
    "kyrre": "HPL023RN",
    "coronius": "HPL024DR",
    "uland": "HPL025DR",
    "elleshar": "HPL026DR",
    "gem": "HPL027DR",
    "malcom": "HPL028DR",
    "melodia": "HPL029DR",
    "alagar": "HPL030DR",
    "aeris": "HPL031DR",
    "piquedram": "HPL032AL",
    "thane": "HPL033AL",
    "josephine": "HPL034AL",
    "neela": "HPL035AL",
    "torosar": "HPL036AL",
    "fafner": "HPL037AL",
    "rissa": "HPL038AL",
    "iona": "HPL039AL",
    "astral": "HPL040WZ",
    "halon": "HPL041WZ",
    "serena": "HPL042WZ",
    "daremyth": "HPL043WZ",
    "theodorus": "HPL044WZ",
    "solmyr": "HPL045WZ",
    "cyra": "HPL046WZ",
    "aine": "HPL047WZ",
    "fiona": "HPL048HR",
    "rashka": "HPL049HR",
    "marius": "HPL050HR",
    "ignatius": "HPL051HR",
    "octavia": "HPL052HR",
    "calh": "HPL053HR",
    "pyre": "HPL054HR",
    "nymus": "HPL055HR",
    "ayden": "HPL056DM",
    "xyron": "HPL057DM",
    "axsis": "HPL058DM",
    "olema": "HPL059DM",
    "calid": "HPL060DM",
    "ash": "HPL061DM",
    "zydar": "HPL062DM",
    "xarfax": "HPL063DM",
    "straker": "HPL064DK",
    "vokial": "HPL065DK",
    "moandor": "HPL066DK",
    "charna": "HPL067DK",
    "tamika": "HPL068DK",
    "isra": "HPL069DK",
    "clavius": "HPL070DK",
    "galthran": "HPL071DK",
    "septienna": "HPL072NC",
    "aislinn": "HPL073NC",
    "sandro": "HPL074NC",
    "nimbus": "HPL075NC",
    "thant": "HPL076NC",
    "xsi": "HPL077NC",
    "vidomina": "HPL078NC",
    "nagash": "HPL079NC",
    "lorelei": "HPL080OV",
    "arlach": "HPL081OV",
    "dace": "HPL082OV",
    "ajit": "HPL083OV",
    "damacon": "HPL084OV",
    "gunnar": "HPL085OV",
    "synca": "HPL086OV",
    "shakti": "HPL087OV",
    "alamar": "HPL088WL",
    "jaegar": "HPL089WL",
    "malekith": "HPL090WL",
    "jeddite": "HPL091WL",
    "geon": "HPL092WL",
    "deemer": "HPL093WL",
    "sephinroth": "HPL094WL",
    "darkstorn": "HPL095WL",
    "yog": "HPL096BR",
    "gurnisson": "HPL097BR",
    "jabarkas": "HPL098BR",
    "shiva": "HPL099BR",
    "gretchin": "HPL100BR",
    "krellion": "HPL101BR",
    "crag-hack": "HPL102BR",
    "tyraxor": "HPL103BR",
    "gird": "HPL104BM",
    "vey": "HPL105BM",
    "dessa": "HPL106BM",
    "terek": "HPL107BM",
    "zubin": "HPL108BM",
    "gundula": "HPL109BM",
    "oris": "HPL110BM",
    "saurug": "HPL111BM",
    "bron": "HPL112BS",
    "drakon": "HPL113BS",
    "wystan": "HPL114BS",
    "tazar": "HPL115BS",
    "alkin": "HPL116BS",
    "korbac": "HPL117BS",
    "gerwulf": "HPL118BS",
    "broghild": "HPL119BS",
    "mirlanda": "HPL120WH",
    "rosic": "HPL121WH",
    "voy": "HPL122WH",
    "verdish": "HPL123WH",
    "merist": "HPL124WH",
    "styg": "HPL125WH",
    "andra": "HPL126WH",
    "tiva": "HPL127WH",
    "pasis": "HPL000PL",
    "thunar": "HPL001PL",
    "ignissa": "HPL002PL",
    "lacus": "HPL003PL",
    "monere": "HPL004PL",
    "erdamon": "HPL005PL",
    "fiur": "HPL006PL",
    "kalt": "HPL007PL",
    "luna": "HPL000EL",
    "brissa": "HPL001EL",
    "ciele": "HPL002EL",
    "labetha": "HPL003EL",
    "inteus": "HPL004EL",
    "aenain": "HPL005EL",
    "gelare": "HPL006EL",
    "grindan": "HPL007EL",
    # Factory (HotA) — no HPL codes; slug is the portrait key
    "henrietta": "FACTORY",
    "sam": "FACTORY",
    "tancred": "FACTORY",
    "melchior": "FACTORY",
    "floribert": "FACTORY",
    "wynona": "FACTORY",
    "dury": "FACTORY",
    "morton": "FACTORY",
    "celestine": "FACTORY",
    "todd": "FACTORY",
    "agar": "FACTORY",
    "bertram": "FACTORY",
    "wrathmont": "FACTORY",
    "ziph": "FACTORY",
    "victoria": "FACTORY",
    "eanswythe": "FACTORY",
    # Cove (HotA) — no HPL codes; slug is the portrait key
    "corkes": "COVE",
    "jeremy": "COVE",
    "illor": "COVE",
    "elmore": "COVE",
    "derek": "COVE",
    "leena": "COVE",
    "anabel": "COVE",
    "cassiopeia": "COVE",
    "miriam": "COVE",
    "casmetra": "COVE",
    "eovacius": "COVE",
    "spint": "COVE",
    "andal": "COVE",
    "manfred": "COVE",
    "zilare": "COVE",
    "astra": "COVE",
    "dargem": "COVE",
}


def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def flatten_roster(mod: dict) -> list[str]:
    names: list[str] = []
    for group in (mod.get("roster") or {}).values():
        names.extend(group)
    return names


def load_hpl4x(faction: str, build_name: str, hero: str) -> Image.Image:
    override = WEB_OVERRIDES.get((faction, hero))
    if override is not None:
        src = override
    elif faction in HOTA_SPRITE_FACTIONS:
        src = (
            ROOT
            / "build"
            / build_name
            / "Content"
            / "sprites4x"
            / "hota"
            / faction
            / "heroes"
            / hero
            / "icons"
            / "portraitLarge.png"
        )
    else:
        hpl = HPL.get(hero)
        if not hpl or hpl in {"FACTORY", "COVE"}:
            raise SystemExit(f"No HPL id for {hero}")
        src = ROOT / "build" / build_name / "Content" / "Data4x" / f"{hpl}.PNG"
    if not src.is_file():
        raise SystemExit(f"Missing {src}")
    with Image.open(src) as image:
        portrait = image.convert("RGBA")
        if portrait.size != HPL_CELL:
            portrait = portrait.resize(HPL_CELL, Image.Resampling.LANCZOS)
        return portrait.copy()


def load_original(hero: str, *, faction: str | None = None) -> Image.Image:
    if faction == "factory" or HPL.get(hero) == "FACTORY":
        src = FACTORY_EXTRACTED / f"{hero}-portraitLarge.png"
        if not src.is_file():
            raise SystemExit(f"Missing original HotA portrait for {hero}: {src}")
        with Image.open(src) as image:
            return image.convert("RGBA").copy()
    if faction == "cove" or HPL.get(hero) == "COVE":
        src = COVE_EXTRACTED / f"{hero}-portraitLarge.png"
        if not src.is_file():
            raise SystemExit(f"Missing original HotA portrait for {hero}: {src}")
        with Image.open(src) as image:
            return image.convert("RGBA").copy()
    hpl = HPL.get(hero)
    if not hpl:
        raise SystemExit(f"No HPL id for {hero}")
    for extension in (".bmp", ".png", ".PNG"):
        src = EXTRACTED / f"{hpl}{extension}"
        if src.is_file():
            with Image.open(src) as image:
                return image.convert("RGBA").copy()
    raise SystemExit(f"Missing original portrait for {hero}: {hpl}")


def write_roster(
    names: list[str],
    portraits: list[Image.Image],
    dest: Path,
    resampling: Image.Resampling = Image.Resampling.LANCZOS,
) -> None:
    rows = (len(names) + COLS - 1) // COLS
    sheet = Image.new("RGBA", (COLS * CELL[0], rows * CELL[1]), (0, 0, 0, 0))
    for index, portrait in enumerate(portraits):
        thumb = portrait.resize(CELL, resampling)
        col, row = index % COLS, index // COLS
        sheet.paste(thumb, (col * CELL[0], row * CELL[1]))
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, format="PNG", optimize=True)


def write_hpl_sheet(names: list[str], portraits: list[Image.Image], dest: Path) -> None:
    rows = (len(names) + COLS - 1) // COLS
    cell_w = HPL_CELL[0] + 2 * HPL_PAD
    cell_h = HPL_CELL[1] + HPL_LABEL + 2 * HPL_PAD
    sheet = Image.new("RGB", (COLS * cell_w, rows * cell_h), (16, 14, 30))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    for index, (name, portrait) in enumerate(zip(names, portraits)):
        col, row = index % COLS, index // COLS
        x = col * cell_w + HPL_PAD
        y = row * cell_h + HPL_PAD
        sheet.paste(portrait.convert("RGB"), (x, y))
        label = slugify(name)
        box = draw.textbbox((0, 0), label, font=font)
        text_w = box[2] - box[0]
        draw.text(
            (x + (HPL_CELL[0] - text_w) // 2, y + HPL_CELL[1] + 6),
            label,
            fill=(235, 231, 255),
            font=font,
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, format="PNG", optimize=True)


def main() -> None:
    catalog = json.loads(MODS_JSON.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SHEET_DIR.mkdir(parents=True, exist_ok=True)
    for mod in catalog["mods"]:
        slug = mod["slug"]
        names = flatten_roster(mod)
        if not names:
            continue
        build_name = BUILD.get(slug)
        if not build_name:
            raise SystemExit(f"No build folder mapping for {slug}")
        portraits = [
            load_hpl4x(slug, build_name, slugify(name)) for name in names
        ]
        originals = [load_original(slugify(name), faction=slug) for name in names]
        roster = OUT_DIR / f"{slug}-roster.png"
        original_roster = OUT_DIR / f"{slug}-original-roster.png"
        hpl_sheet = SHEET_DIR / f"{slug}-hpl.png"
        write_roster(names, portraits, roster)
        write_roster(names, originals, original_roster, Image.Resampling.NEAREST)
        write_hpl_sheet(names, portraits, hpl_sheet)
        print(f"{slug}: {roster.name} + {original_roster.name} + {hpl_sheet.name}")


if __name__ == "__main__":
    main()
