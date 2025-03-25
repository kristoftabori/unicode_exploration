def convert_str_to_tags(input_str: str, offset: int = 0xE0000) -> str:
    """Convert a string to Unicode tags by shifting characters by the given offset.

    Args:
        input_str (str): The input string to convert.
        offset (int, optional): Unicode offset to apply. Defaults to 0xE0000.

    Returns:
        str: The converted string with each character shifted by the offset.

    Example:
        >>> convert_str_to_tags("hello", 0xE0000)
        '󠀨󠀥󠀬󠀬󠀯'
    """
    return "".join(chr(offset + ord(c)) for c in input_str)


def obfuscate_text(input_str: str, *strs_to_obfuscate: str, offset: int = 0xE0000) -> str:
    """Obfuscate specific strings within a larger text by converting them to Unicode tags.

    Args:
        input_str (str): The main text containing strings to obfuscate.
        *strs_to_obfuscate: Variable number of strings to obfuscate within the input text.
        offset (int, optional): Unicode offset to apply. Defaults to 0xE0000.

    Returns:
        str: Text with specified strings obfuscated using Unicode tags.

    Example:
        >>> obfuscate_text("hello world", "hello", offset=0xE0000)
        '󠀨󠀥󠀬󠀬󠀯 world'
    """
    final_str = input_str
    for target_string in strs_to_obfuscate:
        final_str = final_str.replace(target_string, convert_str_to_tags(target_string, offset))
    return final_str


def deobfuscate_char(char: str, offset: int = 0xE0000) -> str:
    """Deobfuscate a single Unicode character by reversing the offset.

    Args:
        char (str): Single character to deobfuscate.
        offset (int, optional): Unicode offset to reverse. Defaults to 0xE0000.

    Returns:
        str: Original character if it was obfuscated, otherwise returns the input character unchanged.

    Example:
        >>> deobfuscate_char('󠀨', 0xE0000)
        'h'
    """
    if offset <= ord(char) <= 0xE007F:
        return chr(ord(char) - offset)
    return char


def deobfuscate_tags(input_str: str, offset: int = 0xE0000) -> str:
    """Deobfuscate a string containing Unicode tags back to its original form.

    Args:
        input_str (str): The string containing obfuscated Unicode tags.
        offset (int, optional): Unicode offset to reverse. Defaults to 0xE0000.

    Returns:
        str: Original string with all obfuscated characters restored.

    Example:
        >>> deobfuscate_tags('󠀨󠀥󠀬󠀬󠀯')
        'hello'
    """
    return ''.join([deobfuscate_char(char, offset) for char in input_str])


def filter_unicode_tags(input_str: str, min_range: int = 0xE0000, max_range: int = 0xE007F) -> str:
    """Filter out characters from the Unicode tag block or any specified range.

    This function removes characters within the specified Unicode range, which by default
    corresponds to the Unicode tag block (U+E0000 to U+E007F).

    Args:
        input_str (str): The input string that may contain Unicode tag characters.
        min_range (int, optional): The minimum Unicode code point to filter. Defaults to 0xE0000.
        max_range (int, optional): The maximum Unicode code point to filter. Defaults to 0xE007F.

    Returns:
        str: String with all characters in the specified range removed.

    Example:
        >>> original = "hello"
        >>> tagged = convert_str_to_tags(original)
        >>> mixed = tagged + " world"
        >>> print(mixed)  # Contains invisible tag characters
        >>> print(filter_unicode_tags(mixed))
        " world"
    """
    return ''.join([c for c in input_str if not (min_range <= ord(c) <= max_range)])


def strip_all_unicode_tags(input_str: str, offsets: list[int] | None = None) -> str:
    """Remove characters from all Unicode tag blocks specified in the offsets list.

    This is a more comprehensive version that can handle multiple tag blocks.

    Args:
        input_str (str): The input string that may contain Unicode tag characters.
        offsets (list[int] | None, optional): List of Unicode tag block starting offsets to filter.
                                     If None, filters the default tag block (E0000).

    Returns:
        str: String with all tag characters removed.

    Example:
        >>> tagged_str = obfuscate_text("This is hidden", "hidden")
        >>> print(strip_all_unicode_tags(tagged_str))
        "This is "
    """
    if offsets is None:
        offsets = [0xE0000]

    result = input_str
    for offset in offsets:
        result = filter_unicode_tags(result, offset, offset + 0x7F)

    return result
