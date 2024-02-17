import convert_to_trad
import get_sentence
import re
import os
import genanki
import csv
import note_templates

from bing_image_downloader import downloader
from gtts import gTTS
from PIL import Image

class SentenceError(Exception):
    pass

# Main vocab card
model_main_card = genanki.Model(
    275837465987236587,  # Unique ID for the model, change this to a different number
    'Vocab Card',
    fields=[
        {'name': 'Simplified_Word'},
        {'name': 'Traditional_Word'},
        {'name': 'Pinyin'},
        {'name': 'Recording'},
        {'name': 'Picture'},
        {'name': 'Sentence_1'},
        {'name': 'Sentence_1_Pinyin'},
        {'name': 'Sentence_1_translation'},
        {'name': 'Picture_1'},
        {'name': 'Recording_of_sentence_1'},
        {'name': 'Sentence_2'},
        {'name': 'Sentence_2_Pinyin'},
        {'name': 'Sentence_2_translation'},
        {'name': 'Picture_2'},
        {'name': 'Recording_of_sentence_2'},
        {'name': 'S_Char_1'},
        {'name': 'S_Char_2'},
        {'name': 'S_Char_3'},
        {'name': 'S_Char_4'},
        {'name': 'T_Char_1'},
        {'name': 'T_Char_2'},
        {'name': 'T_Char_3'},
        {'name': 'T_Char_4'},
        {'name': 'Definition'},
        {'name': 'Personal_Connection'},
        {'name': 'Simplified_Story'},
        {'name': 'Traditional_Story'},
        {'name': 'Mnemonic_Classifier'}
    ],
    templates=note_templates.note_1_templates   
)

