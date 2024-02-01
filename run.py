#################################################
# Chinese card gen 2
#
# TODO
# 1/30/24
# - COMPLETED - note type 2 templates
#   - COMPLETED - move templates to seperate file
# - COMPLETED known words csv and tsv
# - COMPLETED Combine HSK 1-6 into one dataframe
# - COMPLETED Create Set of HSK words that have all known removed
# 2/1/24
# - COMPLETTD Move the combine hsk to its own files
# - COMPLETED Get all feilds for each card
#       - Gen sentences with that py
#       - gen recording of word/sentneces
#           - fix card so recording plays automatically
#           - add recording to cloze
#           - make sentence listening cards in main
#       - convert to trad char
#
#
#################################################

import note_templates
import get_unknown
import pandas as pd
import genanki

known_csv_path = 'Data\\known.csv'
folder_path = 'hsk_csv-master'

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

for index, row in words_to_add.iterrows():

    # Add a note to the deck
    vocab_note = genanki.Note(
        model=model_main_card,
        fields=[
            row[0],
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ],
    )

    c1_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=['{{c1::Rome}} tal of', f'{row[0]}']
    )
    
    c2_note = genanki.Note(
        model=genanki.CLOZE_MODEL,
        fields=['{{c1::Rme}} is the capital of', f'{row[0]}']
    )

    my_deck.add_note(vocab_note)
    my_deck.add_note(c1_note)
    my_deck.add_note(c2_note)

# Save the deck to a file
genanki.Package(my_deck).write_to_file('to_add.apkg')
