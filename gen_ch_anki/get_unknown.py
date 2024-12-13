import os
import pandas as pd

def process_data(known_csv_path, folder_path):
    # Read the known CSV file into a Pandas DataFrame
    known_df = pd.read_csv(known_csv_path)

    # Get a list of all CSV files in the specified folder
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

    # Find unknown words by comparing with the known words DataFrame
    unknown_words = hsk_df[~hsk_df.iloc[:, 0].isin(known_df.iloc[:, 0])]

    # Return the unknown words (you can modify this based on your needs)
    return unknown_words
