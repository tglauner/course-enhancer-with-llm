# generate_narration_based_on_latex.py
# July 10, 2024
# To be used for V2.0
# Generates text that should be read by human speaker w. tele prompter
# Input is actual latex source code
# Input is the 3 digit lecture number
# Output is file with narration

import os, sys
from dotenv import load_dotenv
import openai
import tg_tools
from pathlib import Path

INFO = False
DEBUG = False

# Define the base directory (change this if necessary)
BASE_PATH = Path.home() / 'Dropbox' / '2 - TG Investments and Research' / 'Projects' / 'Capital Markets text book and course 2023' / 'Presentations 2.1'
COURSE_PATH = BASE_PATH
OUTPUT_PATH = BASE_PATH

MODEL = "gpt-4-turbo"
#MAX_TOKENS = 2000
#MAX_SLIDES = 1 #Seems a single slide works very well. #Make sure it's not too long for the model
NUM_SEGMENTS = 999


# START = "Welcome to the lecture about TODO. <break strength=\"x-strong\"/> Before we begin, please note the information regarding copyright and trademark."
# END = "<break strength=\"x-strong\"/> Thank you for attending the lecture. <break strength=\"strong\"/>If you have any questions or comments please do not hesitate to reach out via the comments or email. <break strength=\"strong\"/>I am looking forward to seeing you in the next session."
START = "Welcome to the lecture about TODO. Before we begin, please note the information regarding copyright and trademark."
END = "Thank you for attending the lecture. If you have any questions or comments please do not hesitate to reach out via the comments or email. I am looking forward to seeing you in the next session."

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
               print('Class name ', folder, ' found.')
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def generate_narration_for_segment(inputContent: str) -> str:
  prompt = (
    # Introduction to Role and Purpose
    "You are a graduate school professor at an Ivy League college and the creator of an advanced online course designed for MBA students and professionals."
    "This lecture is part of a comprehensive course. Your role is to guide students through the specific content provided in each slide with clarity and professionalism."
    "Do not include any welcome, closing remarks, or content that is not directly related to the slides."
    "A speaker needs to be able to take the narration as is and read it so the results sounds as if he giving a lecture"

    # Focus on Slide-by-Slide Narration
    "Your task is to carefully read and understand the content of the slides and craft a narration for each slide."
    "The narration should be clear, professional, and easy to follow, explaining the material slide by slide and from top to bottom."

    "Provide explanation and short examples when appropriate without increasing the content very significantly."
    "Ensure your tone remains engaging and confident, suitable for advanced learners."

    # Writing Style
    "Write in a direct and accessible style, avoiding metaphors or overly elaborate language."
    "Use short, concise sentences to make the narration easier for the speaker to read aloud."

    # Additional Context and Explanations
    "While adhering closely to the slide content, feel free to add relevant context or concise explanations where needed to maximize understanding."
    "For non-trivial formulas, focus on explaining their implications rather than describing the formulas explicitly."
    "If a formula is simple and almost definitional, briefly explain its meaning."

    # SSML and Formatting
    "Add an SSML comment tag with the slide title for documentation but do not add the slide title to the narration."
    "Avoid using SSML tags directly in the text as they are not required for this format."

    # Student-Centric Focus
    "Your ultimate goal is to enhance comprehension and retention for MBA-level students and professionals."
    "Maintain a balance between informativeness and brevity, ensuring the narration is engaging but does not overwhelm the audience."

    # Slide Content Input
    "Here is the LaTeX source code for the slide content: \n" + inputContent
  )

  if INFO:
    print('Calling ', MODEL, ' for creating narrative for new section')
    print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))
  if DEBUG:
     print('************************************************')
     print('***************** Prompt Start *****************')
     print('************************************************')
     print(prompt)
     print('************************************************')
     print('***************** Prompt End** *****************')
     print('************************************************')
  
  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  response = openai.ChatCompletion.create(
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
  #print('OpenAI() returns', response.choices[0].message.content)
  if INFO:
    print("Estimated token length of output:", tg_tools.estimate_token_length(response.choices[0].message.content))
  return response.choices[0].message.content

def main(class_code):
  # Load tex file
  # Split file based on section
  # For each section create description using LLM
  # combine the descriptions all into a single file and write out

  class_name = find_class_name(class_code)
  latex_file_name = os.path.join(COURSE_PATH, class_name, class_name + '.tex') 
  with open(latex_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

  output = START + "\n\n"

  if INFO:
    print("Estimated token length of complete program input:", tg_tools.estimate_token_length(content))

  # call llm in chunks of text
  counter = 1

  segments = tg_tools.split_text_by_sections_or_subsections(content)

  for segment in segments:
    # print('Processing segment number ', counter)
    # print(segment)
    output += f"<!-- ************ New Segment Started ************ -->\n"
    segment_narration = generate_narration_for_segment(segment)
    if DEBUG:
      print('***************************************************')
      print('***************** Narration Start *****************')
      print('***************************************************')
      print(segment_narration)
      print('***************************************************')
      print('***************** Narration End** *****************')
      print('***************************************************')
    # print('Narration:\n', segment_narration)
    output += f"{segment_narration}\n\n"
    if counter == NUM_SEGMENTS:
       print("Breaking out ...")
       break
    counter = counter + 1

  output = output + "\n\n" + END

  #  print narrative to file
  narration_file_name = os.path.join(OUTPUT_PATH, class_name, class_code + '_gpt-4-turbo_narration' + '.txt')
  if INFO:
    print('Writing to ', narration_file_name)
  with open(narration_file_name, 'w', encoding='utf-8') as file:
    file.write(output)
        
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python generate_narration_based_on_latex.py <lecture 3 digit code as string>")
    sys.exit(1)

  class_code = sys.argv[1]
  main(class_code)

