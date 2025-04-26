# enhance_narration_based_on_narration.py
# January 6, 2025
# To be used for V2.0
# Input is the 3 digit lecture number
# Output is file with narration_enhanced.txt

import os, sys
from dotenv import load_dotenv
from openai import OpenAI
import tg_tools
from pathlib import Path
import re

INFO = False
DEBUG = False

# Define the base directory (change this if necessary)
BASE_PATH = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023' / 'Presentations 2.0'
COURSE_PATH = BASE_PATH
OUTPUT_PATH = BASE_PATH

MODEL = "gpt-4-turbo"
#MAX_TOKENS = 2000
#MAX_SLIDES = 1 #Seems a single slide works very well. #Make sure it's not too long for the model
NUM_SEGMENTS = 999

def find_class_name(class_code: str) -> str:
    if INFO:
      print('Finding class name ...')
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
            if INFO:
               print('Class name', folder, 'found.')
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def generate_narration_for_segment(inputContent: str) -> str:
  prompt = (
    # Introduction to Role and Purpose
    "You are given a narration. Your tasks is to enhance the wording of the narration without changing its meaning and length."
    "Your narration needs to be easy to follow for students."
    "Keep the slide numbers as is."
    "If the narration for the slide is empty and then return empty narration."

    # Writing Style
    "Write in a direct and accessible style, avoiding metaphors or overly elaborate language."
    "Use short, concise sentences to make the narration easier for the speaker to read aloud."

    "Here is the original narration: \n" + inputContent
  )

  if INFO:
    print('Calling ', MODEL, ' for enhancing narration for new section')
    print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))
  if DEBUG:
     print('***************** Prompt Start *****************')
     print(prompt)
     print('***************** Prompt End *****************\n')
  
  load_dotenv()
  client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
  #return('Dummy OpenAI() return')
  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      {
        'role': 'user',
        'content': prompt
      },
    ],
    temperature = tg_tools.GPT4_parameters.temperature,
    top_p = tg_tools.GPT4_parameters.top_p,
    frequency_penalty = tg_tools.GPT4_parameters.frequency_penalty,
    presence_penalty = tg_tools.GPT4_parameters.presence_penalty
  )
  if DEBUG:
     print('************** OpenAI() response start ****************')
     print('OpenAI() returns\n', response.choices[0].message.content)
     print('************** OpenAI() response end ****************\n')

  if INFO:
    print("Estimated token length of output:", tg_tools.estimate_token_length(response.choices[0].message.content))
  return response.choices[0].message.content

def split_text_by_slide_patterns(text_content):
    # Regular expression to match "Slide n" pattern
    slide_pattern = r'Slide\s+\d+'
    
    # Find all slide markers
    slide_matches = list(re.finditer(slide_pattern, text_content))
    result = []
    
    for i, slide_match in enumerate(slide_matches):
        # Start of the current slide
        start_index = slide_match.end()
        # End of the current slide (start of the next slide or end of text)
        end_index = slide_matches[i + 1].start() if i + 1 < len(slide_matches) else len(text_content)
        
        # Extract the text between the current slide and the next slide
        slide_content = text_content[start_index:end_index].strip()
        
        # Include slide header and its content in the result
        slide_header = slide_match.group()
        result.append(f"{slide_header}\n{slide_content}")
    
    return result


def main(class_code, start, end):
  if INFO:
     print('Executing main with', class_code, start, end)

  # Load tex file
  # Split file based on section
  # For each section create description using LLM
  # combine the descriptions all into a single file and write out

  class_name = find_class_name(class_code)
  narration_file_name = os.path.join(COURSE_PATH, class_name, class_code + '_narration.txt') 
  with open(narration_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

  output = ""

  if INFO:
    print("Estimated token length of complete program input:", tg_tools.estimate_token_length(content))

  # call llm in chunks of text
  counter = 1

  segments = split_text_by_slide_patterns(content)
#['segment sdfasdfsad', 'vfasdfvdavdvfda', 'Dfsdfa']

  for segment in segments:
    if INFO:
        print("Processing slide",counter)
    if counter < start:
      if INFO:
        print("Skipping slide",counter)
      counter = counter + 1
      continue
    if counter > end:
      if INFO:
        print("Breaking out on slide", counter)
      break

    #segment_narration = "Dummy new narration " + str(counter) +"."
    segment_narration = generate_narration_for_segment(segment)
    if DEBUG:
      print('***************** Narration Start *****************')
      print(segment_narration)
      print('***************** Narration End** *****************\n')
 
    output += f"{segment_narration}\n\n"
    if counter == NUM_SEGMENTS:
       print("Breaking out ...")
       break
    counter = counter + 1

  enhanced_narration_file_name = os.path.join(OUTPUT_PATH, class_name, class_code + '_narration_enhanced.txt')
  if INFO:
    print('Writing to ', enhanced_narration_file_name)
  with open(enhanced_narration_file_name, 'w', encoding='utf-8') as file:
    file.write(output)
        
if __name__ == '__main__':
  if len(sys.argv) != 4:
    print("Usage: python enhance_narration_based_on_narration.py <lecture 3 digit code as string> <first slide> <last slide>")
    sys.exit(1)

  class_code = sys.argv[1]
  start = int(sys.argv[2])
  end = int(sys.argv[3])
  main(class_code, start, end)

