# app.py
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

MODEL = "gpt-4o-2024-11-20"
# Process only these number of slides for testing. Set to 999 for all
NUM_SLIDES_PROCESSED = 999

# CLASS_NAME = '190 Value at Risk'
# MODEL = "gpt-4-1106-preview"
# PATH = 'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Capital Markets text book and course 2023\\Presentations 2.0\\' + CLASS_NAME + '\\'

def find_class_name(class_code: str) -> str:
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
            print('Class name ', folder, ' found.')
            return folder  # Return the first matching folder name
    
    # If no matching folder is found, return None
    print('Class not found: ', class_code);
    exit(-1)

def enhance_single_slide(inputContent: str, mode) -> str:
  if mode == "shorten":
    prompt = """Pay special attention to keep latex syntax correct and the same as before. 
    Do not add ```latex as it's somehow in the output.
    Only shorten wordings and keep meaning the same. 
    Generate a single valid LaTeX slide using begin frame and end frame. Ensure all environments are closed properly."""
  elif mode == "enhance":
    prompt = """You are a graduate school professor and an quantitative executive at an Investment Bank on the trading floor in New York.
    Enhance the slides but do not make content significantly longer or shorter and do not change meaning significatnly.
    Do not write full sentence and use grammar and style suitable for slides.
    Do not be verbose and keep writing style for a slide presentation.
    The slide and text you are given, is not the full latex document but only the frame part of a single slide.
    It's important you update only the frame part and do not add items like begin{document}, etc.
    The purpose of the class is to teach first year graduate students or new hires.
    Do not change the font boldness or font formating.
    After the generation double check that the latex is correct and if needed correct it.
    Do not add ```latex as it's somehow in the output.
    Generate a single valid LaTeX slide using begin frame and end frame syntax. Ensure all environments are closed properly.
    The wording should be excellent for a New York or London presentation to highly paid finance people and students."""
  else:
    raise ValueError("Invalid mode! Use 'shorten' or 'enhance'.")

  prompt += " The original slide is this: \n\n" + inputContent
    
  if INFO:
    print('Calling ', MODEL, ' for enhancing narration for new section')
    print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))
  if DEBUG:
     print('***************** Prompt Start *****************')
     print(prompt)
     print('***************** Prompt End *****************\n')

  # print('Calling ', MODEL, ' for enhancing slide')
  print("Estimated token length of input:", tg_tools.estimate_token_length(inputContent))

  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature = 0 if mode == "shorten" else tg_tools.GPT4_parameters.temperature,
    top_p = tg_tools.GPT4_parameters.top_p,
    frequency_penalty = tg_tools.GPT4_parameters.frequency_penalty_latex,
    presence_penalty = tg_tools.GPT4_parameters.presence_penalty,
    max_tokens = 1000
  )
  print("Estimated token length of output:", tg_tools.estimate_token_length(response.choices[0].message.content))
  return response.choices[0].message.content

def main(class_code, mode):

  class_name = find_class_name(class_code)

  inputFile = os.path.join(COURSE_PATH, class_name, class_name + '.tex') 
  baseName, extension = os.path.splitext(inputFile)
  outputfile = baseName + '_' + mode + extension
  insideSlide = False
  slideContent = ""
  enhancedSlideContent = ""
  newFileContent = ""
  num_slides = 0

  with open(inputFile, 'r', encoding='utf-8') as f:
    for line in f:
      if '\\begin{frame}' in line:
          insideSlide = True
          slideContent += line
          num_slides += 1
      elif '\\end{frame}' in line:
        slideContent += line
        print('Calling ' + MODEL + ' for slide ', num_slides)
        enhancedSlideContent = enhance_single_slide(slideContent, mode)
        # print(enhancedSlideContent)
        newFileContent += enhancedSlideContent + '\n'
        slideContent = ""
        insideSlide = False
      elif insideSlide:
        slideContent += line
      else:
        newFileContent += line
      if num_slides > NUM_SLIDES_PROCESSED:
        newFileContent += "\end{document}"
        break
  
  with open(outputfile, 'w', encoding='utf-8') as f:
    f.write(newFileContent)

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2].lower() not in ["shorten", "enhance"]:
        print("Usage: python enhance_slides_based_on_latex.py <lecture 3-digit code> <shorten/enhance>")
        sys.exit(1)

    class_code = sys.argv[1]
    mode = sys.argv[2].lower()  # Convert input to lowercase for consistency
    main(class_code, mode)

