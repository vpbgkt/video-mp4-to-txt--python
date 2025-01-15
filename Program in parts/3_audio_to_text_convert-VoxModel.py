import os
import wave
from vosk import Model, KaldiRecognizer



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

if __name__ == "__main__":
    audio_file = "video2/converted_audio.wav"  # Replace with the path to your audio file
    vosk_model_path = "vosk-model-en-in-0.5"  # Replace with the path to your Vosk model

    try:
        text = audio_to_text(audio_file, vosk_model_path)
        print("Transcription:")
        print(text)
    except Exception as e:
        print(f"Error: {e}")
