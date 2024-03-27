# generate_description_based_on_latex.py
# Create description based on latex files
# GPT4 recommends to use pdf file with agent but it's much more expensive
# Input is the 3 digit lecture number
# Output is file with description
# Creates consistent format and wording across all lectures when executed in batch - not sure why it's so good

import os, sys
from dotenv import load_dotenv
import openai
import tg_tools

COURSE_PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations\\'
)
DESCRIPTION_PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations\\LLM_Descriptions\\'
)
MODEL = "gpt-4-1106-preview"
MAX_TOKENS = 4000

def find_class_name(class_code: str) -> str:
      # Check if the directory exists
    if not os.path.isdir(COURSE_PATH):
      print(f'Directory does not exist: {COURSE_PATH}', file=sys.stderr)
      sys.exit(-1)
    
    # List all folders in the directory
    folders = [folder for folder in os.listdir(COURSE_PATH) if os.path.isdir(os.path.join(COURSE_PATH, folder))]

    # Iterate through the folders and check if xlass_code is in the folder name
    for folder in folders:
        if class_code in folder:
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def generate_description_for_section(inputContent: str) -> str:
  prompt = 'You are a graduate school professor and create an online course that is being sold.'
  prompt += 'Write the answer to the following \"What will students be able to do at the end of this section?\"'
  prompt += 'Write in a straightforward style without metaphors or elaborate language.'
  prompt += 'Provide 5-10 items depending on complexity of lecture. The more complex the more items.'
  prompt += 'Your objective is to maximize the number of students the course is being sold to.'
  prompt += 'Do not exceed 200 character length'
  prompt += 'The content given to you at the end is latex source code of the presentation for the lecture.'
  prompt += 'You are given one lecture only of the course. It is one section or the complete beamer presentation'
  prompt += 'The course content is a finance course for graduate or advanced undergraduate students or professionals who want to work for a bank.' 
  prompt += 'To avoid hitting your token limit limit the reponse to 800 tokens'
  prompt += 'The latex beamer section of the presentation is here: ' + inputContent

  # print('Calling ', MODEL, ' for creating narrative for section')
  print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))

  completion = openai.chat.completions.create(
    model=MODEL,
    messages=[
      {
        'role': 'user',
        'content': prompt
      },
    ],
    temperature=0,
    top_p=0.5,
    frequency_penalty=0.5,
    presence_penalty=0.5
  )
  print("Estimated token length of output:", tg_tools.estimate_token_length(completion.choices[0].message.content))
  return completion.choices[0].message.content

def my_function(class_code):
  # Load tex file
  # Split file based on section
  # For each section create description using LLM
  # combine the descriptions all into a single file and write out

  class_name = find_class_name(class_code)
  latex_file_name = os.path.join(COURSE_PATH, class_name, class_name + '.tex') 
  with open(latex_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

  output = '****** ------ Description generated for ' + class_name + '\n\n'

  # openai API setup
  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  print("Estimated token length of complete program input:", tg_tools.estimate_token_length(content))

  # call llm in chunks of text
  counter = 1
  segments = tg_tools.split_text_by_tokens(content, MAX_TOKENS)
  for segment in segments:
    print('Processing segment number ', counter)
    section_description = generate_description_for_section(segment)
    output += f"*** --- SEGMENT: {counter}\n{section_description}\n\n"
    counter = counter + 1

  #  print narrative to file
  description_file_name = os.path.join(DESCRIPTION_PATH, class_code + '_description' + '.txt')
  print('Writing to ', description_file_name)
  with open(description_file_name, 'a', encoding='utf-8') as file:
    file.write(output)
        
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python generate_description_based_on_latex.py <lecture 3 digit code as string>")
    sys.exit(1)

  class_code = sys.argv[1]
  my_function(class_code)
