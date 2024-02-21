#################################################
# Chinese card gen 2
#
# - Fix format of cloze deletion
# - Add listening cards to main note
# - Fix image sizes
# - move gen note to its own file
# - fix easiest sentence is not the first
# - check if new words added based on known.tsv
# - fixed issue with meiguanxi
#
# TODO
#
# - fix issue with 水果 not outputing a file
#
#################################################

import gen_ch_notes
import get_unknown
import pandas as pd
import genanki
import csv
import os
import csv
import glob
import shutil

from pathlib import Path

known_csv_path = 'Data\\known.csv'
folder_path = 'hsk_csv-master'

# File paths
csv_file_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Data\known.csv'
tsv_file_path = r'C:\Users\jakel\Desktop\Code\ch_add_cards\Data\known.tsv'

def convert_csv_to_tsv(csv_file, tsv_file, encoding='utf-8'):
    with open(csv_file, 'r', encoding=encoding) as csv_in, open(tsv_file, 'w', newline='', encoding=encoding) as tsv_out:
        csv_reader = csv.reader(csv_in)
        tsv_writer = csv.writer(tsv_out, delimiter='\t')

        for row in csv_reader:
            tsv_writer.writerow(row)

convert_csv_to_tsv(known_csv_path, 'Data\\known.tsv')

unknown_words_result = get_unknown.process_data(known_csv_path, folder_path)
  
words_to_add = unknown_words_result.head()

# Create a deck
my_deck = genanki.Deck(
    124475623456289475,  # Unique ID for the deck, change this to a different number
    'To Add',
)

media = list()

for index, row in words_to_add.iterrows():
    try:
        gen_ch_notes.gen_ch_notes(row[0], row[1], row[2], my_deck, media)
    except Exception as e:
        print(f"An error occurred for {row[0]}: {e}")

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

