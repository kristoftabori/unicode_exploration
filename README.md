# Unicode Exploration

A Python library for manipulating and exploring Unicode tag characters (U+E0000 to U+E007F).

## Overview

This library provides utilities for working with the Unicode tag block, allowing you to:

- Convert text to invisible Unicode tag characters
- Obfuscate specific parts of text using tag characters
- Deobfuscate text that contains tag characters
- Filter or strip tag characters from text

The tag characters in the Unicode block U+E0000 to U+E007F are special "invisible" characters that can be used for various purposes, including text annotation and obfuscation.

## Installation

### Using uv (recommended)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install in development mode:

```bash
# Run the install script
./install_dev.sh

# Or manually:
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -e ".[dev]"
```

## Usage Examples

### Converting Text to Unicode Tags

```python
from unicode_exploration import convert_str_to_tags

# Convert a string to invisible Unicode tag characters
tagged_text = convert_str_to_tags("hello")
print(f"Original: hello")
print(f"Tagged: {tagged_text}")  # Will appear as empty or invisible characters
```

### Obfuscating Specific Text

```python
from unicode_exploration import obfuscate_text

# Obfuscate specific words in a text
text = "This is a secret message"
obfuscated = obfuscate_text(text, "secret")
print(obfuscated)  # "This is a [invisible]secret[/invisible] message"
```

### Deobfuscating Tagged Text

```python
from unicode_exploration import deobfuscate_tags

# Deobfuscate text that contains invisible tag characters
original = deobfuscate_tags(obfuscated)
print(original)  # "This is a secret message"
```

### Stripping Tag Characters

```python
from unicode_exploration import strip_all_unicode_tags

# Remove all tag characters from a string
visible_only = strip_all_unicode_tags(obfuscated)
print(visible_only)  # "This is a  message" (note the extra space where "secret" was)
```

## API Reference

### `convert_str_to_tags(input_str: str, offset: int = 0xE0000) -> str`

Converts a string to Unicode tag characters by shifting each character by the given offset.

### `obfuscate_text(input_str: str, *strs_to_obfuscate: str, offset: int = 0xE0000) -> str`

Obfuscates specific parts of text by converting them to tag characters.

### `deobfuscate_char(char: str, offset: int = 0xE0000) -> str`

Deobfuscates a single Unicode character by reversing the offset.

### `deobfuscate_tags(input_str: str, offset: int = 0xE0000) -> str`

Deobfuscates a string containing Unicode tags back to its original form.

### `filter_unicode_tags(input_str: str, min_range: int = 0xE0000, max_range: int = 0xE007F) -> str`

Filters out characters from a specified Unicode range.

### `strip_all_unicode_tags(input_str: str, offsets: list[int] | None = None) -> str`

Removes characters from all specified Unicode tag blocks.

## Testing

Run the tests using:

```bash
# Using the make command
make test

# Using pytest directly
pytest
```

For test coverage:

```bash
make coverage
```

## Code Quality

Lint and format the code:

```bash
# Run linters
make lint

# Format code
make format
```

## License

[MIT License](LICENSE)
