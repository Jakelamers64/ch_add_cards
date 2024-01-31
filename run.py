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
# - Move the combine hsk to its own files
# - Get all feilds for each card
#       - Gen sentences with that py
#
#
#################################################

import note_templates
import pandas as pd
import os

# Specify the path to your CSV file
csv_file_path = 'Data\\known.csv'

# Read the CSV file into a Pandas DataFrame
known_df = pd.read_csv(csv_file_path)

# Display the DataFrame
print(known_df.head())

# Specify the path to the folder containing CSV files
folder_path = 'hsk_csv-master'

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
hsk_df = pd.DataFrame()

# Loop through each CSV file and append its data to the combined DataFrame
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, header=None)
    
    # Concatenate the current DataFrame with the combined DataFrame
    hsk_df = pd.concat([hsk_df, df], ignore_index=True)

print(hsk_df.iloc[:,0])

unknown_words = hsk_df[~hsk_df.iloc[:,0].isin(known_df.iloc[:,0])]

print(unknown_words.head())
