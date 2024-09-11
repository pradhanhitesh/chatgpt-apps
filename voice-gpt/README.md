<h1>Real-time Voice Assistant with GPT and Whisper</h1>

This project implements a real-time voice assistant using OpenAI's Whisper API for audio transcription and GPT-4 for generating responses. It allows users to speak into a microphone, transcribe the audio in real time, and receive an intelligent response from GPT. The conversation history is stored in a JSON file.

<h2>Features</h2>

1. Real-time Voice Recording: Records user input through the microphone and stops when silence is detected.
2. Automatic Transcription: Uses OpenAI Whisper API to transcribe the recorded audio into text.
3. Response Generation: Utilizes OpenAI GPT-4 to generate contextually relevant responses to the transcribed text.
4. Conversation Logging: Stores the conversation history with timestamps in a JSON file.

<h2>Requirements</h2>

1. Python 3.8+
2. pyaudio
3. wave
4. numpy
5. pytz
6. datetime
7. OpenAI Python SDK

<h2>Customization</h2>

1. Adjusting Silence Threshold: You can modify the silence detection behavior by changing the SILENCE_DURATION and SILENCE_THRESHOLD values in the voice.py file:

2. System Prompts for GPT: The GPT response is based on a system prompt that can be customized

```
system_prompt = {
    "role": "system",
    "content": "You are a real-time voice assistant. Analyze the user input and give a relevant, prompt answer."
}
```

3. Batch Size for Audio Processing: The script processes audio in chunks of CHUNK = 1024 frames. You can adjust the chunk size or other audio parameters if needed.

<h2>Issues (dated 11-09-2024)</h2>

1. Ambient noise threshold variability
2. Extracting text from silent audio: Should not happen if the recorded audio is pure silence

<h2>License</h2>
This project is licensed under the MIT License. See the LICENSE file for more details.
