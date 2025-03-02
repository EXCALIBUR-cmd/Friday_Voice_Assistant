from faster_whisper import WhisperModel

# Download the 'tiny' model for CPU usage (offline)
model = WhisperModel("tiny", device="cpu")
print("Model downloaded successfully to the cache directory.")

#You can download models other than 'tiny', such as 'medium', 'base', 'large'
#but these models are larger in size and it takes time to download