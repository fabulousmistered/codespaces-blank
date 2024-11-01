import re
import requests

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def divide_text(lines):
    divided_lines = []
    for line in lines:
        words = re.findall(r'\b\w+\b', line)  # This regex finds all words
        divided_lines.append(words)
    return divided_lines

def extract_unique_words_ordered(divided_lines):
    unique_words = []
    seen_words = set()
    for line in divided_lines:
        for word in line:
            if word not in seen_words:
                unique_words.append(word)
                seen_words.add(word)
    return unique_words

def get_word_info(word, api_key):
    url = f'https://www.latin-is-simple.com/api/vocabulary/{word}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('translations_unstructured', {}).get('en', 'No info available')
        else:
            return 'No info available'
    except requests.RequestException as e:
        print(f"Error fetching data for {word}: {e}")
        return 'No info available'

def generate_html_content(divided_lines, word_info):
    html_content = '<html><body><p>'
    for line in divided_lines:
        for word in line:
            info = word_info.get(word, 'No info available')
            html_content += f'<span class="tooltip">{word}<span class="tooltiptext">{info}</span></span> '
        html_content += '<br>'
    html_content += '</p></body></html>'
    return html_content

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def write_unique_words(file_path, unique_words):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word in unique_words:
            file.write(f"{word}\n")

def write_word_info(file_path, word_info):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, info in word_info.items():
            file.write(f"{word}: {info}\n")

def main():
    try:
        lines = read_file('metafull.txt')
        divided_lines = divide_text(lines)
        
        # Extract unique words in order
        unique_words = extract_unique_words_ordered(divided_lines)
        
        # Write unique words to a separate file
        write_unique_words('unique_words.txt', unique_words)
        
        # Create the dictionary with word information
        api_key = 'vBppUWBT3D8CZPhngy0OW7D4hg6mkg0UQb1adCHjZUcINH3XbeOPR7NrotCA8jFT'
        word_info = {}
        
        for word in unique_words:
            print(f"Fetching data for {word}...")
            word_info[word] = get_word_info(word, api_key)
        
        # Write word information to a separate file
        write_word_info('word_info.txt', word_info)
        
        html_content = generate_html_content(divided_lines, word_info)
        write_file('output.html', html_content)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
