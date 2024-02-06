import opencc

def convert_simplified_to_traditional(simplified_text):
    # Create an OpenCC converter for simplified to traditional conversion
    converter = opencc.OpenCC('s2t')  # 's2t.json' is a configuration file for s2t conversion

    # Convert the simplified text to traditional
    traditional_text = converter.convert(simplified_text)

    return traditional_text

def convert_to_trad(simplified_word):
    trad_word = convert_simplified_to_traditional(simplified_word)

    if trad_word != simplified_word:
        return trad_word
    else:
        return ""