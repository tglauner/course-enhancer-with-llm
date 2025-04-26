"""
count_beamer_slides.py

Description:
    Script to count the total number of Beamer slides in LaTeX files within a specified directory and all its subdirectories.

Usage:
    python count_beamer_slides.py

Input:
    - Directory containing LaTeX (.tex) files formatted for Beamer presentations.

Output:
    - Prints individual slide counts for each LaTeX file.
    - Prints the total number of slides across all files.

Directory Structure:
    Adjust the DIRECTORY path variable as necessary.

Author:
    Tim Glauner

Date:
    April 26, 2025
"""

import os
import re
from pathlib import Path

# Base directory containing LaTeX files (adjust if necessary)
DIRECTORY = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023'

def preprocess_content(content: str) -> str:
    """
    Normalizes line endings and removes trailing whitespace from content.

    Parameters:
        content (str): Raw file content.

    Returns:
        str: Preprocessed content.
    """
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    content = '\n'.join(line.rstrip() for line in content.split('\n'))
    return content

def count_beamer_slides_in_file(file_path: str) -> int:
    """
    Counts the number of Beamer slides in a single LaTeX file.

    Parameters:
        file_path (str): Path to the LaTeX file.

    Returns:
        int: Number of slides in the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = preprocess_content(file.read())
        slides = re.findall(r'\\begin\{frame.*?\}\s*\{.*?\}', content, re.DOTALL)
        return len(slides)

def main():
    """
    Main execution function to count slides across all .tex files and report totals.
    """
    tex_files = []
    for root, _, files in os.walk(DIRECTORY):
        tex_files.extend(os.path.join(root, file) for file in files if file.endswith('.tex'))

    tex_files.sort()

    total_slides = 0
    file_slide_counts = {}

    for tex_file in tex_files:
        slide_count = count_beamer_slides_in_file(tex_file)
        file_slide_counts[tex_file] = slide_count
        total_slides += slide_count

    for tex_file in tex_files:
        print(f"{tex_file}: {file_slide_counts[tex_file]} slides")

    print(f"\nTotal number of Beamer slides: {total_slides}")

if __name__ == "__main__":
    main()
