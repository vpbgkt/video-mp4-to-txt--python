import os
import wave
import audioop
from moviepy import VideoFileClip
from vosk import Model, KaldiRecognizer

def extract_audio_from_video(video_path, audio_path):
    """
    Extracts audio from a given video file and saves it as a WAV file.

    Parameters:
    video_path (str): Path to the input video file.
    audio_path (str): Path to save the extracted audio file.

    Returns:
    None
    """
    # Load the video file using moviepy
    video = VideoFileClip(video_path)
    # Extract the audio from the video
    audio = video.audio
    # Save the extracted audio as a WAV file
    audio.write_audiofile(audio_path)
    print(f"Audio extracted and saved to: {audio_path}")

def convert_wav_to_required_format(input_path, output_path, target_rate=16000):
    """
    Converts the input WAV audio file to mono and resamples it to the target sample rate.

    Parameters:
    input_path (str): Path to the input WAV audio file.
    output_path (str): Path to save the converted audio file.
    target_rate (int): The desired sample rate for the output audio (default is 16000 Hz).

    Returns:
    None
    """
    # Open the input WAV file for reading
    with wave.open(input_path, 'rb') as infile:
        # Extract properties of the audio file
        n_channels = infile.getnchannels()
        sample_width = infile.getsampwidth()
        frame_rate = infile.getframerate()
        n_frames = infile.getnframes()
        
        # Read all frames from the audio file
        audio_data = infile.readframes(n_frames)
        
        # Convert audio to mono if it has more than 1 channel
        if n_channels > 1:
            audio_data = audioop.tomono(audio_data, sample_width, 0.5, 0.5)
        
        # Resample the audio if the frame rate is not equal to the target rate
        if frame_rate != target_rate:
            audio_data, _ = audioop.ratecv(audio_data, sample_width, 1, frame_rate, target_rate, None)
        
        # Write the converted audio to the output WAV file
        with wave.open(output_path, 'wb') as outfile:
            outfile.setnchannels(1)  # Mono
            outfile.setsampwidth(sample_width)
            outfile.setframerate(target_rate)
            outfile.writeframes(audio_data)
    
    print(f"Converted audio saved to: {output_path}")

def audio_to_text(audio_path, model_path):
    """
    Converts the speech from an audio file to text using the Vosk speech-to-text model.

    Parameters:
    audio_path (str): Path to the WAV audio file for transcription.
    model_path (str): Path to the Vosk speech-to-text model.

    Returns:
    str: The transcribed text.
    """
    # Check if the Vosk model exists at the provided path
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # Load the Vosk model
    model = Model(model_path)

    # Open the audio file for reading
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            raise ValueError("Audio file must be WAV format mono PCM with a sample rate of 8000 or 16000 Hz")

        recognizer = KaldiRecognizer(model, wf.getframerate())

        # Process audio in small chunks and collect the transcribed text
        result_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_text += eval(result).get("text", "") + " "

        # Add the final partial result if any
        final_result = recognizer.FinalResult()
        result_text += eval(final_result).get("text", "")

    return result_text.strip()

def main():
    """
    Main function to extract audio from video, convert it to a required format, transcribe it to text,
    and save the transcription to a file.
    """
    # Ask for the video file path
    video_path = input("Enter the path to the video file (e.g., /path/to/video.mp4): ").strip()

    # Check if the video file exists
    if not os.path.exists(video_path):
        print("Error: Video file does not exist.")
        return

    # Step 1: Extract audio from the video file
    audio_path = os.path.splitext(video_path)[0] + "_audio.wav"
    extract_audio_from_video(video_path, audio_path)

    # Step 2: Convert the extracted audio to the required format (mono, 16kHz)
    converted_audio_path = os.path.splitext(video_path)[0] + "_converted_audio.wav"
    convert_wav_to_required_format(audio_path, converted_audio_path)

    # Step 3: Transcribe the audio to text using the Vosk model
    vosk_model_path = "vosk-model-en-in-0.5"  # Update this with the correct path to your Vosk model
    try:
        text = audio_to_text(converted_audio_path, vosk_model_path)
        print("Transcription completed.")
        
        # Step 4: Save the transcription to a text file
        text_file_path = os.path.splitext(video_path)[0] + "_transcription.txt"
        with open(text_file_path, "w") as text_file:
            text_file.write(text)
        print(f"Transcription saved to: {text_file_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
