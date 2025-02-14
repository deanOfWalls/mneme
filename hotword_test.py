import pvporcupine
import pyaudio
import struct

ACCESS_KEY = "WiX+NEu10KBTfIuE4T4WS1H6qIANSd8tXsiqVbmlbpO7KzpM1mTM2w=="

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=["/home/dean/Dev/mneme/Sophia_en_linux_v3_0_0.ppn"]
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
            print("Hotword detected!")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
