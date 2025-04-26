from openai import OpenAI
import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# OpenAI API setup
load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# Define the base directory (adjust this path if necessary)
BASE_PATH = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023' / 'Presentations 2.0'
COURSE_PATH = BASE_PATH

def find_class_name(class_code: str) -> str:
    """
    Finds the folder name corresponding to the class code.
    """
    print('Looking for class name for code:', class_code)
    if not os.path.isdir(COURSE_PATH):
        print(f"Directory does not exist: {COURSE_PATH}", file=sys.stderr)
        sys.exit(-1)

    # Search for the folder that contains the class code
    folders = [folder for folder in os.listdir(COURSE_PATH) if os.path.isdir(os.path.join(COURSE_PATH, folder))]
    for folder in folders:
        if class_code in folder:
            print('Found class name:', folder)
            return folder

    print('Class not found:', class_code)
    exit(-1)

def read_text_file(file_path):
    """
    Reads the content of a text file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        exit(1)

def split_text_into_chunks(text, max_length=4000):
    """
    Splits text into chunks of specified maximum length, preserving paragraph boundaries.
    """
    paragraphs = text.split("\n\n")  # Split text into paragraphs
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # Add the paragraph if it fits in the current chunk
        if len(current_chunk) + len(paragraph) <= max_length:
            current_chunk += paragraph + "\n\n"
        else:
            # If the current paragraph exceeds the limit, start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def generate_tts_with_openai(text, output_file, model="tts-1", voice="alloy"):
    """
    Generates TTS audio using OpenAI's TTS API.
    """
    speech_file_path = Path(output_file)
    
    try:
        print(f"Generating TTS audio for {output_file}...")
        client = OpenAI()
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        print(f"Audio saved to: {output_file}")
    except Exception as e:
        print(f"Error generating TTS with OpenAI: {e}")
        exit(1)

def main(class_code):
    """
    Main function to process files for a given class code.
    """
    class_name = find_class_name(class_code)
    input_file = os.path.join(COURSE_PATH, class_name, class_code + '_gpt-4-turbo_narration.txt')
    output_folder = os.path.join(COURSE_PATH, class_name)

    # Read the text file
    text = read_text_file(input_file)

    # Split text into chunks to respect the API's character limit
    chunks = split_text_into_chunks(text, max_length=4000)

    # Generate TTS files for each chunk
    for i, chunk in enumerate(chunks, start=1):
        output_file = os.path.join(output_folder, f"{class_code}_tts_audio_part_{i}.mp3")
        generate_tts_with_openai(chunk, output_file)

    print(f"All audio files generated for class code {class_code}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_tts.py <3-digit class code>")
        sys.exit(1)

    class_code = sys.argv[1]
    main(class_code)
