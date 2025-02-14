import pvporcupine
import pyaudio
import struct
import subprocess
import os
from datetime import datetime

ACCESS_KEY = "WiX+NEu10KBTfIuE4T4WS1H6qIANSd8tXsiqVbmlbpO7KzpM1mTM2w=="
PPN_PATH = "/home/dean/Dev/mneme/Sophia_en_linux_v3_0_0.ppn"
OUTPUT_DIR = "/home/dean/Dev/mneme/memories"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[PPN_PATH]
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for 'sophia' hotword...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Hotword detected! Starting recording...")

            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            wav_path = os.path.join(OUTPUT_DIR, f"{timestamp}.wav")

            # Start recording with sox using VAD (Voice Activity Detection)
            subprocess.run([
                "sox", "-t", "alsa", "default", wav_path,
                "silence", "1", "0.1", "1%", "1", "1.0", "1%"
            ])

            print(f"Recording saved to {wav_path}")

except KeyboardInterrupt:
    print("Stopping...")
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
