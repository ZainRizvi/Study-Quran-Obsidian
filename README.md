# Study Quran Obsidian

Build your personal Quran study system in Obsidian.

If you use Obsidian for learning and note-taking, this tool lets you bring the Quran into your vault—with the Arabic text, multiple translations side by side, and the ability to link your own notes and reflections to any verse.

Write a note about something you learned? Link it to the verse. Studying a particular surah? See all your related notes in one place. Compare how different scholars translated a phrase. Build connections across your knowledge base with the Quran at the center.

## What You Get

- **Every verse as its own file** - Link to `[[Quran 2-255]]` from anywhere in your vault
- **Multiple translations** - Choose from 70+ translations to display side by side
- **Arabic text** - Displayed prominently at the top of each verse
- **Backlinks** - See all your notes that reference each verse or surah
- **Navigation** - Previous/next verse links, surah links, and Obsidian aliases for flexible linking

## Quick Start

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
# Clone this repo
git clone https://github.com/ZainRizvi/Study-Quran-Obsidian.git
cd Study-Quran-Obsidian

# See available translations
uv run python -m quran_obsidian.cli list

# Generate the Quran files into your Obsidian vault
uv run python -m quran_obsidian.cli generate \
  --output /path/to/your/vault/Quran \
  --translations arabic,thestudyquran,aliquliqarai
```

The first run will download the translation database automatically.

## Setting Up Obsidian

After generating the files:

1. **Install the Dataview plugin** (required for the references feature):
   - Obsidian Settings → Community plugins → Browse
   - Search for "Dataview" and install it
   - Enable the plugin

2. That's it. Open your vault and start exploring.

You can now:
- Link to any verse: `[[Quran 2-255]]` or `[[Quran 1-1]]`
- Link to surahs: `[[Surah al-Baqarah]]` or `[[1 - Surah al-Fatihah]]`
- See which of your notes reference each verse (via backlinks and Dataview)
- Navigate between verses with prev/next links

## Choosing Translations

Run `uv run python -m quran_obsidian.cli list` to see all 70+ available translations.

Some popular choices:
- `arabic` - The Arabic text
- `thestudyquran` - The Study Quran (comprehensive commentary tradition)
- `aliquliqarai` - Ali Quli Qara'i (Shia perspective)
- `muhammadahmedsamira` - Muhammad Ahmed/Samira (literal translation)
- `abdelhaleem` - Abdel Haleem (modern, readable English)
- `mustafakhattab2018` - The Clear Quran

Example with multiple translations:
```bash
uv run python -m quran_obsidian.cli generate \
  --output my-vault/Quran \
  --translations arabic,thestudyquran,abdelhaleem,aliquliqarai
```

## Data Sources

This project uses data from:

- **[faisalill/quran_db](https://github.com/faisalill/quran_db)** - Quran Translation Database with 70+ translations
- **[sarfraznawaz2005/quran-json](https://github.com/sarfraznawaz2005/quran-json)** - Surah metadata (Meccan/Medinan classification)

Thank you to the maintainers for making this data freely available.

## License

MIT
