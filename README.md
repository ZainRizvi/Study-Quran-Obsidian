# Quran Obsidian

Generate Obsidian-compatible markdown files for Quran verses and surahs with multiple translations.

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ZainRizvi/quran-obsidian.git
cd quran-obsidian
```

## Usage

### List available translations

```bash
uv run python -m quran_obsidian.cli list
```

This will clone the quran_db repository on first run and list all available translations (70+).

### Generate Quran files

```bash
uv run python -m quran_obsidian.cli generate --output out/quran --translations thestudyquran,arabic,aliquliqarai
```

This generates:
- `Surahs/` - One markdown file per surah with metadata and verse links
- `Verses/Surah N/` - One markdown file per verse with all requested translations

### Example with multiple translations

```bash
uv run python -m quran_obsidian.cli generate \
  --output my-quran-vault \
  --translations thestudyquran,arabic,muhammadahmedsamira,aliquliqarai
```

## Output Format

### Surah files

Each surah file includes:
- YAML frontmatter with surah number, Arabic name, English translation, verse count, and type (Meccan/Medinan)
- Obsidian aliases for easy linking
- Dataview reference section
- Links to all verses

### Verse files

Each verse file includes:
- YAML frontmatter with surah number, verse number, and aliases
- Link to parent surah
- Previous/next verse navigation links
- All requested translations with proper attribution
- Arabic text displayed in large format
- Dataview reference section for notes

## Data Sources

This project uses data from the following repositories:

- **[faisalill/quran_db](https://github.com/faisalill/quran_db)** - Quran Translation Database containing 70+ translations in JSON format. This is the primary data source for all Quranic text and translations.

- **[sarfraznawaz2005/quran-json](https://github.com/sarfraznawaz2005/quran-json)** - Source of surah metadata including Meccan/Medinan classification.

Thank you to the maintainers of these repositories for making Quranic data freely available.

## License

MIT
