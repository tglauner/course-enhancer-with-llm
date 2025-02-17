"""
LaTeX to Markdown Conversion and Expansion Script

Description:
This script processes a LaTeX file containing sections and subsections, 
extracts the content, and expands it using OpenAI's GPT-4 to generate 
detailed technical book content. The output is saved as a Markdown file.

Key Functionalities:
1. Reads a LaTeX file.
2. Parses sections and subsections using regex.
3. Chunks content for optimal token usage with GPT-4.
4. Expands the content into detailed book sections using AI.
5. Saves the generated content as a structured Markdown file.

Dependencies:
- Python 3.x
- OpenAI API (GPT-4)
- dotenv (for API key management)
- regex (re module for parsing LaTeX)

Usage:
1. Set up your OpenAI API key in a `.env` file with the variable `OPENAI_API_KEY`.
2. Update `input_file` with the path to your LaTeX file.
3. Run the script to generate a structured Markdown document.

Author:
Tim Glauner
"""

import re, os
from dotenv import load_dotenv
import openai

 # openai API setup
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Step 1: Read LaTeX File
def read_latex_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Step 2: Parse Sections and Subsections
def parse_latex_sections(latex_content):
    # Regex patterns for sections and subsections
    section_pattern = r"\\section\{(.*?)\}"
    subsection_pattern = r"\\subsection\{(.*?)\}"
    
    sections = []
    content_split = re.split(section_pattern, latex_content)
    
    for i in range(1, len(content_split), 2):  # Odd indexes are section titles
        section_title = content_split[i].strip()
        section_content = content_split[i + 1]
        
        # Extract subsections
        subsections = []
        subsection_split = re.split(subsection_pattern, section_content)
        
        for j in range(1, len(subsection_split), 2):  # Odd indexes are subsection titles
            subsection_title = subsection_split[j].strip()
            subsection_content = subsection_split[j + 1].strip()
            subsections.append((subsection_title, subsection_content))
        
        sections.append((section_title, subsections))
    
    return sections

# Step 3: Chunk Content for GPT-4
def chunk_text(text, max_tokens=3000):
    # Estimate tokens: ~4 characters per token
    max_chars = max_tokens * 4
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# Step 4: Expand Content with GPT-4
def expand_with_gpt4(title, content):
    chunks = chunk_text(content)
    expanded_content = []
    print('Number of chunks: ', len(chunks))
    for chunk in chunks:
        print('Calling model for chunk')
        prompt = f"""
        Convert the following LaTeX content into a detailed section for a technical book:
        Title: {title}
        Content: {chunk}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert technical writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        expanded_content.append(response['choices'][0]['message']['content'])
    
    print('Return from expand_with_gpt4')
    return "\n".join(expanded_content)

# Step 5: Generate Book Content
def generate_book(sections):
    book_content = []
    
    for section_title, subsections in sections:
        book_content.append(f"# {section_title}\n")
        for subsection_title, subsection_content in subsections:
            print('Processing ', section_title, ' and ', subsection_title, '.')
            expanded_subchapter = expand_with_gpt4(subsection_title, subsection_content)
            book_content.append(f"## {subsection_title}\n")
            book_content.append(expanded_subchapter)
    
    return "\n".join(book_content)

# Step 6: Save Book Content
def save_to_markdown(content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

# Main Program
if __name__ == "__main__":
    input_file = "400 shorter.text"  # Path to your LaTeX file
    output_file = "output_book.md"           # Path to save the markdown file
    
    # Step-by-step process
    latex_content = read_latex_file(input_file)
    sections = parse_latex_sections(latex_content)
    book_content = generate_book(sections)
    save_to_markdown(book_content, output_file)
    
    print(f"Book content saved to {output_file}")
