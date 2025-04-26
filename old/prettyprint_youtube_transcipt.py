# prettyprint_youtube_transcipt.py

# Cleans up youtube script to be easily readable
# Will require some manual adjustments
import os, sys, re

CLASS_NAME = '080 FX Concepts Main Money IR Parity' # Modify for new lecture
PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations\\' + CLASS_NAME + '\\'
)
TRANSCIPT_FILE_NAME = os.path.join(PATH, '080_transcript_youtube_take1_1_23.txt') # Modify for new lecture
OUTPUT_FILE_NAME = os.path.join(PATH, '080_transcript_youtube_take1_1_23_pretty.txt') # Modify for new lecture
MODEL = "gpt-4-1106-preview"

def my_function():
  content = ''
  pretty = ''

# load content
  with open(TRANSCIPT_FILE_NAME, 'r', encoding='utf-8') as file:
    print('Loading ', TRANSCIPT_FILE_NAME)
    content += file.read()

# Define a regular expression pattern to match timestamps (e.g., "0:00")
  timestamp_pattern = re.compile(r'^\d+:\d+')

# Split the text into lines and remove lines that match the timestamp pattern
  lines = content.split('\n')
  filtered_lines = [line for line in lines if not timestamp_pattern.match(line)]

# Join the filtered lines with spaces to create paragraphs
  paragraphs = ' '.join(filtered_lines)

# Remove extra spaces and print the result
  pretty = re.sub(r'\s+', ' ', paragraphs).strip()
  
# write new pretty content
  print('Writing pretty to ', OUTPUT_FILE_NAME)
  with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
      file.write(pretty)
        
if __name__ == '__main__':
  if len(sys.argv) != 1:
    print("Usage: python prettyprint_youtube_transcipt.py")
    sys.exit(1)
  my_function()
