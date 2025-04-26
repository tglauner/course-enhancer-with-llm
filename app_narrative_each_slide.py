# app.py
import os
from dotenv import load_dotenv
import openai

CLASS_NAME = '025 Interest Rate Fundamentals'
MODEL = "gpt-4-1106-preview"

def narrativeForSlideWithAI(inputContent: str) -> str:
  prompt = "You are a graduate school professor and an quantitative executive at an Investment Bank on the trading floor in New York."
  prompt += "Based on the slide you are given you need to write down a narrative that the speaker can read when displaying the slides."
  prompt += "The speaker will present the slides while reading out load your narrative so it needs to be in sync."
  prompt += "The narrative should not sound like the speaker is just reading the slides."
  prompt += "Your narrative will be saved in a text file and given on a teleprompter to the speaker."
  prompt += "The original slides are: " + inputContent

  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=1,
#    max_tokens=4096,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response.choices[0].message.content

def my_function():
  load_dotenv()

  openai.api_key = os.getenv("OPENAI_API_KEY")

  path = "C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Capital Markets text book and course 2023\\Presentations\\"+CLASS_NAME+"\\"

  inputFile = os.path.join(path, CLASS_NAME + ".tex")
  baseName, extension = os.path.splitext(inputFile)

  insideSlide = False
  slideContent = ""
  narrative = ""
  num_slides = 0

  with open(inputFile, 'r') as f:
    for line in f:
      if '\\begin{frame}' in line:
          insideSlide = True
          slideContent += line
          num_slides += 1
          if num_slides > 5:
            break
      elif '\\end{frame}' in line:
        slideContent += line
        print("Calling ", MODEL, " for slide ", num_slides)
        narrative = narrativeForSlideWithAI(slideContent)
        print(narrative)
        output_file_name = os.path.join(path, "narr_" + CLASS_NAME + "_" + str(num_slides) + ".txt")
        print("Writing narrative to ", output_file_name)                                        
        with open(output_file_name, 'w') as output_file:
          output_file.write(narrative)
        slideContent = ""
        insideSlide = False
      elif insideSlide:
        slideContent += line
      else:
        print('Skipping line')
        
if __name__ == "__main__":
    my_function()
