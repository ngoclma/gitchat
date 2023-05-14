import PyPDF2
import json
import re

# Paths
pdf_path = 'gitchat/_data/progit.pdf'
raw_text_path = 'gitchat/_data/rawgitbook.txt'
text_path = 'gitchat/_data/gitbook.txt'
json_path = 'gitchat/_data/book-data.json'

# Lines
tablecontent_start_line = 9
tablecontent_end_line = 121

# Book data
book_title = 'Pro Git'
author = 'Scott Chacon and Ben Straub'
edition = 'Second Edition'

## Functions
def convert_pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def remove_undefined_characters(inp_path, out_path):
    with open(inp_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove undefined characters using regular expressions
    cleaned_content = re.sub(r'[^\x00-\x7F]+', '', content)

    with open(out_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def read_lines_from_file(file_path, start_line, end_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Adjust the line numbers to account for zero-based indexing
    start_line -= 1
    end_line -= 1

    # Slice the list of lines to extract the desired range
    selected_lines = lines[start_line:end_line+1]
    
    return selected_lines

def extract_section_names(contents):
    section_names = []
    pattern = r"([A-Za-z\s]+) \."
    for line in contents:
        matches = re.findall(pattern, line)
        for match in matches:
            section_names.append(match.strip())
    return section_names

def find_second_occurrence(string, substring):
    first_occurrence = string.find(substring)
    if first_occurrence == -1:
        return -1

    second_occurrence = string.find(substring, first_occurrence + len(substring))
    return second_occurrence

def extract_substring(string, start_substring, end_substring):
    start_index = find_second_occurrence(string, start_substring)
    if start_index == -1:
        return None

    end_index = find_second_occurrence(string, end_substring)
    if end_index == -1:
        return None

    extracted_substring = string[start_index + len(start_substring):end_index]
    return extracted_substring

def convert_text_to_json(book_title, author, edition, book_content):
    book_data = {
        "title": book_title,
        "author": author,
        "edition": edition,
        "content": []
    }

    for section_title, section_text in book_content.items():
        section_data = {
            "title": section_title,
            "content": section_text
        }
        book_data["content"].append(section_data)

    return book_data

def save_json_to_file(json_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(json_data, file, indent=4)

## Usage

# Convert and store
# text = convert_pdf_to_text(pdf_path)
# save_text_to_file(text, raw_text_path)
# remove_undefined_characters(raw_text_path, text_path)

# Extract sections title and content
with open(text_path, 'r', encoding='utf-8') as file:
    book_text = file.read()

contents = read_lines_from_file(text_path, tablecontent_start_line, tablecontent_end_line)
book_titles = extract_section_names(contents)
no_titles = len(book_titles)
book_content = {}

for i in range(no_titles - 1):
    title = book_titles[i]
    start_substring = book_titles[i]
    end_substring = book_titles[i+1]
    text = extract_substring(book_text, start_substring, end_substring)
    if (text != None):
        text = text.replace('\n', ' ')
        text = text.replace('\\', '\\\\')
        text = text.replace('\ ', ' ')
        text = text.replace('"', '`')
    else:
        text = ''
    book_content[title] = text

# Convert to JSON
json_data = convert_text_to_json(book_title, author, edition, book_content)
save_json_to_file(json_data, json_path)