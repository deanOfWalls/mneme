import pvporcupine
import pyaudio
import struct
import subprocess
from datetime import datetime
import os

ACCESS_KEY = "WiX+NEu10KBTfIuE4T4WS1H6qIANSd8tXsiqVbmlbpO7KzpM1mTM2w=="
KEYWORD_PATH = "/home/dean/Dev/mneme/Sophia_en_linux_v3_0_0.ppn"
MEMORIES_DIR = "/home/dean/Dev/mneme/memories"
WHISPER_CPP_DIR = "/home/dean/Dev/mneme/whisper.cpp/build/bin"
MODEL_PATH = "/home/dean/Dev/mneme/whisper.cpp/models/ggml-base.bin"
GENERATE_INDEX_SCRIPT = "/home/dean/Dev/mneme/generate-index.sh"


def record_memory():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    wav_path = os.path.join(MEMORIES_DIR, f"{timestamp}.wav")

    print(f"[INFO] Recording memory to: {wav_path}")

    record_process = subprocess.Popen([
        "sox", "-t", "alsa", "default", "-r", "16000", "-c", "1", "-b", "16", wav_path,
        "silence", "1", "0.1", "1%", "1", "1.0", "1%"
    ])

    try:
        record_process.wait()
        print(f"[SUCCESS] Memory recorded to: {wav_path}")
        process_memory(wav_path)
    except KeyboardInterrupt:
        record_process.terminate()
        print("[INFO] Recording interrupted.")


def process_memory(wav_path):
    base_filename = os.path.splitext(os.path.basename(wav_path))[0]
    md_path = os.path.join(MEMORIES_DIR, f"{base_filename}.md")

    resampled_wav_path = wav_path.replace(".wav", "_16k.wav")
    subprocess.run([
        "sox", wav_path, "-r", "16000", "-c", "1", "-b", "16", resampled_wav_path
    ], check=True)

    result = subprocess.run(
        [
            os.path.join(WHISPER_CPP_DIR, "whisper-cli"),
            "-m", MODEL_PATH,
            "-f", resampled_wav_path,
            "--output-txt"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] Transcription failed for {resampled_wav_path}: {result.stderr}")
        return

    transcript_path = f"{resampled_wav_path}.txt"

    if os.path.exists(transcript_path):
        with open(transcript_path, "r") as f:
            transcript = f.read().strip()

        with open(md_path, "w") as f:
            f.write(f"# Mneme Memory – {base_filename}\n\n")
            f.write(transcript)

        # Check if transcription is empty (after trimming whitespace)
        if not transcript:
            print(f"[INFO] Empty memory detected, deleting: {md_path}")
            os.remove(md_path)
        else:
            os.remove(wav_path)
            os.remove(resampled_wav_path)
            os.remove(transcript_path)

            print(f"[SUCCESS] Transcribed and saved memory to: {md_path}")
            push_memory(md_path)


def push_memory(md_path):
    # Generate index.html locally
    subprocess.run(["bash", GENERATE_INDEX_SCRIPT], check=True)

    # Stage the .md and the index.html
    subprocess.run(["git", "-C", MEMORIES_DIR, "add", md_path], check=True)
    subprocess.run(["git", "-C", MEMORIES_DIR, "add", "../index.html"], check=True)

    # Commit and push
    subprocess.run(["git", "-C", MEMORIES_DIR, "commit", "-m", f"Add memory {os.path.basename(md_path)} and update index"], check=True)
    subprocess.run(["git", "-C", MEMORIES_DIR, "push", "origin", "master"], check=True)

    print(f"[SUCCESS] Pushed {md_path} and index.html to GitHub.")


def main():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("[INFO] Listening for 'sophia' hotword...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result >= 0:
                print("[SUCCESS] Hotword detected!")
                record_memory()

    except KeyboardInterrupt:
        print("[INFO] Stopping hotword detection...")

    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    main()
