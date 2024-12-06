import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

# Ensure you have the necessary NLTK data
nltk.download('punkt')

# Function to read text files
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Function to align prose translations with verse
def align_prose_with_verse(verse_lines, prose_text):
    prose_sentences = sent_tokenize(prose_text)
    aligned_lines = []
    for i, verse_line in enumerate(verse_lines):
        if i < len(prose_sentences):
            aligned_lines.append((verse_line, prose_sentences[i]))
        else:
            aligned_lines.append((verse_line, ""))
    return aligned_lines

# Read the Latin text and English translations
latin_lines = read_text_file('latin.txt')
translation1_lines = read_text_file('translation1.txt')
translation2_text = read_text_file('translation2.txt')  # Prose translation

# Align the prose translation with the Latin text
aligned_translation2 = align_prose_with_verse(latin_lines, translation2_text)

# Create a DataFrame to store the aligned lines
df = pd.DataFrame({
    'Latin': latin_lines,
    'Translation1': translation1_lines,
    'Translation2': [line[1] for line in aligned_translation2]
})

# Save the aligned lines to a new text file
df.to_csv('interlinear_poem.txt', sep='\t', index=False, header=True)

print("Interlinear document created successfully!")
