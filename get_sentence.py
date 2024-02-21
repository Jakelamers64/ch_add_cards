import os
import subprocess

def get_sentence(word, new_cwd, mined_sentences_path):
    # Save the current working directory
    original_cwd = os.getcwd()

    # Set the new working directory
    os.chdir(new_cwd)

    # Command to run
    # python assigner.py -m --string f'{word}' -l C:\\Users\\jakel\\Desktop\\Code\\ch_add_cards\\Data\\known.tsv --limit 2 -s custom -o custom --easy
    command = [
        'python', 
        'assigner.py',
        '-m',
        '--string', f'{word}',
        '-l', 'C:\\Users\\jakel\\Desktop\\Code\\ch_add_cards\\Data\\known.tsv',
        '--limit', '2',
        '-s', 'custom',
        '-o', 'custom',
        '--easy'
    ]

    try:
        # Run the subprocess command
        subprocess.run(command)

    except subprocess.CalledProcessError as e:
        # Handle any subprocess errors
        print(f"Error: {e}")
        print(f"Exit Status: {e.returncode}")

    finally:
        # Change back to the original working directory
        os.chdir(original_cwd)

    file_content = ""

    # Open and read the content of the file
    with open(mined_sentences_path, 'r', encoding='utf-8') as file:
        file_content = file_content + file.read() + "\n"

    # Check if the file exists before attempting to delete it
    if os.path.exists(mined_sentences_path):
        os.remove(mined_sentences_path)
        print(f'The file for {word} has been deleted.')
    else:
        print(f'The file for {word} does not exist.')

    return file_content

# test
#if __name__ == '__main__':
#    get_sentence('水果',
#                 'chinese-sentence-miner-master',
#                 r'C:\Users\jakel\Desktop\Code\ch_add_cards\chinese-sentence-miner-master\output.txt')
