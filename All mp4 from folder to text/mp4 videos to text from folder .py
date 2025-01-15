import os
import wave
import audioop
from moviepy import VideoFileClip
from vosk import Model, KaldiRecognizer

def extract_audio_from_video(video_path, audio_path):
    # Load the video
    video = VideoFileClip(video_path)
    # Extract audio from the video
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"Audio extracted and saved to: {audio_path}")

def convert_wav_to_required_format(input_path, output_path, target_rate=16000):
    # Open the input WAV file
    with wave.open(input_path, 'rb') as infile:
        # Check the input audio properties
        n_channels = infile.getnchannels()
        sample_width = infile.getsampwidth()
        frame_rate = infile.getframerate()
        n_frames = infile.getnframes()
        
        # Read the audio frames
        audio_data = infile.readframes(n_frames)
        
        # Convert to mono if necessary
        if n_channels > 1:
            audio_data = audioop.tomono(audio_data, sample_width, 0.5, 0.5)
        
        # Resample if necessary
        if frame_rate != target_rate:
            audio_data, _ = audioop.ratecv(audio_data, sample_width, 1, frame_rate, target_rate, None)
        
        # Write the output WAV file
        with wave.open(output_path, 'wb') as outfile:
            outfile.setnchannels(1)  # Mono
            outfile.setsampwidth(sample_width)
            outfile.setframerate(target_rate)
            outfile.writeframes(audio_data)
    
    print(f"Converted audio saved to: {output_path}")

def audio_to_text(audio_path, model_path):
    # Check if the model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # Load the Vosk model
    model = Model(model_path)

    # Open the audio file
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            raise ValueError("Audio file must be WAV format mono PCM with a sample rate of 8000 or 16000 Hz")

        recognizer = KaldiRecognizer(model, wf.getframerate())

        # Process audio and convert to text
        result_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_text += eval(result).get("text", "") + " "

        # Add final partial result if any
        final_result = recognizer.FinalResult()
        result_text += eval(final_result).get("text", "")

    return result_text.strip()

def process_videos(folder_path, output_base_folder):
    # Create the base data folder if it doesn't exist
    data_folder = os.path.join(output_base_folder, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Get all video files (assuming they are .mp4)
    video_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    if not video_files:
        print("No video files found in the folder.")
        return

    # Process each video file
    for video_file in video_files:
        video_file_path = os.path.join(folder_path, video_file)

        # Step 1: Extract audio from video
        audio_path = os.path.join(folder_path, "audio.wav")
        extract_audio_from_video(video_file_path, audio_path)

        # Step 2: Convert audio to required format
        converted_audio_path = os.path.join(folder_path, "converted_audio.wav")
        convert_wav_to_required_format(audio_path, converted_audio_path)

        # Step 3: Transcribe audio to text
        vosk_model_path = "vosk-model-en-in-0.5"  # Ensure this path points to your Vosk model
        try:
            text = audio_to_text(converted_audio_path, vosk_model_path)
            print(f"Transcription completed for {video_file}")
            
            # Step 4: Create a folder for the video inside 'data' and save the transcription
            video_data_folder = os.path.join(data_folder, os.path.splitext(video_file)[0])
            if not os.path.exists(video_data_folder):
                os.makedirs(video_data_folder)
            
            text_file_path = os.path.join(video_data_folder, "transcription.txt")
            with open(text_file_path, "w") as text_file:
                text_file.write(text)
            print(f"Transcription saved to: {text_file_path}")
        
        except Exception as e:
            print(f"Error processing {video_file}: {e}")

def main():
    folder_path = input("Enter the folder path containing the video files: ").strip()
    output_base_folder = folder_path  # You can change this to a different output folder if needed
    
    process_videos(folder_path, output_base_folder)

if __name__ == "__main__":
    main()
