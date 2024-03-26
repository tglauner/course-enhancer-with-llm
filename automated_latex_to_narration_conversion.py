# automated_latex_to_narration_conversion.py
# Create narrative based on latex file
# Input is the 3 digit lecture number
# Output are individual files based on lecture and section
# TODO modify to take as input always lecture shoftcut. Maybe maintain with json file?

# NOT COMPLETED AS IT WILL NOT BE USED FOR NOW ##################################
import os, sys
from dotenv import load_dotenv
import openai
import tg_tools

CLASS_NAME = '044 Valuation of Swaps and Swap Use Cases' # Modify for new lecture
PATH = ''
COURSE_PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations\\'
)
TRANSCIPT_FILE_NAME = os.path.join(PATH, '044_transcript_youtube_take1_1_6.txt') # Modify for new lecture
OUTPUT_FILE_NAME = os.path.join(PATH, '044_narration_take1_1_6.txt') # Modify for new lecture
MODEL = "gpt-4-1106-preview"
CONTENT_FILE_NAMES = [TRANSCIPT_FILE_NAME]
MAX_TOKENS = 1200

def find_class_name(class_code):
      # Check if the directory exists
    if not os.path.exists(COURSE_PATH):
        print('Directory does not exists: ', COURSE_PATH);
        exit(-1)
    
    # List all folders in the directory
    folders = [folder for folder in os.listdir(COURSE_PATH) if os.path.isdir(os.path.join(COURSE_PATH, folder))]

    # Iterate through the folders and check if the part_of_name is in the folder name
    for folder in folders:
        if class_code in folder:
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = 'You are a graduate school professor.'
  prompt += 'The content you are given is a subset of the total content. It is one section of the beamer presentation'
  prompt += 'The content is a finance course for graduate or advanced undergraduate students or professionals.' 
  prompt += 'Create a new transcript based on the latex section you are given.'
  prompt += 'Narrative should be about 2 minutes per slide.'
  prompt += 'Create reasonable paragraphs but do not change the sequence of the thoughts.'
  prompt += 'The latex beamer section of the presentation is here: ' + inputContent

  print('Calling ', MODEL, ' for creating narrative for section')
  print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))

  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=0,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5
  )
  print("Estimated token length of output:", tg_tools.estimate_token_length(response.choices[0].message.content))
  return response.choices[0].message.content

def my_function(class_code):
  # Load tex file
  # Split file based on section
  # For each section create narration file <<class_code>_auto_narration_<index>_<section(first 10 char)>.txt
  # ask LLM to create narration
  # combine them all
  narrative = ''
  section_narrative = ''
  content = ''

  # openai API setup
  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  # setup filenames and load content
  class_name = find_class_name(class_code)
  tex_file_name = os.path.join(COURSE_PATH, class_name, class_name + '.tex')
  with open(tex_file_name, 'r', encoding='utf-8') as file:
    print('Loading ', tex_file_name)
    content += file.read()
    
  print("Estimated token length of complete input:", tg_tools.estimate_token_length(content))

  # call llm in chunks of text
  counter = 0
  sections = tg_tools.extract_sections_from_beamer_latex(content)
  for section in sections:
    section_name = section['section_name']
    section_content = section['section_content']
    section_narrative = narrativeForSlideWithAI(section_content)
    narrative += f"{section_name}\n{section_narrative}\n"

# if (counter := counter + 1) > 1: break

#  print narrative to file
  print("Estimated token length of complete output:", tg_tools.estimate_token_length(narrative))
  narrative_file_name = os.path.join(COURSE_PATH, class_name, class_code + '_narration_auto' + '.txt')
  print('Writing narrative to ', narrative_file_name)
  with open(narrative_file_name, 'w', encoding='utf-8') as file:
      file.write(narrative)
        
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python automated_latex_to_narration.py <lecture 3 digit code")
    sys.exit(1)

  class_code = sys.argv[1]
  my_function(class_code)
