# analyze_text.py
# Create 10 most important points based on youtube transcipt
import os
from dotenv import load_dotenv
import openai
import tg_tools

CLASS_NAME = '040 Interest Rate Financial Instruments and Derivatives' # Modify for new lecture
PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Making Inv Banker Analysis\\'
)
TRANSCIPT_FILE_NAME = os.path.join(PATH, 'youtube_transcript.txt') # Modify for new lecture
OUTPUT_FILE_NAME = os.path.join(PATH, 'youtube_transcript_analysis.txt') # Modify for new lecture
MODEL = "gpt-4-1106-preview"
CONTENT_FILE_NAMES = [TRANSCIPT_FILE_NAME]
MAX_TOKENS = 3000

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = 'Analyze this text and give the ten most important points'
  prompt += 'The text is here: ' + inputContent

  print('Calling ', MODEL, ' for analyzing text')
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

def my_function():
  narrative = ''
  segment_narrative = ''
  content = ''

  load_dotenv()
  openai.api_key = os.getenv('OPENAI_API_KEY')

  # load content
  for file_name in CONTENT_FILE_NAMES:
    with open(file_name, 'r', encoding='utf-8') as file:
      print('Loading ', file_name)
      content += file.read()

  print("Estimated token length of complete input:", tg_tools.estimate_token_length(content))

  # call llm in chunks of text
  counter = 0
  segments = tg_tools.split_text_by_tokens(content, MAX_TOKENS)
  for segment in segments:
    segment_narrative = narrativeForSlideWithAI(segment)
    narrative += segment_narrative
#    if (counter := counter + 1) > 1: break

#  print narrative to file
  print("Estimated token length of complete output:", tg_tools.estimate_token_length(narrative))
  print('Writing output to ', OUTPUT_FILE_NAME)
  with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
      file.write(narrative)
        
if __name__ == '__main__':
    my_function()
