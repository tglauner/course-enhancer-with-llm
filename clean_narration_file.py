# clean_narration_file.py
# August18, 2024
# To be used for V2.0
# Remove white spaces from ssml file to easily paste it into MS editor
# Input is the 3 digit lecture number
# Output is new file

import os, sys, re
import tg_tools
from pathlib import Path

# Define the base directory (change this if necessary)
BASE_PATH = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023' / 'Presentations 2.0'
COURSE_PATH = BASE_PATH
OUTPUT_PATH = BASE_PATH

# Define your replacement rules
replacement_rules = {
    r'”': '"',
    r'<\s*break_strength': '<break strength',
    r'<\s*breakstrength': '<break strength',
    r'<\s*breakstrength\s*=\s*"\s*x\s*-\s*strong\s*"\s*/\s*>': '<break strength="x-strong"/>',
    r'<\s*break\s+strength\s*=\s*"x-strong"\s*/\s*>': '<break strength="x-strong"/>',
    r'<\s*break_strength\s*=\s*"x-strong"\s*/\s*>': '<break strength="x-strong"/>',
    r'<\s*x\s*-\s*strong\s*>': '<break strength="x-strong"/>',
    r'<\s*break\s*x\s*-\s*strong\s*>': '<break strength="x-strong"/>',
    r'<\s*break\s*x\s*-\s*strong\s*/>': '<break strength="x-strong"/>',
    r'<\s*breath\s*x\s*-\s*strong\s*/>': '<break strength="x-strong"/>',
    r'<\s*breathe\s*x\s*-\s*strong\s*/>': '<break strength="x-strong"/>',
    r'<\s*break_strength\s*=\s*"strong"\s*/\s*>': '<break strength="strong"/>',
    r'<\s*break\s+strength\s*=\s*"strong"\s*/\s*>': '<break strength="strong"/>',
    r'<\s*break\s*strong\s*>': '<break strength="strong"/>',
    r'<\s*break\s*strong\s*/>': '<break strength="strong"/>',
    r'<\s*breath\s*strong\s*/>': '<break strength="strong"/>',
    r'<\s*breathe\s*strong\s*/>': '<break strength="strong"/>',
    r'<\s*strong\s*>': '<break strength="strong"/>',
    r'<\s*br\s*/\s*>': '<br/>',
    r'<\s*break\s*/\s*>': '',  # Removes any break tags without attributes
    r'\n': '',  # Removes newlines
    r'P&L': 'P and L',  # Custom text replacement
}

def find_class_name(class_code: str) -> str:
    print('Looking for class name for code ', class_code)
      # Check if the directory exists
    if not os.path.isdir(COURSE_PATH):
      print(f'Directory does not exist: {COURSE_PATH}', file=sys.stderr)
      sys.exit(-1)
    
    # List all folders in the directory
    folders = [folder for folder in os.listdir(COURSE_PATH) if os.path.isdir(os.path.join(COURSE_PATH, folder))]

    # Iterate through the folders and check if class_code is in the folder name
    for folder in folders:
#        print(folder)
        if class_code in folder:
            print('Found class name ', folder)
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def clean_line(line):
    # Apply all replacements
    for pattern, replacement in replacement_rules.items():
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
    return line

def main(class_code):

  class_name = find_class_name(class_code)
  file_name = os.path.join(COURSE_PATH, class_name, class_code+ '_gpt-4-turbo_narration.txt') 
  clean_file_name = os.path.join(COURSE_PATH, class_name, class_code+ '_gpt-4-turbo_narration_clean.txt')
  with open(file_name, 'r', encoding='utf-8') as file, open(clean_file_name, 'w', encoding='utf-8') as clean_file:
     for line in file:
        # Replace carriage return with nothing
        cleaned_line = clean_line(line)
        clean_file.write(cleaned_line)
  print("Cleaned file created.")
        
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python clean_narration_file.py <lecture 3 digit code as string>")
    sys.exit(1)

  class_code = sys.argv[1]
  main(class_code)
