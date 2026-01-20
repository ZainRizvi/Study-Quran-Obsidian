# CLAUDE.md

## Project Overview

**quran-obsidian** generates Obsidian-compatible markdown files for the entire Quran with multiple translations. The output is designed for use in Obsidian vaults with features like wiki-links, YAML frontmatter, and Dataview queries.

## Architecture

```
User runs CLI → Downloads quran_db repo (once) → Loads JSON translations → Generates markdown files
```

### Key Files

- `quran_obsidian/cli.py` - Entry point. Commands: `generate`, `list`
- `quran_obsidian/data.py` - Loads translation JSONs from quran_db, manages repo cloning
- `quran_obsidian/generator.py` - Core logic for generating Surah and Verse markdown files
- `quran_obsidian/surah_metadata.json` - Static file with Meccan/Medinan classification (from external source)

### Data Flow

1. On first run, `data.py` clones `faisalill/quran_db` to local `quran_db/` directory (gitignored)
2. Each translation is a JSON file: `{translator}.json` with structure:
   ```json
   {
     "1": {
       "SurahTransliteratedName": "al-Fatihah",
       "SurahArabicName": "الفَاتِحَة",
       "SurahEnglishNames": "The Opening",
       "Ayahs": {
         "1": {"Translator Name": "verse text..."},
         "2": {"Translator Name": "verse text..."}
       }
     }
   }
   ```
3. Generator iterates all 114 surahs, creates one Surah file and N verse files per surah

## Output Structure

```
output/
├── Surahs/
│   ├── 1 - Surah al-Fatihah.md
│   ├── 2 - Surah al-Baqarah.md
│   └── ...
└── Verses/
    ├── Surah 1/
    │   ├── Quran 1-1.md
    │   ├── Quran 1-2.md
    │   └── ...
    ├── Surah 2/
    │   └── ...
    └── ...
```

## Important Implementation Details

### Arabic Text Processing
- Arabic verses in the source contain verse-end markers (۝ followed by Arabic-Indic numerals)
- These are stripped using regex in `strip_arabic_verse_markers()`
- Arabic is displayed with `<big><big><big>` tags for visibility

### Translation Display Names
- JSON filenames are lowercase, no spaces (e.g., `thestudyquran.json`)
- Display names are extracted from inside the JSON (e.g., "The Study Quran")
- The translator name is the key inside each verse's Ayahs dict

### HTML Entities
- Some translations contain HTML entities (`&mdash;`, `&#91;`, etc.)
- These are decoded to actual characters using `html.unescape()`

### Surah Metadata
- Meccan/Medinan classification comes from `surah_metadata.json`
- This file is committed to the repo (not from quran_db)
- Source: https://github.com/sarfraznawaz2005/quran-json/blob/master/surah.json

## Priorities

1. **Output fidelity** - Match the reference output format exactly (see `reference_data/Sample_output/`)
2. **Data accuracy** - Preserve original translation text without modification
3. **Obsidian compatibility** - Ensure wiki-links, frontmatter, and Dataview queries work correctly

## Common Tasks

### Adding a new translation source
1. Translations come from quran_db repo - no action needed unless using a different repo
2. To change the source repo, modify `QURAN_DB_REPO` in `data.py`

### Modifying output format
1. Surah template: `generate_surah_file()` in `generator.py`
2. Verse template: `generate_verse_file()` in `generator.py`
3. Reference the `reference_data/Sample_output/` directory for expected format

### Testing changes
```bash
# Quick test with just Surah 1
uv run python -c "
from quran_obsidian.generator import generate_quran_files
from pathlib import Path
generate_quran_files(Path('test_out'), ['arabic', 'thestudyquran'])
"

# Full generation
uv run python -m quran_obsidian.cli generate -o out/quran -t thestudyquran,arabic,aliquliqarai
```

## Reference Data

The `reference_data/Sample_output/` directory contains example output that the script should match. This is the source of truth for output format.

## External Dependencies

- **quran_db repo** (faisalill/quran_db) - Cloned automatically on first run
- **No Python dependencies** - Uses only standard library (json, pathlib, subprocess, argparse, html, re)

## Gotchas

1. The `quran_db/` directory is gitignored and auto-cloned. Delete it to force a fresh clone.
2. Translation names for CLI are the JSON filenames without `.json` extension
3. "arabic" is treated as a translation but formatted differently (no quotes, big tags)
4. Some translations have special characters in filenames (e.g., `aliãœnal.json`)
