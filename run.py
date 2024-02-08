#################################################
# Chinese card gen 2
#
# TODO
#
# - COMPLETED Get all feilds for each card
#       - Gen sentences with that py
#       - gen recording of word/sentneces
#           - fix card so recording plays automatically
#           - add recording to cloze
#           - make sentence listening cards in main
#       - convert to trad char
#
# - Determine why get_sentence returning different
#
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
from gtts import gTTS

known_csv_path = 'Data\\known.csv'
folder_path = 'hsk_csv-master'
new_cwd = 'chinese-sentence-miner-master'
mined_sentences_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\chinese-sentence-miner-master\test.txt'

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

convert_csv_to_tsv(known_csv_path, 'Data\\known.tsv')

unknown_words_result = get_unknown.process_data(known_csv_path, folder_path)
  
words_to_add = unknown_words_result.head()

# Create a deck
my_deck = genanki.Deck(
    124475623456289475,  # Unique ID for the deck, change this to a different number
    'To Add',
)

my_deck.media_files = []

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
    sentences = get_sentence.get_sentence(row[0],new_cwd,mined_sentences_path)

    media.append(os.path.abspath(text_to_mp3(row[0])))

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[0].split(",")[0])))

    media.append(os.path.abspath(text_to_mp3(sentences.split("\n")[1].split(",")[0])))

    c1_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[re.sub(row[0],f"{{{{c1::{row[0]}}}}}",sentences.split("\n")[0].split(",")[0]), f"[sound:{media[1]}]"]
    )

    c2_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=[re.sub(row[0],f"{{{{c1::{row[0]}}}}}",sentences.split("\n")[1].split(",")[0]), f"[sound:{media[2]}]"]
    )

    # Add a note to the deck
    vocab_note = genanki.Note(
        model=model_main_card,
        fields=[
            row[0],
            convert_to_trad.convert_to_trad(row[0]),
            row[1],
            f'[sound:{media[0]}]',
            '',
            '',
            '',
            '',
            '',
            f"[sound:{media[1]}]",
            '',
            '',
            '',
            '',
            f"[sound:{media[2]}]",
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
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

    break

print(my_deck.media_files)

my_deck.media_files = media

print(my_deck.media_files)

my_deck.write_to_file('to_add.apkg')
