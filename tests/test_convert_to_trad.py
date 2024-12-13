import pytest
from unittest.mock import Mock, patch


# Import your functions here
from gen_ch_anki.convert_to_trad import convert_simplified_to_traditional, convert_to_trad

@pytest.fixture
def mock_opencc():
    with patch('opencc.OpenCC') as mock:
        # Create a mock converter instance
        mock_converter = Mock()
        mock.return_value = mock_converter
        yield mock_converter


def test_convert_simplified_to_traditional_basic(mock_opencc):
    # Test basic conversion
    simplified = "双儿"
    expected = "雙兒"
    mock_opencc.convert.return_value = expected

    result = convert_simplified_to_traditional(simplified)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(simplified)


def test_convert_simplified_to_traditional_long_text(mock_opencc):
    # Test longer text conversion
    simplified = "我们在中国的新年吃饺子"
    expected = "我們在中國的新年吃餃子"
    mock_opencc.convert.return_value = expected

    result = convert_simplified_to_traditional(simplified)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(simplified)


def test_convert_simplified_to_traditional_mixed(mock_opencc):
    # Test text with mixed characters and numbers
    simplified = "2024年春节快乐"
    expected = "2024年春節快樂"
    mock_opencc.convert.return_value = expected

    result = convert_simplified_to_traditional(simplified)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(simplified)


def test_convert_to_trad_with_conversion(mock_opencc):
    # Test when conversion produces different text
    simplified = "专业"
    expected = "專業"
    mock_opencc.convert.return_value = expected

    result = convert_to_trad(simplified)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(simplified)


def test_convert_to_trad_no_conversion(mock_opencc):
    # Test when input and output are the same
    text = "Hello World"  # Non-Chinese text
    mock_opencc.convert.return_value = text

    result = convert_to_trad(text)
    assert result == ""
    mock_opencc.convert.assert_called_once_with(text)


def test_convert_to_trad_empty_string(mock_opencc):
    # Test empty string input
    mock_opencc.convert.return_value = ""

    result = convert_to_trad("")
    assert result == ""
    mock_opencc.convert.assert_called_once_with("")


def test_real_opencc_conversion():
    # Real integration test without mocks
    simplified = "双儿"
    result = convert_simplified_to_traditional(simplified)
    assert result != ""
    assert result != simplified  # Should be different from input
    assert "雙" in result  # Should contain specific traditional character


def test_convert_simplified_to_traditional_special_chars(mock_opencc):
    # Test text with special characters
    simplified = "软件123!@#$%"
    expected = "軟件123!@#$%"
    mock_opencc.convert.return_value = expected

    result = convert_simplified_to_traditional(simplified)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(simplified)


@pytest.mark.parametrize("input_text,expected", [
    ("专业", "專業"),
    ("图书馆", "圖書館"),
    ("软件", "軟件"),
    ("计算机", "計算機"),
])
def test_convert_simplified_to_traditional_parametrized(mock_opencc, input_text, expected):
    # Parametrized test for multiple conversions
    mock_opencc.convert.return_value = expected

    result = convert_simplified_to_traditional(input_text)
    assert result == expected
    mock_opencc.convert.assert_called_once_with(input_text)