# app.py
import os
from dotenv import load_dotenv
import openai

className = "270 Federal Home Loan Banks - FHLB"
#once = True

def enhanceSlideWithAI(inputContent: str) -> str:
  prompt = "You are a graduate school professor and an quantitative executive at an Investment Bank on the trading floor in New York."
  prompt += "Enhance the slides but do not make content significantly longer or shorter."
  prompt += "Do not write full sentence but keep style for slides"
  prompt += "Do not be verbose and keep writing style for a slide presentation."
  prompt += "Even if you write a full sentence do not end a line with a period."
  prompt += "The slide and text you are given, is not the full latex document but only the frame part."
  prompt += "Please update only frame part and do not add items like begin{document}, etc."
  prompt += "Create complete latex text that does not require any post processing."
  prompt += "The purpose of the class is to teach first year graduate students or new hires."

  # global once
  # if once:
  #   once = False
  #   print("Prompt**************************************************************\n", prompt)

  prompt += "The original slide is this: " + inputContent

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
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

  path = "C:\\Users\\Dad\\Dropbox\\2 - TG Investments and Research\\Projects\\Capital Markets text book and course 2023\\Presentations\\"+className+"\\"

  inputFile = os.path.join(path, className + ".tex")
  baseName, extension = os.path.splitext(inputFile)
  outputfile = baseName + "_V1" + extension
  insideSlide = False
  slideContent = ""
  enhancedSlideContent = ""
  newFileContent = ""
  num_slides = 0

  with open(inputFile, 'r') as f:
    for line in f:
      if '\\begin{frame}' in line:
          insideSlide = True
          slideContent += line
          num_slides += 1
      elif '\\end{frame}' in line:
        slideContent += line
        print("Calling gpt-3.5-turbo for slide ", num_slides)
        enhancedSlideContent = enhanceSlideWithAI(slideContent)
        print(enhancedSlideContent)
        newFileContent += enhancedSlideContent + '\n'
        slideContent = ""
        insideSlide = False
      elif insideSlide:
        slideContent += line
      else:
        newFileContent += line
  
  with open(outputfile, 'w') as f:
    f.write(newFileContent)





# with open(courseContent+'V1') as outputFile:
#     outputFile.write(response.choices[0].message.content)

# 6. Main execution script
if __name__ == "__main__":
    my_function()
