# app.py
# Create narrative based on complete latex source code of lecture
# Pictures are not included and not seen to llm
import os
from dotenv import load_dotenv
import openai

CLASS_NAME = '025 Interest Rate Fundamentals'
MODEL = "gpt-4-1106-preview"
PATH = 'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Capital Markets text book and course 2023\\Presentations\\' + CLASS_NAME + '\\'
LECTURE_FILE_NAME = os.path.join(PATH, CLASS_NAME + '.tex')
OUTPUT_FILE_NAME = os.path.join(PATH, 'narr_using_latex_source_' + MODEL + '_' + CLASS_NAME + '.txt')
INPUT_STYLE_FILE_NAME = 'C:\\Users\\Dad\Dropbox\\2 - TG Investments and Research\\Projects\\LatexTemplatesAndSamples\\my_metropolis_style.sty'
INPUT_FIRST_FILE_NAME = 'C:\\Users\\Dad\Dropbox\\2 - TG Investments and Research\\Projects\\LatexTemplatesAndSamples\\firstThreeSlides.tex'
INPUT_LAST_FILE_NAME = 'C:\\Users\\Dad\Dropbox\\2 - TG Investments and Research\\Projects\\LatexTemplatesAndSamples\\lastSummarySlide.tex'
CONTENT_FILE_NAMES = [INPUT_STYLE_FILE_NAME, INPUT_FIRST_FILE_NAME, LECTURE_FILE_NAME, INPUT_LAST_FILE_NAME]

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = 'You are a graduate school professor.'
#  prompt = 'You are a graduate school professor and an quantitative executive at an Investment Bank on the trading floor in New York.'
  prompt += 'The information you are given is latex source code of the presentation.'
  prompt += 'The latex presentation creates a separator slide for each section and subsection. Pay attention to this fact to get the slide numbers correct.'
  prompt += 'Based on each of the slide you are given you need to write down a narrative that the speaker can read when displaying the slides.'
  prompt += 'The presentation is a lecture and the narration that will be read by speaker'
  prompt += 'The narrative should not sound like the speaker is just reading the slides.'
  prompt += 'Your narrative will be saved in a text file and given on a teleprompter to the speaker.'
#  prompt += 'Structure the narrative so that for every slide there is something to say based on the points in the slides from top to bottom.'
  prompt += 'Be clear in the narrative what words belong to which slide inclduing numbering and frametitles'
 # prompt += 'Depending on the amount of content create narration for about 1.5 minutes per slide'
#  prompt += 'Length of presentation is about 1.5 minutes per slide but short slides obviously need very brief narrative.'
  prompt += 'Thre are about 20 slides and your content for each slide should be about 250 words'
  prompt += 'Also write into the text at the end of narration of each slide how many words you created for the slide'
  prompt += 'The latex source code is: ' + inputContent

  print('Calling ', MODEL, ' for creating narrative for complete lecture')

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

  return response.choices[0].message.content

def my_function():
  narrative = ''
  content = ''

  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  # load content
  for file_name in CONTENT_FILE_NAMES:
    with open(file_name, 'r', encoding='utf-8') as file:
      print('Loading ', file_name)
      content += file.read()

  # call llm
  narrative = narrativeForSlideWithAI(content)

#  print narrative to file
  print('Writing narrative to ', OUTPUT_FILE_NAME)
  with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
      file.write(narrative)
        
if __name__ == '__main__':
    my_function()
