from gen_ch_anki import convert_to_trad, note_templates
import re
import os
import genanki
import csv
from bing_image_downloader import downloader
from gtts import gTTS
from PIL import Image
from gen_ch_anki.assigner import best_sentences
from icrawler.builtin import BingImageCrawler


class SentenceError(Exception):
    """Custom exception for sentence-related errors"""
    pass



# Define the Anki card model structure
class ChineseVocabModel:
    """Class to handle the Anki card model definition"""
    MODEL_ID = 275837465987236587  # Unique model identifier

    @staticmethod
    def get_model():
        """Returns a configured genanki Model for Chinese vocabulary cards"""
        return genanki.Model(
            ChineseVocabModel.MODEL_ID,
            'Vocab Card',
            fields=[
                # Basic word information
                {'name': 'Simplified_Word'},
                {'name': 'Traditional_Word'},
                {'name': 'Pinyin'},
                {'name': 'Recording'},
                {'name': 'Picture'},

                # First example sentence
                {'name': 'Sentence_1'},
                {'name': 'Sentence_1_Pinyin'},
                {'name': 'Sentence_1_translation'},
                {'name': 'Picture_1'},
                {'name': 'Recording_of_sentence_1'},

                # Second example sentence
                {'name': 'Sentence_2'},
                {'name': 'Sentence_2_Pinyin'},
                {'name': 'Sentence_2_translation'},
                {'name': 'Picture_2'},
                {'name': 'Recording_of_sentence_2'},

                # Individual character practice
                {'name': 'S_Char_1'}, {'name': 'S_Char_2'},
                {'name': 'S_Char_3'}, {'name': 'S_Char_4'},
                {'name': 'T_Char_1'}, {'name': 'T_Char_2'},
                {'name': 'T_Char_3'}, {'name': 'T_Char_4'},

                # Additional learning aids
                {'name': 'Definition'},
                {'name': 'Personal_Connection'},
                {'name': 'Simplified_Story'},
                {'name': 'Traditional_Story'},
                {'name': 'Mnemonic_Classifier'}
            ],
            templates=note_templates.note_1_templates
        )


def get_images(text,media_files,output_dir):
    crawler = BingImageCrawler(storage={
        'root_dir': f"{output_dir}/{text}"
    })
    crawler.crawl(keyword=text, max_num=5)

    process_images(text, media_files, output_dir)

def get_characters_to_write(word, known_chars_path, min_length=4):
    """
    Determines which characters from a word need to be practiced based on known characters.

    Args:
        word (str): The Chinese word to analyze
        known_chars_path (str): Path to TSV file containing known characters
        min_length (int): Minimum number of character slots to return

    Returns:
        list: Characters to practice, with empty strings for known characters
    """
    # Load known characters from file
    with open(known_chars_path, 'r', encoding='utf-8') as file:
        known_characters = {char for row in csv.reader(file) for char in row[0]}

    # Generate practice list
    result = ['' if char in known_characters else word.replace(char, '__') for char in word]

    # Pad to minimum length
    return result + [''] * (min_length - len(result))


def process_images(dir_name, media_list, output_dir, target_size=(300, 300)):
    """
    Processes downloaded images: converts to JPG, resizes, and adds to media list.

    Args:
        dir_name (str): Directory containing the images
        media_list (list): List to append processed image paths
        output_dir (str): Base output directory for images
        target_size (tuple): Target dimensions for resized images
    """
    for root, _, files in os.walk(os.path.join(output_dir, dir_name)):
        for filename in files:
            try:
                # Generate paths
                original_path = os.path.join(root, filename)
                # Edit string from image crawl to text_Image_Num
                new_filename = f"{os.path.basename(root)}_Image_{filename}"
                new_filename = new_filename.replace("0","")
                #
                new_path = os.path.join(root, new_filename)
                new_path = os.path.splitext(new_path)[0] + '.jpg'

                # Process image
                with Image.open(original_path) as img:
                    rgb_im = img.convert('RGB')
                    resized_img = rgb_im.resize(target_size)
                    resized_img.save(new_path, 'JPEG')

                media_list.append(os.path.abspath(new_path))
            except Exception as e:
                print(f"Error processing image {original_path}: {e}")


def create_audio(text, language='zh'):
    """
    Creates MP3 audio file for Chinese text using gTTS.

    Args:
        text (str): Text to convert to speech
        language (str): Language code (default: 'zh' for Chinese)

    Returns:
        str: Path to generated audio file
    """
    output_file = f"{text}.mp3"
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    return output_file


