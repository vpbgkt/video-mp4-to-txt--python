import wave
import audioop

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

# Example usage
input_audio = "video2/audio.wav"  # Input WAV file
output_audio = "video2/converted_audio.wav"   # Output WAV file
convert_wav_to_required_format(input_audio, output_audio)

# Use `output_audio` in your Vosk script
