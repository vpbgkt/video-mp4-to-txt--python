import imageio
from moviepy import VideoFileClip

# Load the video
video = VideoFileClip("video2/19 NOVEMBER Youtube Adityaveer CAT Common Aptitute Test.mp4")

# Extract audio from the video
audio = video.audio
audio.write_audiofile("video2/audio.wav")  # Save the audio as a WAV file