def update_known_characters(word, file_paths):
    """
    Updates the list of known characters in both CSV and TSV files.

    Args:
        word (str): Word containing characters to mark as known
        file_paths (dict): Paths to CSV and TSV files
    """
    for path in file_paths.values():
        delimiter = ',' if path.endswith('.csv') else '\t'
        with open(path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow([word])


def create_vocabulary_note(word, pinyin, definition, sentences, simp_chars, trad_chars, deck):
    """
    Creates and adds the main vocabulary note to the deck.

    Args:
        word (str): Chinese vocabulary word
        pinyin (str): Pinyin pronunciation
        definition (str): English definition
        sentences (list): List of tuples containing (sentence, pinyin, translation)
        simp_chars (list): Characters to practice in simplified form
        trad_chars (list): Characters to practice in traditional form
        deck (genanki.Deck): Anki deck to add the note to
    """
    vocab_note = genanki.Note(
        model=ChineseVocabModel.get_model(),
        fields=[
            # Basic word information
            word,
            convert_to_trad.convert_to_trad(word),
            pinyin,
            f'[sound:{word}.mp3]',
            f'<img src="{word}_Image_1.jpg" /> <img src="{word}_Image_2.jpg" /> <img src="{word}_Image_3.jpg" />',

            # First example sentence
            convert_to_trad.convert_simplified_to_traditional(sentences[0][0]),
            sentences[0][1],  # pinyin
            sentences[0][2],  # translation
            f'<img src="{sentences[0][0]}_Image_1.jpg" /> <img src="{sentences[0][0]}_Image_2.jpg" /> <img src="{sentences[0][0]}_Image_3.jpg" />',
            f'[sound:{sentences[0][0]}.mp3]',

            # Second example sentence
            convert_to_trad.convert_simplified_to_traditional(sentences[1][0]),
            sentences[1][1],  # pinyin
            sentences[1][2],  # translation
            f'<img src="{sentences[1][0]}_Image_1.jpg" /> <img src="{sentences[1][0]}_Image_2.jpg" /> <img src="{sentences[1][0]}_Image_3.jpg" />',
            f'[sound:{sentences[1][0]}.mp3]',

            # Character practice fields
            *simp_chars,  # Unpack simplified characters
            *trad_chars,  # Unpack traditional characters

            # Additional fields
            definition,
            '',  # Personal Connection
            '',  # Simplified Story
            '',  # Traditional Story
            ''  # Mnemonic Classifier
        ]
    )
    deck.add_note(vocab_note)


def create_cloze_notes(word, sentences, deck):
    """
    Creates and adds cloze deletion notes for example sentences.

    Args:
        word (str): Chinese vocabulary word to create cloze deletions for
        sentences (list): List of tuples containing (sentence, pinyin, translation)
        deck (genanki.Deck): Anki deck to add the notes to
    """
    for i, sentence in enumerate(sentences, 1):
        cloze_note = genanki.Note(
            model=genanki.CLOZE_MODEL,
            fields=[
                # First field: Sentence with cloze deletion
                convert_to_trad.convert_simplified_to_traditional(
                    re.sub(word, f"{{{{c1::{word}}}}}", sentence[0])
                ),
                # Second field: Additional information
                (
                    f"{word}/{convert_to_trad.convert_to_trad(word)}<br>" 
                    f"{convert_to_trad.convert_simplified_to_traditional(sentence[0])}<br>"
                    f"{sentence[1]}<br>"
                    f"{sentence[2]}<br>" 
                    f"[sound:{sentence[0]}.mp3]<br>" 
                    f"<img src='{sentence[0]}_Image_1.jpg' /> "
                    f"<img src='{sentence[0]}_Image_2.jpg' /> "
                    f"<img src='{sentence[0]}_Image_3.jpg' />"
                )
        ]
        )
        deck.add_note(cloze_note)

def generate_chinese_notes(word, pinyin, definition, deck, media_files, config):
    """
    Generates Anki notes for a Chinese vocabulary word with example sentences.

    Args:
        word (str): Chinese vocabulary word
        pinyin (str): Pinyin pronunciation
        definition (str): English definition
        deck (genanki.Deck): Anki deck to add notes to
        media_files (list): List to track media files
        config (dict): Configuration settings
    """
    # Get example sentences
    sentences = best_sentences(word, limit=2,sentances_path=config['sentances_path_path'])

    if len(sentences) != 2:
        raise SentenceError(f"Unable to find enough example sentences for {word}")

    # Generate audio files
    media_files.append(os.path.abspath(create_audio(word)))
    for sentence in sentences:
        media_files.append(os.path.abspath(create_audio(sentence[0])))

    # Download and process images
    for text in [word] + [s[0] for s in sentences]:
        get_images(text, media_files, config['img_output_dir'])

    # Create character practice fields
    simp_chars = get_characters_to_write(word, config['known_chars_path'])
    trad_chars = get_characters_to_write(convert_to_trad.convert_to_trad(word), config['known_chars_path'])

    # Create and add notes to deck
    create_vocabulary_note(word, pinyin, definition, sentences, simp_chars, trad_chars, deck)
    create_cloze_notes(word, sentences, deck)

    # Update known characters
    traditional_word = convert_to_trad.convert_to_trad(word)
    for w in [word, traditional_word]:
        update_known_characters(w, {
            'csv': config['known_csv_path'],
            'tsv': config['known_tsv_path']
        })