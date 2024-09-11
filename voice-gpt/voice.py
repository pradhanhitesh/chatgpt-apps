import pyaudio
import wave
import numpy as np
import time
import json
from openai import OpenAI
from config import api_key
import pandas as pd
import json
import datetime
import pytz
import time
import os

# Set OpenAI key
client = OpenAI(api_key=api_key)

# Set default parameters
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 2  # Number of audio channels (stereo)
RATE = 44100  # Sample rate (samples per second)
SILENCE_DURATION = 3  # Duration (seconds) of silence before stopping recording
WAVE_OUTPUT_FILENAME = "voice.wav"
conversation = {}  # Store conversations with timestamps

# Initialize PyAudio
p = pyaudio.PyAudio()

# Fetch time
def fetch_time():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    format_time = current_time.strftime("%Y-%m-%d-%H:%M:%S")

    return format_time
    
# Function to get ambient noise level for threshold adjustment
def get_ambient_noise_level(stream, num_chunks=50):
    noise_levels = []
    for _ in range(num_chunks):
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        noise_levels.append(np.linalg.norm(audio_data))
    return np.mean(noise_levels)

# Function to record audio and save it as a .wav file
def record_audio():
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("* adjusting for ambient noise...")

    ambient_noise_level = get_ambient_noise_level(stream)
    SILENCE_THRESHOLD = ambient_noise_level * 2.5
    # print(f"* Ambient noise level: {ambient_noise_level}, Silence threshold: {SILENCE_THRESHOLD}")
    
    print("* recording")
    frames = []
    silent_chunks = 0  # Counter for silent chunks
    max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)  # Number of chunks representing 5 seconds of silence

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert the data to numpy array to analyze volume levels
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.linalg.norm(audio_data)

        if volume < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0  # Reset if sound is detected

        # Stop recording if silence has been detected for long enough
        if silent_chunks > max_silent_chunks:
            # print("* silence detected, stopping recording")
            break

    # print("* done recording")
    # print(fetch_time())

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to transcribe the audio using OpenAI Whisper API
def transcribe_audio():
    print("* transcribing")
    audio_file = open(WAVE_OUTPUT_FILENAME, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    transcript_text = transcription.text
    conversation[fetch_time()] = transcript_text
    
    # print("* transcription complete")
    # print(fetch_time(), transcript_text)
    return transcript_text

# Function to generate response using GPT-4 and update the conversation history
def generate_response():
    # print("* generating response")
    # print(fetch_time())

    # Create system and user message prompts
    system_prompt = {
        "role": "system",
        "content": "You are a real-time voice assistant. Analyze the user input and give a relevant, prompt answer."
    }
    
    user_input = json.dumps(conversation)
    user_message = {
        "role": "user",
        "content": user_input
    }

    # Get response from GPT model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_prompt, user_message],
        temperature=0.7
    )

    response_content = response.choices[0].message.content
    # print(response_content)
    conversation[fetch_time()] = response_content  # Store response in conversation history
    # print(fetch_time())
    return response_content


while True:
    # print("Start speaking...")
    record_audio()
    transcription = transcribe_audio()

    print("User:", transcription)
    if len(transcription) > 1:
        response = generate_response()
        print("Assistant:", response)
        time.sleep(3)

        # Automatically restart the loop to continue the conversation
        # print("Listening for the next input...")
        
    else:
        print("ChatGPT Assistant Terminated")
        break

# Convert and write JSON object to file
with open("conversation.json", "w") as outfile: 
    json.dump(conversation, outfile)