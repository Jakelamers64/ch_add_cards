#################################################
# Chinese card gen 2
#
# TODO
# 1/30/24
# - COMPLETED - note type 2 templates
#   - COMPLETED - move templates to seperate file
# - COMPLETED known words csv and tsv
# - Combine HSK 1-6 into one dataframe
# - Create Set of HSK words that have all known removed
# 
# 
# 
#
#
#
#
#################################################

import note_templates
import pandas as pd
import os

# Specify the path to your CSV file
csv_file_path = 'Data\\known.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Display the DataFrame
print(df.head())

"""
# Specify the path to the folder containing CSV files
folder_path = 'hsk_csv-master'

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through each CSV file and append its data to the combined DataFrame
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    # Read the CSV file into a DataFrame
    current_df = pd.read_csv(csv_file_path)

    # Append the current DataFrame to the combined DataFrame
    combined_df = pd.concat([combined_df, current_df], ignore_index=True)

# Display the combined DataFrame
print(combined_df)
"""
