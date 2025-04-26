"""
clean_ssml_tags.py

Description:
    Script to remove SSML tags from narration text files, preserving comments.

Usage:
    python clean_ssml_tags.py <3-digit lecture code>

Input:
    - A narration text file containing SSML tags.

Output:
    - A cleaned narration text file without SSML tags, preserving all comments.

Directory Structure:
    Adjust the BASE_PATH to match your local setup.

Author:
    Tim Glauner

Date:
    April 26, 2025
"""

import os
import sys
import re
from pathlib import Path

# Base directory for lecture files (adjust if necessary)
BASE_PATH = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023' / 'Presentations 2.0'
COURSE_PATH = BASE_PATH

def find_class_name(class_code: str) -> str:
    """
    Finds the folder name corresponding to the provided class code.

    Parameters:
        class_code (str): The 3-digit lecture code.

    Returns:
        str: The name of the class folder.
    """
    if not os.path.isdir(COURSE_PATH):
        sys.exit(f'Directory does not exist: {COURSE_PATH}')

    folders = [folder for folder in os.listdir(COURSE_PATH)
               if os.path.isdir(os.path.join(COURSE_PATH, folder))]

    for folder in folders:
        if class_code in folder:
            return folder

    sys.exit(f'Class not found: {class_code}')

def remove_ssml_tags(line: str) -> str:
    """
    Removes SSML tags from a line, excluding comments.

    Parameters:
        line (str): Line of text potentially containing SSML tags.

    Returns:
        str: Cleaned line without SSML tags.
    """
    return re.sub(r'<(?!\!)[^>]+>', '', line)

def main(class_code: str):
    """
    Main execution function that reads, processes, and outputs the cleaned file.

    Parameters:
        class_code (str): The 3-digit lecture code.
    """
    class_name = find_class_name(class_code)
    input_file = os.path.join(COURSE_PATH, class_name, f'{class_code}_gpt-4-turbo_narration.txt')
    output_file = os.path.join(COURSE_PATH, class_name, f'{class_code}_gpt-4-turbo_narration_no_ssml.txt')

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(remove_ssml_tags(line))

    print(f"Cleaned file created at {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python clean_ssml_tags.py <3-digit lecture code>")
        sys.exit(1)

    main(sys.argv[1])
