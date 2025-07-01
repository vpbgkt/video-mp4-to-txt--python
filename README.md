🎥 MP4 Video to Text Transcription (Using Vosk Speech Recognition)
This project allows you to convert speech from any .mp4 video file into text using the Vosk offline speech recognition engine.

💡 Note: You will need to download the appropriate Vosk voice model for the language spoken in your video. These models are freely available online (just search for “vosk model [language]”).

🚀 Features
Extracts audio from .mp4 video files.

Converts audio to mono WAV format (compatible with Vosk).

Transcribes audio to text using the Vosk engine.

Saves the transcription as a .txt file in the same directory as the input video.

🔧 How It Works
1. Extract Audio from Video
The extract_audio_from_video() function uses moviepy to extract the audio track from the video and save it as a .wav file.

2. Convert Audio to Compatible Format
The convert_wav_to_required_format() function ensures the audio is:

Mono

16-bit PCM

Sampled at 16,000 Hz (default)

This formatting is necessary for accurate speech recognition with Vosk.

3. Transcribe Audio to Text
The audio_to_text() function:

Loads the Vosk model

Processes the audio in small chunks

Writes the recognized speech into a text file

4. Save the Transcription
The transcription is saved as transcription.txt in the same directory as your video file.

📦 Requirements
Make sure the following Python packages are installed:

bash
Copy
Edit
pip install moviepy vosk
Other standard libraries used:

wave

audioop

os, sys, json

📁 Setup & Usage
Download a Vosk model:

Go to the Vosk models page.

Choose a model based on your video’s language (e.g., vosk-model-en-in-0.5 for Indian English).

Unzip the model and note the directory path.

Run the Script:

When prompted, enter the folder path containing your .mp4 video.

The script will automatically detect the first .mp4 file in that directory.

text
Copy
Edit
Enter the folder path where the video file exists: /path/to/video
The script will:

Extract the audio

Convert it to the proper format

Transcribe it

Save the result as transcription.txt

🛠️ Troubleshooting
Missing Vosk Model: If the model path is incorrect or missing, the script will raise an error. Ensure the model is properly downloaded and the path is correctly set in the script.

Audio Format Issues: If the audio is not in mono, 16-bit PCM, and sampled at 8000 or 16000 Hz, the script will automatically attempt to convert it to the correct format.

📄 Example
bash
Copy
Edit
Enter the folder path where the video file exists: /Users/username/Videos
Output:

bash
Copy
Edit
transcription.txt saved successfully in /Users/username/Videos
📌 Notes
Only the first .mp4 file in the given folder will be processed.

This project is designed for offline usage and does not require an internet connection once the model is downloaded.

