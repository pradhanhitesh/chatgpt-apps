# Import required packages
from openai import OpenAI
from config import api_key
import pandas as pd
import json
import datetime
import pytz

# Initialize OpenAI client with the provided API key
client = OpenAI(api_key=api_key)

def fetch_time():
    """
    Fetches the current date and time in the 'Asia/Kolkata' timezone.
    
    Returns:
        str: The current time in the format 'YYYY-MM-DD-HH:MM:SS'.
    """
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    format_time = current_time.strftime("%Y-%m-%d-%H:%M:%S")
    return format_time

# Load the data from a CSV file
# Ensure that the path is updated to the correct file path
data = pd.read_excel("/path/to/the/csv/file/.csv")

# Extract 'Comments' and 'SubID' columns into separate lists
comments = list(data['Comments'])  # List of comments from the CSV file
sub_id = list(data['SubID'])  # List of corresponding subject IDs

# Define batch size for processing
batch_size = 100

for i in range(0, len(comments), batch_size):
    batch_comments = comments[i:i + batch_size]
    batch_subs = sub_id[i:i + batch_size]

    batch_json = {}
    for k in range(len(batch_comments)):
        batch_json[str(batch_subs[k])] = batch_comments[k]

    print(f"Batch no: {i} started at: {fetch_time()}")

    # Create a system message asking GPT to return output as JSON
    system_prompt = {
        "role": "system",
        "content": "You are a JSON processing assistant.  "
        "Use this format to save the response for each value in the user's JSON input: "
        "{ 'subject-id' : 'this should state the key associated with value in the JSON input.', "
        "'findings' : 'this is where the comments are put with proper formatting, remove any dead space, commas, typeset the comments as well.', "
        " 'type' : 'this is where you classify the comment as normal/abnormal.' , "
        " 'location' : 'this is where you extract the location if mentioned any in the comment. If normal study of the brain, write 'not applicable' ' ,"
        " 'likely cause' : 'this is where you mention the likely cause if mentioned any in the comment. If normal study of the brain, write 'not applicable''}"
        "Accept input in JSON format and return the output in valid JSON format without '''json tag."
    }

    # Convert the batch data to a JSON string (optional for clarity)
    user_input = json.dumps(batch_json)

    # Create a user message containing the JSON input
    user_message = {
        "role": "user",
        "content": user_input
    }

    # Send the request to the OpenAI API with the system and user prompts
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Model used for processing
        messages=[system_prompt, user_message],  # Messages for the API
        temperature=0.7  # Controls randomness of the response
    )

    # Extract the response content, which is expected to be in JSON format
    response_content = response.choices[0].message.content

    # Parse the response content back into a Python dictionary
    response_json = json.loads(response_content)

    # Save the response as a JSON file with the batch number in the filename
    with open('output_' + str(i) + '.json', 'w') as json_file:
        json.dump(response_json, json_file, indent=4)  # Save with indentation for readability