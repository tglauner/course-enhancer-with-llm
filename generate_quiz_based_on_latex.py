# generate_quiz_based_on_latex.py
# Create multiple choice quiz based on each section in a latex file
# Input is the 3 digit lecture number
# Output is file with muliple choice quiz

import os, sys
from dotenv import load_dotenv
import openai
import tg_tools

COURSE_PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations\\'
)
MODEL = "gpt-4-1106-preview"
MAX_TOKENS = 1200

def find_class_name(class_code: str) -> str:
      # Check if the directory exists
    if not os.path.exists(COURSE_PATH):
        print('Directory does not exists: ', COURSE_PATH);
        exit(-1)
    
    # List all folders in the directory
    folders = [folder for folder in os.listdir(COURSE_PATH) if os.path.isdir(os.path.join(COURSE_PATH, folder))]

    # Iterate through the folders and check if xlass_code is in the folder name
    for folder in folders:
        if class_code in folder:
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def generate_quiz_for_section(inputContent: str) -> str:
  prompt = 'You are a graduate school professor.'
  prompt += 'The content is latex source code of a presentation. You are given is a subset of the total content. It is one section of a beamer presentation'
  prompt += 'The content is a finance course for graduate or advanced undergraduate students or professionals.' 
  prompt += 'Create a muliple choice quiz with 10 questions for this section and each multiple choice question has 3 answers of which one is correct.'
  prompt += 'In addition to stating which answer is correct and the reason, state for the incorrect answers the reason why they are incorrect.'
  prompt += 'Also state the reason why the correct answer is correct without just repeating the answer but explaining why it is correct. Also, do not refer to the fact that it is stated in the presentation but explain why'
  prompt += 'For the correct answer give the reason and always start a single sentence with Correct because ...'
  prompt += 'For the incorrect answer give the reason and always start a single sentence with Incorrect because ...'
  # prompt += 'After you have written out the questions and answers you need to create a section with csv format precisely in the following format with 8 columns:'
  # prompt += 'Here is the top row and then three sample rows. In your output you should create one row for each question. So, expected to have 11 rows in the output'
  # prompt += 'Question,Question Type (multiple-choice or multi-select),Answer Option 1,Answer Option 2,Answer Option 3,Correct Response,Explanation,Knowledge Area\n'
  # prompt += 'What is the name for a 5-sided polygon?,multiple-choice,Hexagon,Pentagon,2,"A pentagon has five sides. Squares have four sides, hexagons have six.",Geometry\n'
  # prompt += 'Which of the following are woodwind instruments?,multi-select,Oboe,Trumpet,Flute,"1,3","Expanation is that it is just like that",Music\n'
  # prompt += 'What is the atomic symbol for Gold?,multiple-choice,Go,Gd,Ag,4,"The atomic symbol for the element Gold is Au",Chemistry\n'
  prompt += 'The latex beamer section of the presentation is here: ' + inputContent

  print('Calling ', MODEL, ' for creating quiz for section')
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
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5
  )
  print("Estimated token length of output:", tg_tools.estimate_token_length(completion.choices[0].message.content))
  return completion.choices[0].message.content

def my_function(class_code):
  # Load tex file
  # Split file based on section
  # For each section create quiz using LLM
  # combine the quizzes all into a single file and write out

  class_name = find_class_name(class_code)
  latex_file_name = os.path.join(COURSE_PATH, class_name, class_name + '.tex') 
  with open(latex_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

  output = 'Quiz generated for ' + class_name + '\n\n'

  # openai API setup
  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  print("Estimated token length of complete program input:", tg_tools.estimate_token_length(content))
  
  # call llm in chunks of text
  counter = 0
  sections = tg_tools.extract_sections_from_beamer_latex(content)
  for section in sections:
    section_name = section['section_name']
    section_content = section['section_content']
    print('Generating quiz for ', section_name)
    section_quiz = generate_quiz_for_section(section_content)
    output += f"************ SECTION: {section_name}\n{section_quiz}\n\n"

  #  print narrative to file
  quiz_file_name = os.path.join(COURSE_PATH, class_name, class_code + '_quiz' + '.txt')
  print('Writing to ', quiz_file_name)
  with open(quiz_file_name, 'a', encoding='utf-8') as file:
    file.write(output)
        
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python generate_quiz_based_on_latex.py <lecture 3 digit code as string>")
    sys.exit(1)

  class_code = sys.argv[1]
  my_function(class_code)
