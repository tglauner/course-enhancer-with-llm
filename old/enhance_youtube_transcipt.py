# enhance_youtube_transcipt.py

# Creates narrative based on youtube transcipt
# With newest model the token restrictions can be removed
import os, sys
from dotenv import load_dotenv
import openai
import tg_tools

CLASS_NAME = '190 Value at Risk 2.0' # Modify for new lecture
PATH = (
  'C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\'
  'Capital Markets text book and course 2023\\Presentations 2.0\\' + CLASS_NAME + '\\'
)
TRANSCIPT_FILE_NAME = os.path.join(PATH, '190_transcript_youtube_1_43.txt') # Modify for new lecture
OUTPUT_FILE_NAME = os.path.join(PATH, '190_narration_1_43.txt') # Modify for new lecture
MODEL = "gpt-4-turbo"
CONTENT_FILE_NAMES = [TRANSCIPT_FILE_NAME]
MAX_TOKENS = 1200

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = (
      "You are a graduate school professor. "
      "Create a new transcript based on the transcript you are given. "
      "Maintain the length and sequence of the transcript as closely as possible. "
      "Remove all the time stamps. "
      "Ensure excellent grammar with correct punctuations and pauses for the speaker. "
      "Fix mostly wording, grammar, and style but do not change the functional statements. "
      "Create reasonable paragraphs but do not change the sequence of the thoughts. "
      "Avoid very long sentences run on sentences even if the original transcript has them."
      "The original transcript is here: " + inputContent) 

  print('Calling ', MODEL, ' for creating narrative for complete lecture')
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

def main():
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
    #if (counter := counter + 1) > 1: break

#  narrative = narrativeForSlideWithAI(content)

#  print narrative to file
  print("Estimated token length of complete output:", tg_tools.estimate_token_length(narrative))
  print('Writing narrative to ', OUTPUT_FILE_NAME)
  with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
      file.write(narrative)
        
if __name__ == '__main__':
  if len(sys.argv) != 1:
    print("Usage: python enhance_youtube_transcipt.py")
    sys.exit(1)
  main()