def char_to_write(word, 
               path_to_known = "C:\\Users\\jakel\\Desktop\\Code\\ch_add_cards\\Data\\known.tsv", 
               min_result_length = 4):
    known_characters = set()

    with open(path_to_known, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for char in row[0]:
                known_characters.add(char)

    result = []

    for char in word:
        if char in known_characters:
            result.append('')
        else:
            result.append(word.replace(char,'__'))

    while len(result) < min_result_length:
        result.append('')

    return result

def convert_and_rename(dir_name, media, img_output_dir = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Images', size=(300, 300)):
    for root, dirs, files in os.walk(os.path.join(img_output_dir, dir_name)):
        for filename in files:
            original_path = os.path.join(root, filename)
            new_filename = f"{os.path.basename(root)}_{filename}"
            new_path = os.path.join(root, new_filename)
            new_path = re.sub(r'\..*$', '.jpg', new_path)

            try:
                # Open the image file
                with Image.open(original_path) as img:
                    # Convert and save the image as JPG with the .jpg file extension
                    rgb_im = img.convert('RGB')
                    rgb_im.save(new_path, 'JPEG')
                    
                    # Resize the image to medium size and save with the same path
                    resized_img = img.resize(size)
                    resized_img.save(new_path, 'JPEG')

                print(f"Conversion successful: {original_path} -> {new_path}")
            except Exception as e:
                print(f"Error converting {original_path} to JPG: {e}")

            #os.rename(original_path, new_path)
            media.append(rf"{new_path}")

def at_least_two_chinese_sentences(input_string):
    # Split the input string into sentences based on the comma separator
    split_str = input_string.split(', ')

    # Count the number of Chinese sentences
    count_chinese_sentences = sum(1 for sentence in split_str if re.search(r'[\u4e00-\u9fff]', sentence))

    # Return true if there are two or more Chinese sentences
    return count_chinese_sentences >= 2

def text_to_mp3(text, language='zh'):
    """
    Convert text to MP3 using gTTS.

    :param text: Text to be converted to speech
    :param language: Language code (default is 'zh' for Chinese)
    :param output_file: Output file name (default is 'output.mp3')
    """
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(f"{text}.mp3")

    return f"{text}.mp3"

# Function to add row[0] as a newline
def add_row_zero_as_newline(word, file_path, delimiter=','):
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=delimiter)
        if isinstance(word, str):
            writer.writerow([word])
        else:
            print("Error: The provided word is not a string.")

def gen_ch_notes(word,
                 word_pinyin,
                 word_def, 
                 my_deck, 
                 media, 
                 new_cwd = 'chinese-sentence-miner-master',
                 img_output_dir = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Images',
                 csv_file_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Data\known.csv',
                 tsv_file_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Data\known.tsv',
                 mined_sentences_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\chinese-sentence-miner-master\output.txt'):
    # Set the number of images to download
    num_images_to_download = 3

    sentences = get_sentence.get_sentence(word,new_cwd,mined_sentences_path)

    if not at_least_two_chinese_sentences(sentences):
        raise SentenceError(f"You need to add sentences for {word}\nEnd: {word}")

    print(f"Start: {word}\n{sentences}")

    # sound for word
    media.append(os.path.abspath(text_to_mp3(word)))

    # Images for word
    downloader.download(
        word, 
        limit=num_images_to_download, 
        output_dir=img_output_dir,
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60
    )

    #Images for sentence 1
    downloader.download(
        sentences.split("\n")[0].split(",")[0], 
        limit=num_images_to_download, 
        output_dir=img_output_dir,
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60
    )

    #Images for sentence 2
    downloader.download(
        sentences.split("\n")[1].split(",")[0], 
        limit=num_images_to_download, 
        output_dir=img_output_dir,
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60
    )

    convert_and_rename(word, media)
    convert_and_rename(sentences.split("\n")[0].split(",")[0], media)
    convert_and_rename(sentences.split("\n")[1].split(",")[0], media)

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[0].split(",")[0])))

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[1].split(",")[0])))

    simp_list = char_to_write(word)
    trad_list = char_to_write(convert_to_trad.convert_to_trad(word))

    c1_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[
            convert_to_trad.convert_simplified_to_traditional(re.sub(word,f"{{{{c1::{word}}}}}",sentences.split("\n")[0].split(",")[0])), 
            f"{word}/{convert_to_trad.convert_to_trad(word)}<br>{convert_to_trad.convert_simplified_to_traditional(sentences.split('\n')[0].split(',')[0])}<br>{sentences.split('\n')[0].split(',')[1]}<br>{sentences.split('\n')[0].split(',')[2]}<br>[sound:{sentences.split('\n')[0].split(',')[0]}.mp3]<br><img src='{sentences.split('\n')[0].split(',')[0]}_Image_1.jpg' /> <img src='{sentences.split('\n')[0].split(',')[0]}_Image_2.jpg' /> <img src='{sentences.split('\n')[0].split(',')[0]}_Image_3.jpg' />"
            ]
    )

    c2_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[
            convert_to_trad.convert_simplified_to_traditional(re.sub(word,f"{{{{c1::{word}}}}}",sentences.split("\n")[1].split(",")[0])), 
            f"{word}/{convert_to_trad.convert_to_trad(word)}<br>{convert_to_trad.convert_simplified_to_traditional(sentences.split('\n')[1].split(',')[0])}<br>{sentences.split('\n')[1].split(',')[1]}<br>{sentences.split('\n')[1].split(',')[2]}<br>[sound:{sentences.split('\n')[1].split(',')[0]}.mp3]<br><img src='{sentences.split('\n')[1].split(',')[0]}_Image_1.jpg' /> <img src='{sentences.split('\n')[1].split(',')[0]}_Image_2.jpg' /> <img src='{sentences.split('\n')[1].split(',')[0]}_Image_3.jpg' />"
            ]
    )


    # Add a note to the deck
    vocab_note = genanki.Note(
        model=model_main_card,
        fields=[
            word,
            convert_to_trad.convert_to_trad(word),
            word_pinyin,
            f'[sound:{word}.mp3]',
            f'<img src="{word}_Image_1.jpg" /> <img src="{word}_Image_2.jpg" /> <img src="{word}_Image_3.jpg" />',
            convert_to_trad.convert_simplified_to_traditional(sentences.split("\n")[0].split(",")[0]),
            sentences.split("\n")[0].split(",")[1],
            sentences.split("\n")[0].split(",")[2],
            f'<img src="{sentences.split("\n")[0].split(",")[0]}_Image_1.jpg" /> <img src="{sentences.split("\n")[0].split(",")[0]}_Image_2.jpg" /> <img src="{sentences.split("\n")[0].split(",")[0]}_Image_3.jpg" />',
            f'[sound:{sentences.split("\n")[0].split(",")[0]}.mp3]',
            convert_to_trad.convert_simplified_to_traditional(sentences.split("\n")[1].split(",")[0]),
            sentences.split("\n")[1].split(",")[1],
            sentences.split("\n")[1].split(",")[2],
            f'<img src="{sentences.split("\n")[1].split(",")[0]}_Image_1.jpg" /> <img src="{sentences.split("\n")[1].split(",")[0]}_Image_2.jpg" /> <img src="{sentences.split("\n")[1].split(",")[0]}_Image_3.jpg" />',
            f'[sound:{sentences.split("\n")[1].split(",")[0]}.mp3]',
            simp_list[0],
            simp_list[1],
            simp_list[2],
            simp_list[3],
            trad_list[0],
            trad_list[1],
            trad_list[2],
            trad_list[3],
            word_def,
            '',
            '',
            '',
            ''
        ],
    )

    my_deck.add_note(vocab_note)
    my_deck.add_note(c1_note)
    my_deck.add_note(c2_note)

    # Add word as a newline to CSV file
    add_row_zero_as_newline(word, csv_file_path)

    # Add word as a newline to TSV file
    add_row_zero_as_newline(word, tsv_file_path, delimiter='\t')

    # Add word as a newline to CSV file
    add_row_zero_as_newline(convert_to_trad.convert_simplified_to_traditional(word), csv_file_path)

    # Add word as a newline to TSV file
    add_row_zero_as_newline(convert_to_trad.convert_simplified_to_traditional(word), tsv_file_path, delimiter='\t')

    print(f"End: {word}\n")