"""Generate Obsidian markdown files for Quran verses and surahs."""

import html
import re
from pathlib import Path

from .data import (
    get_surah_type,
    get_translator_display_name,
    load_surah_metadata,
    load_translation,
)


def strip_arabic_verse_markers(text: str) -> str:
    """Remove Arabic verse end markers (۝ followed by digits) from text."""
    # Match the verse marker ۝ followed by any Arabic-Indic digits (٠-٩)
    # Also match the non-breaking space that often precedes it
    return re.sub(r"\s*[\u06dd][\u0660-\u0669]+", "", text)


def decode_html_entities(text: str) -> str:
    """Decode HTML entities like &mdash; and &#91; to their actual characters."""
    return html.unescape(text)


def format_surah_name_for_file(transliterated_name: str, surah_num: int) -> str:
    """Format surah name for file naming: '1 - Surah al-Fatihah'."""
    return f"{surah_num} - Surah {transliterated_name}"


def generate_surah_file(
    surah_num: int,
    arabic_data: dict,
    surah_metadata: list[dict],
) -> str:
    """Generate the markdown content for a surah file."""
    surah_data = arabic_data[str(surah_num)]
    transliterated_name = surah_data["SurahTransliteratedName"]
    arabic_name = surah_data["SurahArabicName"]
    english_name = surah_data["SurahEnglishNames"]
    total_verses = len(surah_data["Ayahs"])
    surah_type = get_surah_type(surah_num, surah_metadata)

    # Build aliases
    aliases = [
        f"Surah {arabic_name}",
        f"Surah {transliterated_name}",
        f"Surah {english_name}",
    ]

    # Build verses list
    verses_list = "\n".join(f"- [[Quran {surah_num}-{v}]]" for v in range(1, total_verses + 1))

    content = f"""---
surah_num: {surah_num}
name: {arabic_name}
translation: {english_name}
total_verses: {total_verses}
type: {surah_type}
aliases:
  - {aliases[0]}
  - {aliases[1]}
  - {aliases[2]}
---
# Surah **{arabic_name}**

# Notes

# References
```dataview
list
from [[]]
where !contains(surah_num, {surah_num})
```

# Verses
{verses_list}

"""
    return content


def generate_verse_file(
    surah_num: int,
    verse_num: int,
    total_verses: int,
    transliterated_name: str,
    translations_data: list[tuple[str, dict, str]],  # [(name, data, display_name), ...]
    arabic_data: dict,
) -> str:
    """Generate the markdown content for a verse file.

    translations_data is a list of tuples: (translation_name, translation_data, display_name)
    where translation_name is e.g. 'arabic' and display_name is e.g. 'Arabic'
    """
    surah_file_name = format_surah_name_for_file(transliterated_name, surah_num)

    # Build prev/next links
    links_parts = []
    if verse_num > 1:
        links_parts.append(f"[[Quran {surah_num}-{verse_num - 1}|prev verse]]")
    if verse_num < total_verses:
        links_parts.append(f"[[Quran {surah_num}-{verse_num + 1}|next verse]]")
    links_str = ", ".join(links_parts)

    # Build sources section
    sources_parts = []
    citation = f"Quran {surah_num}:{verse_num}, Surah {transliterated_name}"

    for trans_name, trans_data, display_name in translations_data:
        verse_text = trans_data[str(surah_num)]["Ayahs"][str(verse_num)].get(display_name, "")

        if trans_name == "arabic":
            # Arabic gets special formatting with <big> tags and no quotes
            cleaned_text = strip_arabic_verse_markers(verse_text)
            sources_parts.append(
                f"##### {display_name}\n<big><big><big>{cleaned_text}</big></big></big>\n--{citation}"
            )
        else:
            # Regular translations get quotes and decode HTML entities
            cleaned_text = decode_html_entities(verse_text)
            sources_parts.append(f'##### {display_name}\n"{cleaned_text}"  --{citation}')

    sources_str = "\n\n".join(sources_parts)

    content = f"""---
surah_num: {surah_num}
verse: {verse_num}
aliases:
  - Quran {surah_num}:{verse_num}
  - Surah {transliterated_name} {surah_num}:{verse_num}
---
[[{surah_file_name}]], Verse {verse_num}

Links: {links_str}

# Sources

{sources_str}


# Notes Refrencing Verse
```dataview
list
from [[]]
where !contains(surah_num, {surah_num})
```

"""
    return content


def generate_quran_files(
    output_dir: Path,
    translation_names: list[str],
) -> None:
    """Generate all Quran verse and surah files.

    Args:
        output_dir: Directory to write output files to
        translation_names: List of translation names to include (e.g., ['thestudyquran', 'arabic'])
    """
    # Create output directories
    surahs_dir = output_dir / "Surahs"
    verses_dir = output_dir / "Verses"
    surahs_dir.mkdir(parents=True, exist_ok=True)
    verses_dir.mkdir(parents=True, exist_ok=True)

    # Load metadata
    surah_metadata = load_surah_metadata()

    # Load all translations
    translations_data = []
    for name in translation_names:
        data = load_translation(name)
        display_name = get_translator_display_name(data)
        translations_data.append((name, data, display_name))

    # Use arabic data for surah info (or first translation if arabic not in list)
    arabic_data = None
    for name, data, _ in translations_data:
        if name == "arabic":
            arabic_data = data
            break
    if arabic_data is None:
        # Load arabic separately for surah metadata
        arabic_data = load_translation("arabic")

    # Generate files for all 114 surahs
    total_surahs = 114
    for surah_num in range(1, total_surahs + 1):
        surah_info = arabic_data[str(surah_num)]
        transliterated_name = surah_info["SurahTransliteratedName"]
        total_verses = len(surah_info["Ayahs"])

        # Generate surah file
        surah_content = generate_surah_file(surah_num, arabic_data, surah_metadata)
        surah_filename = f"{format_surah_name_for_file(transliterated_name, surah_num)}.md"
        surah_path = surahs_dir / surah_filename
        surah_path.write_text(surah_content, encoding="utf-8")

        # Create verse subdirectory
        verse_subdir = verses_dir / f"Surah {surah_num}"
        verse_subdir.mkdir(parents=True, exist_ok=True)

        # Generate verse files
        for verse_num in range(1, total_verses + 1):
            verse_content = generate_verse_file(
                surah_num,
                verse_num,
                total_verses,
                transliterated_name,
                translations_data,
                arabic_data,
            )
            verse_filename = f"Quran {surah_num}-{verse_num}.md"
            verse_path = verse_subdir / verse_filename
            verse_path.write_text(verse_content, encoding="utf-8")

        print(f"Generated Surah {surah_num}: {transliterated_name} ({total_verses} verses)")
