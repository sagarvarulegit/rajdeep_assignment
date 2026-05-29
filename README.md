# FYISC - Angle and its Measurement

A premium animated educational video series presenting the chapter **"Angle and its Measurement"** from the FYISC syllabus. 

This project uses **Manim** (Mathematical Animation Engine) for visual geometry renderings and **ElevenLabs TTS API** for high-quality, professional narration (using a custom cloned voice `FYISC Teacher`).

---

## 📽️ Project Overview

The project is structured into two main parts:
1. **Topic Explanation (`explain_angles.py`)**: Covers the conceptual foundations, definitions, measurement systems, and formulas.
2. **Exercise Solutions (`exercise_one_solutions.py`)**: Step-by-step visual solutions for all 20 questions in Exercise 1.

---

## 🗂️ Directory Structure

```
angles_its_measurement/
├── explain_angles.py              # Source code for the topic explanation scenes
├── exercise_one_solutions.py      # Source code for the exercise solutions (Q1 - Q20)
├── align_voiceovers.py            # Script to align & mux voiceovers with Manim videos
├── render_all.py                  # Automation script to render & align all scenes
├── FYISC - Angle and it's Measurement.pdf # Syllabus worksheet reference
├── youtube_questions_transcript.txt # Transcript of exercise question details
├── youtube_raw_transcript.txt      # Raw lecture reference transcript
├── voiceovers/                     # Contains subtitle timings and cached audios
└── final_videos/                  # Output directory for final video files (MP4)
```

---

## 🚀 Getting Started

### 📋 Prerequisites
Make sure you have python and the following dependencies installed:
```bash
pip install manim edge-tts gTTS
```
*Note: FFmpeg and FFprobe must also be installed and available on your system path.*

### 🎙️ ElevenLabs Configuration
By default, the scripts look for your ElevenLabs API Key in the environment variable `ELEVENLABS_API_KEY`. If not set, it defaults to the configured API key and uses the cloned voice ID `Ij5WqlrmfRUJMb1TYRFl` (`FYISC Teacher`).

### 🏃 Rendering and Aligning Videos
To render and align all scenes automatically, run the helper script:
```bash
python render_all.py
```

To run a specific scene (e.g., `Q13Scene`):
```bash
python render_all.py --scene Q13Scene
```
This will:
1. Run Manim to generate the raw video segments and dynamic subtitle timing logs.
2. Generate voiceover files using ElevenLabs.
3. Automatically align the voiceovers with the video using FFmpeg.
4. Export the completed video to the `final_videos/` directory.
