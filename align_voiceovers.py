import os
import json
import argparse
import subprocess

# Configuration
FFMPEG_PATH = r"C:\Users\sunwa\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
VOICEOVER_DIR = "voiceovers"
RAW_VIDEO_DIR = os.path.join("media", "videos", "exercise_one_solutions", "720p30")
OUTPUT_DIR = "final_videos"

def run_command(cmd):
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Command failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise RuntimeError(f"FFmpeg command failed with return code {result.returncode}")

def align_scene(scene_name):
    print(f"\n========================================")
    print(f"Aligning Scene: {scene_name}")
    print(f"========================================")
    
    json_path = os.path.join(VOICEOVER_DIR, f"{scene_name}_subtitles.json")
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found: {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        subtitles = json.load(f)
        
    if not subtitles:
        print(f"Warning: No subtitles found in {json_path}")
        return
        
    raw_video_path = os.path.join(RAW_VIDEO_DIR, f"{scene_name}.mp4")
    if not os.path.exists(raw_video_path):
        alt_path = os.path.join("media", "videos", "explain_angles", "720p30", f"{scene_name}.mp4")
        if os.path.exists(alt_path):
            raw_video_path = alt_path
        else:
            print(f"Error: Raw video not found: {raw_video_path} (also checked {alt_path})")
            return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    final_video_path = os.path.join(OUTPUT_DIR, f"{scene_name}_with_voiceover.mp4")
    
    # Step 1: Collect inputs and verify cached files exist
    inputs = ["-i", raw_video_path]
    snippet_files = []
    
    for idx, item in enumerate(subtitles):
        audio_path = item["audio_path"]
        time_offset = item["time"]
        
        if not os.path.exists(audio_path):
            print(f"Error: Cached audio file not found: {audio_path}")
            return
            
        inputs.extend(["-i", audio_path])
        snippet_files.append((audio_path, time_offset))
        
    # Step 2: Build FFmpeg filter complex
    filter_complex_parts = []
    # Build adelay filters
    for idx, (_, offset_sec) in enumerate(snippet_files):
        delay_ms = int(offset_sec * 1000)
        filter_complex_parts.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[a{idx}]")
        
    # Build amix filter
    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(snippet_files)))
    if len(snippet_files) > 1:
        filter_complex_parts.append(f"{mix_inputs}amix=inputs={len(snippet_files)}:duration=longest:dropout_transition=0[outa]")
    else:
        filter_complex_parts.append(f"[a0]anull[outa]")
        
    filter_complex_str = "; ".join(filter_complex_parts)
    
    # FFmpeg command
    cmd = [
        FFMPEG_PATH,
        "-y"
    ] + inputs + [
        "-filter_complex", filter_complex_str,
        "-map", "0:v",
        "-map", "[outa]",
        "-c:v", "copy",
        "-c:a", "aac",
        final_video_path
    ]
    
    print("Muxing audio and video using FFmpeg...")
    run_command(cmd)
    print(f"Successfully created: {final_video_path}")

def main():
    parser = argparse.ArgumentParser(description="Align cached voiceovers with Manim video subtitles using FFmpeg.")
    parser.add_argument("--scene", type=str, help="Specific scene name (e.g. Q1Scene) to align. If omitted, aligns all scenes with subtitle logs.")
    args = parser.parse_args()
    
    if args.scene:
        align_scene(args.scene)
    else:
        all_logs = [f for f in os.listdir(VOICEOVER_DIR) if f.endswith("_subtitles.json")]
        if not all_logs:
            print("No subtitle log files found in the voiceovers directory.")
            return
            
        for log in sorted(all_logs):
            scene_name = log.replace("_subtitles.json", "")
            try:
                align_scene(scene_name)
            except Exception as e:
                print(f"Failed to align {scene_name}: {e}")

if __name__ == "__main__":
    main()
