"""Tests for the unicode_block_masking module."""
import pytest
from unicode_exploration import (
    convert_str_to_tags,
    obfuscate_text,
    deobfuscate_char,
    deobfuscate_tags,
    filter_unicode_tags,
    strip_all_unicode_tags
)


class TestStripUnicodeTags:
    """Tests for the strip_unicode_tags function."""

    def test_default_strip(self):
        """Test stripping Unicode tags with default parameters."""
        original = "This is hidden"
        tagged = obfuscate_text(original, "hidden")

        result = strip_all_unicode_tags(tagged)

        assert result == "This is "

    def test_multiple_offsets(self):
        """Test stripping Unicode tags at multiple offsets."""
        text1 = convert_str_to_tags("hello", offset=0xE0000)
        text2 = convert_str_to_tags("world", offset=0xE0001)
        combined = f"{text1} {text2} record"

        result = strip_all_unicode_tags(combined, [0xE0000, 0xE0001])

        assert result == "  record"

    def test_no_tags_present(self):
        """Test when no tags are present."""
        test_str = "hello world"
        result = strip_all_unicode_tags(test_str)
        assert result == test_str

    def test_empty_string(self):
        """Test with empty string."""
        result = strip_all_unicode_tags("")
        assert result == ""


class TestConvertStrToTags:
    """Tests for the convert_str_to_tags function."""

    def test_default_offset(self):
        """Test with default offset."""
        result = convert_str_to_tags("hello")
        expected = ""

        assert strip_all_unicode_tags(result) == expected

    def test_custom_offset(self):
        """Test with custom offset."""
        custom_offset = 0xE0001
        result = convert_str_to_tags("hello", offset=custom_offset)
        expected = ""
        assert strip_all_unicode_tags(result) == expected

    def test_empty_string(self):
        """Test with empty string."""
        result = convert_str_to_tags("")
        assert result == ""

    def test_special_characters(self):
        """Test with special characters."""
        special_str = "!@#$%^&*()"
        result = convert_str_to_tags(special_str)
        expected = ""
        assert strip_all_unicode_tags(result) == expected


class TestObfuscateText:
    """Tests for the obfuscate_text function."""

    def test_single_word_obfuscation(self):
        """Test obfuscating a single word in a string."""
        result = obfuscate_text("hello world", "hello")
        expected = ' world'
        assert strip_all_unicode_tags(result) == expected

    def test_multiple_words_obfuscation(self):
        """Test obfuscating multiple words in a string."""
        result = obfuscate_text("hello beautiful world", "hello", "world")
        expected = ' beautiful '
        assert strip_all_unicode_tags(result) == expected

    def test_custom_offset(self):
        """Test with custom offset."""
        custom_offset = 0xE0001
        result = obfuscate_text("hello world", "hello", offset=custom_offset)
        expected = ' world'
        assert strip_all_unicode_tags(result) == expected

    def test_no_matches(self):
        """Test when no strings to obfuscate are found."""
        result = obfuscate_text("hello world", "goodbye")
        assert result == "hello world"

    def test_empty_string(self):
        """Test with empty input string."""
        result = obfuscate_text("", "hello")
        assert result == ""


class TestDeobfuscateChar:
    """Tests for the deobfuscate_char function."""

    def test_obfuscated_char(self):
        """Test deobfuscating a character that was obfuscated."""
        obfuscated_h = chr(0xE0000 + ord('h'))
        result = deobfuscate_char(obfuscated_h)
        assert result == 'h'

    def test_normal_char(self):
        """Test with a normal non-obfuscated character."""
        result = deobfuscate_char('h')
        assert result == 'h'

    def test_custom_offset(self):
        """Test with custom offset."""
        custom_offset = 0xE0001
        obfuscated_h = chr(custom_offset + ord('h'))
        if custom_offset > 0xE007F:
            pytest.skip("deobfuscate_char function only checks for E0000-E007F range")
        else:
            result = deobfuscate_char(obfuscated_h, offset=custom_offset)
            assert result == 'h'


class TestDeobfuscateTags:
    """Tests for the deobfuscate_tags function."""

    def test_fully_obfuscated_string(self):
        """Test deobfuscating a fully obfuscated string."""
        obfuscated = convert_str_to_tags("hello")
        result = deobfuscate_tags(obfuscated)
        assert result == "hello"

    def test_mixed_string(self):
        """Test with a string containing both obfuscated and normal characters."""
        obfuscated_hello = convert_str_to_tags("hello")
        mixed = obfuscated_hello + " world"
        result = deobfuscate_tags(mixed)
        assert result == "hello world"

    def test_custom_offset(self):
        """Test with custom offset."""
        custom_offset = 0xE0001
        obfuscated = convert_str_to_tags("hello", offset=custom_offset)
        if custom_offset > 0xE007F:
            pytest.skip("deobfuscate_tags uses deobfuscate_char which only checks for E0000-E007F range")
        else:
            result = deobfuscate_tags(obfuscated, offset=custom_offset)
            assert result == "hello"

    def test_empty_string(self):
        """Test with empty string."""
        result = deobfuscate_tags("")
        assert result == ""


class TestFilterUnicodeTags:
    """Tests for the filter_unicode_tags function."""

    def test_filtering_tags(self):
        """Test filtering out Unicode tag characters."""
        original = "hello"
        tagged = convert_str_to_tags(original)
        mixed = tagged + " world"

        result = filter_unicode_tags(mixed)

        assert result == " world"

    def test_custom_range(self):
        """Test filtering with custom range."""
        test_str = "hello123"
        # Filter characters between 'a' and 'z' (ordinals 97-122)
        result = filter_unicode_tags(test_str, 97, 122)

        # Only digits should remain
        assert result == "123"

    def test_no_tags_present(self):
        """Test when no tags are present."""
        test_str = "hello world"
        result = filter_unicode_tags(test_str)
        assert result == test_str

    def test_empty_string(self):
        """Test with empty string."""
        result = filter_unicode_tags("")
        assert result == ""
