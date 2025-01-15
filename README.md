**Any language Mp4 Video to Text ( vox voice model is required as your video language, its free zip available on google )**
These scripts extracts audio from a video file, converts the audio into a compatible format, and transcribes it into text using the Vosk speech-to-text engine. Here's a breakdown of how it works:

Key Steps:
Extract Audio from Video:
The extract_audio_from_video() function uses moviepy to extract the audio from a video file and save it as a WAV file.

Convert Audio to Desired Format:
The convert_wav_to_required_format() function ensures the audio file is in mono and resampled to the desired sample rate (16,000 Hz by default), which is compatible with the Vosk recognizer.

Transcribe Audio to Text:
The audio_to_text() function loads the Vosk model, processes the WAV audio file, and transcribes it to text by reading the audio in small chunks.

Save the Transcription:
The transcription is saved as a .txt file in the same folder as the input video.

How to Use:
Folder Path Input: The user is asked to input the path where the video file is stored.
Model Path: Ensure that the path to the Vosk model is correct and the model files are available on your system. In this case, it uses the vosk-model-en-in-0.5 model.
Video File: The script assumes the video file is in .mp4 format, and it will process the first .mp4 file it finds in the specified folder.
Required Libraries:
**Make sure you have the following libraries installed:**
**Download Vox model from official site, with your suitable language of video,** 
moviepy: For video processing and audio extraction.
vosk: For speech recognition (make sure to install the Vosk Python package and download the Vosk model).
wave, audioop: For handling and processing audio files.
You can install the necessary Python libraries with:


pip install moviepy vosk
Example Execution:
When running the script, it will prompt for a folder path:


Enter the folder path where the video file exists: /path/to/video
The script will extract the audio, convert it to the correct format, transcribe the speech, and save the transcription as transcription.txt in the same folder.

Troubleshooting:
**Missing Vosk Model: If the Vosk model path is incorrect** , the script will raise an error. Make sure the model is downloaded and accessible at the specified path.
Audio File Format: The WAV audio file must be mono, 16-bit PCM, and sampled at either 8000 or 16000 Hz. If the input doesn't meet these criteria, the script will attempt to convert it.
