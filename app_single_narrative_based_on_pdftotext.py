# app.py
import os
from dotenv import load_dotenv
import openai

className = '025 Interest Rate Fundamentals'
#once = True
MODEL = "gpt-4-1106-preview"

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = 'You are a graduate school professor and an quantitative executive at an Investment Bank on the trading floor in New York.'
  prompt += 'The information you are given is latex source code of the presentation. The presentation is shown to the audience and you need to generate narration that will be read by speaker'
  prompt += 'The repeated info in the text should be ignored as these are headers.'
  prompt += 'The speaker will present the slides while reading out load your narrative so it needs to be in sync.'
  prompt += 'The narrative should not sound like the speaker is just reading the slides.'
  prompt += 'Your narrative will be saved in a text file and given on a teleprompter to the speaker.'
#  prompt += 'Structure the narrative so that for every slide there is something to say based on the points in the slides from top to bottom.'
  prompt += 'Be clear in the narrative what words belong to which slide inclduing numbering and frametitles'
  prompt += 'Length of presentation is 1.5 minutes per slide.'
  prompt += 'The latex source code is: ' + inputContent

  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  print('OpenAI model called: ', openai.Model)
  return response.choices[0].message.content

def my_function():
  load_dotenv()

  openai.api_key = os.getenv('OPENAI_API_KEY')

  path = 'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Capital Markets text book and course 2023\\Presentations\\'+className+'\\'
  input_file_name = 'pdf_converted_to_text.txt'
  print('Input file name: ', input_file_name)
  input_file = os.path.join(path, input_file_name)
  print('Input file name with path: ', input_file)
  narrative = ''
  
  with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()
    narrative = narrativeForSlideWithAI(content)
    output_file_name = os.path.join(path, 'narr_all_source_pdftotext_' + MODEL + '_' + className + '.txt')
    print('Writing narrative to ', output_file_name)                                        
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
      output_file.write(narrative)
        
if __name__ == '__main__':
    my_function()
