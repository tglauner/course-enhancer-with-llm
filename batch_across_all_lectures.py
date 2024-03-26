import json
import subprocess

# Load the JSON data from the file
with open('class_codes.json', 'r') as file:
    data = json.load(file)

# Loop over the elements and call app.py for each one
for element in data['elements']:
    # Construct the command to call app.py with the current element as an argument
    command = ['python', 'generate_quiz_based_on_latex.py', element]
    
    # Execute the command
    print('Executing ', command)
    subprocess.run(command)

