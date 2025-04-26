# tg_tools.py
import re

class GPT4_parameters:
    temperature = 0.2 # 0
    top_p = 0.6 # 0.5
    frequency_penalty = 0.85 #0.85 might be too high for latex code. So, setting to 0.3
    frequency_penalty_latex = 0.4
    presence_penalty = 0.25 #0.5
    
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

def split_text_by_tokens(latex_content, max_tokens_per_segment):
    # Split the text into words
    words = latex_content.split()
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

def split_text_by_sections_or_subsections(latex_content):
    # Regular expressions for sections, subsections, and slides
    section_pattern = r'\\section{([^}]*)}'
    subsection_pattern = r'\\subsection{([^}]*)}'
    slide_pattern = r'\\begin{frame}.*?\\end{frame}'  # Non-greedy to match individual slides

    # Find all sections in the content
    section_matches = list(re.finditer(section_pattern, latex_content))
    result = []

    for i, section_match in enumerate(section_matches):
        section_start = section_match.end()
        section_end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(latex_content)
        section_content = latex_content[section_start:section_end]

        # Find subsections within the section
        subsection_matches = list(re.finditer(subsection_pattern, section_content))

        if subsection_matches:
            # If subsections exist, process each subsection
            for j, subsection_match in enumerate(subsection_matches):
                subsection_start = subsection_match.end()
                subsection_end = subsection_matches[j + 1].start() if j + 1 < len(subsection_matches) else len(section_content)
                subsection_content = section_content[subsection_start:subsection_end]

                # Extract slides from subsection
                subsection_slides = re.findall(slide_pattern, subsection_content, re.DOTALL)
                result.append("\n\n".join(subsection_slides))
        else:
            # If no subsections, process section slides directly
            section_slides = re.findall(slide_pattern, section_content, re.DOTALL)
            result.append("\n\n".join(section_slides))

    return result

def split_text_by_slides(latex_content, number_max_slides):
    # Define a regular expression pattern to match the beginning and end of each slide
    slide_pattern = r'\\begin{frame}.*?\\end{frame}'

    # Find all slide matches in the LaTeX content
    slide_matches = list(re.finditer(slide_pattern, latex_content, re.DOTALL))

    # Initialize a list to store the text segments for each group of slides
    slides_segments = []

    # Initialize variables for segmenting
    num_slides = len(slide_matches)

    # Iterate through the slides in chunks based on number_max_slides
    for i in range(0, num_slides, number_max_slides):
        segment_end = min(i + number_max_slides, num_slides)

        # Determine the start and end positions for the segment
        start_position = slide_matches[i].start()
        end_position = slide_matches[segment_end - 1].end()  # End at the last slide's \end{frame}

        # Extract the content for the current segment of slides
        segment_content = latex_content[start_position:end_position].strip()
        slides_segments.append(segment_content)

    return slides_segments

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
