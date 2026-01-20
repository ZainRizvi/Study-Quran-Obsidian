"""Command-line interface for quran-obsidian."""

import argparse
import sys
from pathlib import Path

from .data import get_available_translations
from .generator import generate_quran_files


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate Quran markdown files."""
    output_dir = Path(args.output)
    translations = [t.strip() for t in args.translations.split(",")]

    # Validate translations
    available = set(get_available_translations())
    invalid = [t for t in translations if t not in available]
    if invalid:
        print(f"Error: Unknown translation(s): {', '.join(invalid)}", file=sys.stderr)
        print(f"Use 'quran-obsidian list' to see available translations.", file=sys.stderr)
        return 1

    print(f"Generating Quran files to {output_dir}")
    print(f"Translations: {', '.join(translations)}")
    print()

    generate_quran_files(output_dir, translations)

    print()
    print(f"Done! Files written to {output_dir}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List available translations."""
    translations = get_available_translations()
    print("Available translations:")
    print()
    for t in translations:
        print(f"  {t}")
    print()
    print(f"Total: {len(translations)} translations")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="quran-obsidian",
        description="Generate Obsidian-compatible markdown files for Quran verses and surahs with multiple translations.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate Quran markdown files",
        description="Generate Obsidian markdown files for all surahs and verses with specified translations.",
    )
    gen_parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output directory for generated files",
    )
    gen_parser.add_argument(
        "--translations",
        "-t",
        required=True,
        help="Comma-separated list of translations to include (use 'list' command to see available options)",
    )
    gen_parser.set_defaults(func=cmd_generate)

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available translations",
        description="List all available translations from the quran_db database.",
    )
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
