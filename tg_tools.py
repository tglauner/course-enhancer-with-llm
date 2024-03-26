# tg_tools.py
import re

def estimate_token_length(text):
    # Splitting the text by spaces for a rough estimate
    words = text.split()

    # Counting the number of words and assuming each word is a token
    token_count = len(words)

    # Adjusting for common punctuations that are likely to be separate tokens
    for word in words:
        for char in [',', '.', '!', '?', ';', ':']:
            if char in word:
                token_count += 1

    return token_count

def split_text_by_tokens(text, max_tokens_per_segment):
    # Split the text into words
    words = text.split()
    segments = []
    current_segment = []

    for word in words:
        current_segment.append(word)
        # Check if adding this word exceeds the max token limit
        if estimate_token_length(' '.join(current_segment)) > max_tokens_per_segment:
            # Finish the current segment and start a new one
            current_segment.pop()  # Remove the last word that caused the overflow
            segments.append(' '.join(current_segment))
            current_segment = [word]

    # Add the last segment if it's not empty
    if current_segment:
        segments.append(' '.join(current_segment))

    return segments

def extract_sections_from_beamer_latex(latex_content):
    # Define a regular expression pattern to match sections
    section_pattern = r'\\section{([^}]*)}'

    # Find all section matches in the LaTeX content
    section_matches = list(re.finditer(section_pattern, latex_content))

    # Initialize a list to store the text segments for each section
    sections = []

    # Iterate through the section matches
    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip()  # Get the section name
        section_start = match.start()            # Start position of the section
        section_end = match.end()                # End position of the section

        # Determine the content for the current section
        if i + 1 < len(section_matches):
            # If not the last section, end at the start of the next section
            next_section_start = section_matches[i + 1].start()
            section_content = latex_content[section_end:next_section_start].strip()
        else:
            # For the last section, end at the end of the file
            section_content = latex_content[section_end:].strip()

        # Add the section name and content to the sections list
        sections.append({
            'section_name': section_name,
            'section_content': section_content
        })

    return sections
