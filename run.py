#################################################
# Chinese card gen 2
#
# TODO
#
# - Fix format of cloze deletion
# - Add listening cards to main note
# - Fix image sizes
# - move gen note to its own file
#
#################################################

import note_templates
import get_unknown
import convert_to_trad
import pandas as pd
import genanki
import csv
import get_sentence
import re
import os
import csv
import glob
import shutil

from gtts import gTTS
from bing_image_downloader import downloader
from PIL import Image
from pathlib import Path

known_csv_path = 'Data\\known.csv'
folder_path = 'hsk_csv-master'
new_cwd = 'chinese-sentence-miner-master'
mined_sentences_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\chinese-sentence-miner-master\test.txt'
img_output_dir = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Images'

def convert_csv_to_tsv(csv_file, tsv_file, encoding='utf-8'):
    with open(csv_file, 'r', encoding=encoding) as csv_in, open(tsv_file, 'w', newline='', encoding=encoding) as tsv_out:
        csv_reader = csv.reader(csv_in)
        tsv_writer = csv.writer(tsv_out, delimiter='\t')

        for row in csv_reader:
            tsv_writer.writerow(row)

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

def at_least_two_chinese_sentences(input_string):
    # Split the input string into sentences based on the comma separator
    split_str = input_string.split(', ')

    # Count the number of Chinese sentences
    count_chinese_sentences = sum(1 for sentence in split_str if re.search(r'[\u4e00-\u9fff]', sentence))

    # Return true if there are two or more Chinese sentences
    return count_chinese_sentences >= 2

def convert_and_rename(dir_name):
    for root, dirs, files in os.walk(os.path.join(img_output_dir, dir_name)):
        for filename in files:
            original_path = os.path.join(root, filename)
            new_filename = f"{os.path.basename(root)}_{filename}"
            new_path = os.path.join(root, new_filename)
            new_path = re.sub(r'\..*$', '.jpg', new_path)

            try:
                # Open the image file
                with Image.open(original_path) as img:
                     # Save the image as JPG with the .jpg file extension
                    img.convert('RGB').save(new_path, 'JPEG')
                print(f"Conversion successful: {original_path} -> {new_path}")
            except Exception as e:
                print(f"Error converting {original_path} to JPG: {e}")

            #os.rename(original_path, new_path)
            media.append(rf"{new_path}")

convert_csv_to_tsv(known_csv_path, 'Data\\known.tsv')

unknown_words_result = get_unknown.process_data(known_csv_path, folder_path)
  
words_to_add = unknown_words_result.head()

# Create a deck
my_deck = genanki.Deck(
    124475623456289475,  # Unique ID for the deck, change this to a different number
    'To Add',
)

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

media = list()

for index, row in words_to_add.iterrows():
    # Set the number of images to download
    num_images_to_download = 3

    sentences = get_sentence.get_sentence(row[0],new_cwd,mined_sentences_path)

    if not at_least_two_chinese_sentences(sentences):
        print(f"You need to add sentences for {row[0]}\nEnd: {row[0]}\n")
        continue

    print(f"Start: {row[0]}\n{sentences}")

    # sound for word
    media.append(os.path.abspath(text_to_mp3(row[0])))

    # Images for word
    downloader.download(
        row[0], 
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

    convert_and_rename(row[0])
    convert_and_rename(sentences.split("\n")[0].split(",")[0])
    convert_and_rename(sentences.split("\n")[1].split(",")[0])

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[0].split(",")[0])))

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[1].split(",")[0])))

    c1_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[re.sub(row[0],f"{{{{c1::{row[0]}}}}}",sentences.split("\n")[0].split(",")[0]), f"[sound:{media[1]}]<img src='Image_2.jpg'>"]
    )

    c2_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[re.sub(row[0],f"{{{{c1::{row[0]}}}}}",sentences.split("\n")[1].split(",")[0]), f"[sound:{media[2]}]"]
    )

    simp_list = char_to_write(row[0])
    trad_list = char_to_write(convert_to_trad.convert_to_trad(row[0]))

    # Add a note to the deck
    vocab_note = genanki.Note(
        model=model_main_card,
        fields=[
            row[0],
            convert_to_trad.convert_to_trad(row[0]),
            row[1],
            f'[sound:{row[0]}.mp3]',
            f'<img src="{row[0]}_Image_1.jpg" /> <img src="{row[0]}_Image_2.jpg" /> <img src="{row[0]}_Image_3.jpg" />',
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
            row[2],
            '',
            '',
            '',
            ''
        ],
    )

    my_deck.add_note(vocab_note)
    my_deck.add_note(c1_note)
    my_deck.add_note(c2_note)

    print(f"End: {row[0]}\n")

# create package
my_package = genanki.Package(my_deck)
my_package.media_files = media

my_package.write_to_file('to_add.apkg')

# Get the current working directory
cwd = os.getcwd()

# Use glob to find all files with the .mp3 extension in the current directory
mp3_files = glob.glob(os.path.join(cwd, '*.mp3'))

# Delete each .mp3 file
for mp3_file in mp3_files:
    try:
        os.remove(mp3_file)
        print(f"Deleted: {mp3_file}")
    except Exception as e:
        print(f"Error deleting {mp3_file}: {e}")

def delete_all_folders(directory):
    # Get a list of all directories in the specified directory
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    # Delete each folder
    for folder in folders:
        dir_path = Path(directory) / folder

        try:
            shutil.rmtree(dir_path)
            print(f"Directory '{dir_path}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting directory '{dir_path}': {e}")

# Specify the directory path (replace 'Images' with your actual directory)
directory_path = 'Images'

# Delete all folders in the specified directory
delete_all_folders(directory_path)

