https://deanofwalls.github.io/mneme/index.html

# Mneme

Mneme is a personal, local-first memory logging tool designed to seamlessly capture thoughts, ideas, and notes via voice, transcribe them to text, and push them to a GitHub repository for easy viewing and long-term storage. The project is inspired by the desire to offload short-term memory into a trusted external system, acting as an always-available personal memory assistant.

## Inspiration & Purpose

In an age of rapid information consumption and constant mental context-switching, short-term memory can often struggle to keep up. Mneme is built to solve a personal pain point: capturing fleeting thoughts before they are lost. 

Rather than relying on typing or manual note-taking, Mneme enables hands-free voice-based input through a hotword detection system, ensuring that spontaneous ideas can be quickly recorded without disrupting workflow.

Key goals of the project:
- Preserve thoughts effortlessly via voice capture
- Ensure privacy and ownership by processing everything locally
- Push transcriptions to a personal GitHub repository for cloud backup and easy access
- Display memories in a simple, clean, and terminal-inspired interface

## Technologies Used

Mneme is built on a collection of open-source tools and libraries, chosen for their efficiency, privacy, and compatibility with local-first development:

| Technology          | Purpose                                                   |
|---------------------|-----------------------------------------------------------|
| Python              | Core scripting and automation                             |
| Picovoice Porcupine | Local hotword detection (wake word) - https://picovoice.ai/products/porcupine/ |
| Sox                 | Voice recording with silence detection (VAD)              |
| Whisper.cpp         | OpenAI's Whisper transcription model, C++ GPU-optimized  |
| GitHub Pages        | Static hosting of transcribed memories                    |
| Shell scripting     | Automated HTML index generation                           |
| Fira Code Font      | Terminal-inspired monospaced font for clean readability   |

## Build Process

### 1. Environment Setup
- Create a Python virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install pvporcupine pyaudio
  ```

### 2. Hotword Detection
- Register and obtain a Picovoice Access Key from https://picovoice.ai/
- Download and place a `.ppn` hotword file in the project directory

### 3. Whisper.cpp
- Clone and build `whisper.cpp` locally:
  ```bash
  git clone https://github.com/ggerganov/whisper.cpp.git
  cd whisper.cpp
  mkdir build && cd build
  cmake ..
  cmake --build .
  ```
- Note: In newer versions, executables are found under `build/bin/` instead of `build/`
- Download a model (e.g., `ggml-base.bin`) into the `models` directory:
  ```bash
  cd models
  wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
  ```
- Common execution path for transcription looks like this:
  ```bash
  ./bin/whisper-cli -m ../models/ggml-base.bin -f <path-to-wav-file> --output-txt
  ```

### 4. Recording & Transcription
- `sox` is used for recording audio on VAD (voice-activity detection) settings
- Whisper transcribes the recorded `.wav` files into `.md` text files

### 5. Index Generation
- A shell script (`generate-index.sh`) compiles all `.md` files into a `index.html` log view
- Custom dark terminal-inspired styling via `style.css`

### 6. GitHub Pages Hosting
- Memory entries and the index are pushed to a public or private GitHub repository
- GitHub Pages serves the `index.html` for easy viewing

## Usage
1. Run `mneme_capture.py` to begin listening for the hotword
2. Say the hotword (e.g., 'sophia') followed by your thought
3. The recording is transcribed, converted to `.md`, and pushed to GitHub
4. View memories via the generated index on GitHub Pages

## Future Improvements
- Smarter VAD parameters for better silence detection
- Inline deletion of memories from the web interface
- Optional local-only mode for offline-first privacy
- Enhanced error handling and UI feedback during recording/transcription

