"""Data loading and management for Quran translations."""

import json
import subprocess
import sys
from pathlib import Path

QURAN_DB_REPO = "https://github.com/ZainRizvi/quran_db.git"
QURAN_DB_DIR = Path(__file__).parent.parent / "quran_db"
SURAH_METADATA_PATH = Path(__file__).parent / "surah_metadata.json"


def ensure_quran_db() -> Path:
    """Ensure quran_db repo is cloned and up to date. Returns the path to the repo."""
    if not QURAN_DB_DIR.exists():
        print(f"Cloning quran_db repository to {QURAN_DB_DIR}...", file=sys.stderr)
        subprocess.run(
            ["git", "clone", "--depth", "1", QURAN_DB_REPO, str(QURAN_DB_DIR)],
            check=True,
        )
        print("Done.", file=sys.stderr)
    return QURAN_DB_DIR


def get_available_translations() -> list[str]:
    """Get list of available translation file names (without .json extension)."""
    db_path = ensure_quran_db()
    translations = []
    for json_file in db_path.glob("*.json"):
        name = json_file.stem
        # Skip non-translation files
        if name not in ("transliteration", "transliteration2"):
            translations.append(name)
    return sorted(translations)


def load_translation(name: str) -> dict:
    """Load a translation JSON file by name."""
    db_path = ensure_quran_db()
    json_path = db_path / f"{name}.json"
    if not json_path.exists():
        raise ValueError(f"Translation '{name}' not found at {json_path}")
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def load_surah_metadata() -> list[dict]:
    """Load surah metadata (for Meccan/Medinan info)."""
    with open(SURAH_METADATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_surah_type(surah_num: int, metadata: list[dict]) -> str:
    """Get the type (meccan/medinan) for a surah number."""
    # metadata is 0-indexed, surah numbers are 1-indexed
    if 1 <= surah_num <= len(metadata):
        place = metadata[surah_num - 1]["place"].lower()
        return "meccan" if place == "mecca" else "medinan"
    return "unknown"


def get_translator_display_name(translation_data: dict) -> str:
    """Extract the display name of the translator from the translation data.

    The translator name is stored as a key in each verse's Ayahs dict.
    """
    # Get first surah, first ayah to find the translator key
    first_surah = translation_data.get("1", {})
    first_ayah = first_surah.get("Ayahs", {}).get("1", {})
    if first_ayah:
        # Return the first (and usually only) key
        return next(iter(first_ayah.keys()))
    return "Unknown"
