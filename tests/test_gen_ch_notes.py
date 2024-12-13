import pytest
from unittest.mock import Mock, patch, mock_open
import os
import csv
import genanki
from PIL import Image
import io


# Import your modules
from gen_ch_anki.gen_ch_notes import char_to_write, convert_and_rename, at_least_two_chinese_sentences, text_to_mp3, add_row_zero_as_newline, gen_ch_notes

@pytest.fixture
def mock_csv_file():
    csv_content = "你,nǐ\n好,hǎo\n"
    return mock_open(read_data=csv_content)


@pytest.fixture
def mock_media():
    return []


@pytest.fixture
def mock_deck():
    return Mock(spec=genanki.Deck)


class TestCharToWrite:
    @pytest.fixture
    def mock_known_chars(self):
        return "你好世界"

    @patch('builtins.open', create=True)
    def test_basic_word_processing(self, mock_file, mock_known_chars):
        mock_file.return_value.__enter__.return_value = [mock_known_chars]

        result = char_to_write("你好")
        assert len(result) == 4  # Should return 4 elements minimum
        assert all(isinstance(x, str) for x in result)

    @patch('builtins.open', create=True)
    def test_unknown_characters(self, mock_file, mock_known_chars):
        mock_file.return_value.__enter__.return_value = [mock_known_chars]

        result = char_to_write("测试")
        assert "__试" in result[0] or "测__" in result[0]
        assert len(result) == 4

    @patch('builtins.open', create=True)
    def test_empty_input(self, mock_file, mock_known_chars):
        mock_file.return_value.__enter__.return_value = [mock_known_chars]

        result = char_to_write("")
        assert len(result) == 4
        assert all(x == '' for x in result)


class TestConvertAndRename:
    @pytest.fixture
    def mock_image(self):
        # Create a small test image
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    @patch('PIL.Image.open')
    @patch('os.walk')
    def test_image_conversion(self, mock_walk, mock_pil_open, mock_image, mock_media):
        # Setup mock walk
        mock_walk.return_value = [
            ("/test/path", [], ["image1.png", "image2.jpg"])
        ]

        # Setup mock PIL
        mock_img = Mock()
        mock_img.convert.return_value = mock_img
        mock_img.save = Mock()
        mock_pil_open.return_value.__enter__.return_value = mock_img

        convert_and_rename("test_dir", mock_media)

        assert len(mock_media) == 2
        assert mock_img.save.called
        assert mock_img.convert.called


class TestAtLeastTwoChineseSentences:
    @pytest.mark.parametrize("input_str,expected", [
        ("你好，世界, Hello world", True),
        ("你好, 世界", True),
        ("Hello, World", False),
        ("你好, Hello", False),
        ("", False),
    ])
    def test_various_inputs(self, input_str, expected):
        assert at_least_two_chinese_sentences(input_str) == expected


class TestTextToMp3:
    @patch('gtts.gTTS')
    def test_basic_conversion(self, mock_gtts):
        mock_tts_instance = Mock()
        mock_gtts.return_value = mock_tts_instance

        result = text_to_mp3("你好")

        assert result == "你好.mp3"
        mock_gtts.assert_called_once_with(text="你好", lang="zh", slow=False)
        mock_tts_instance.save.assert_called_once_with("你好.mp3")


class TestAddRowZeroAsNewline:
    def test_add_string(self, tmp_path):
        file_path = tmp_path / "test.csv"
        word = "测试"

        add_row_zero_as_newline(word, file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            assert content == "测试"

    def test_add_non_string(self, tmp_path):
        file_path = tmp_path / "test.csv"
        word = 123

        add_row_zero_as_newline(word, file_path)

        assert not os.path.exists(file_path) or os.path.getsize(file_path) == 0


class TestGenChNotes:
    @pytest.fixture
    def mock_dependencies(self):
        patches = {
            'downloader.download': patch('bing_image_downloader.downloader.download'),
            'text_to_mp3': patch('your_module.text_to_mp3'),
            'convert_and_rename': patch('your_module.convert_and_rename'),
            'best_sentences': patch('gen_ch_anki.assigner.best_sentences'),
            'add_row_zero_as_newline': patch('your_module.add_row_zero_as_newline'),
        }

        mocks = {}
        for name, patcher in patches.items():
            mocks[name] = patcher.start()

        yield mocks

        for patcher in patches.values():
            patcher.stop()

    def test_basic_note_generation(self, mock_dependencies, mock_deck, mock_media):
        mock_dependencies['best_sentences'].return_value = [
            ("这是第一句。", "Zhè shì dì yī jù.", "This is the first sentence."),
            ("这是第二句。", "Zhè shì dì èr jù.", "This is the second sentence.")
        ]

        gen_ch_notes(
            "测试", "cèshì", "test",
            mock_deck, mock_media
        )

        assert mock_deck.add_note.call_count == 3  # Main note + 2 cloze notes
        assert len(mock_media) > 0

    def test_sentence_error(self, mock_dependencies, mock_deck, mock_media):
        mock_dependencies['best_sentences'].return_value = [("单句", "dān jù", "Single sentence")]

        with pytest.raises(SentenceError):
            gen_ch_notes(
                "测试", "cèshì", "test",
                mock_deck, mock_media
            )


if __name__ == '__main__':
    pytest.main(['-v'])