import os
import subprocess
import argparse

EXPLAIN_SCENES = [
    "TitleScene",
    "DirectedAngleScene",
    "StandardPositionScene",
    "MeasurementSystemsScene",
    "FormulasScene",
    "OutroScene"
]

EXERCISE_SCENES = [
    f"Q{i}Scene" for i in range(1, 21)
]

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Render and align all video scenes with premium voiceovers.")
    parser.add_argument("--type", choices=["explain", "exercises", "all"], default="all",
                        help="Which set of scenes to render: explain (explain_angles), exercises (exercise_one_solutions), or all (default).")
    parser.add_argument("--scene", type=str, help="Render a specific scene only.")
    args = parser.parse_args()

    # Determine scenes to run
    scenes_to_run = []
    if args.scene:
        if args.scene in EXPLAIN_SCENES:
            scenes_to_run.append(("explain_angles.py", args.scene))
        elif args.scene in EXERCISE_SCENES or args.scene == "Q13SceneWhiteboard":
            scenes_to_run.append(("exercise_one_solutions.py", args.scene))
        else:
            print(f"Error: Scene '{args.scene}' is not recognized.")
            return
    else:
        if args.type in ["explain", "all"]:
            for scene in EXPLAIN_SCENES:
                scenes_to_run.append(("explain_angles.py", scene))
        if args.type in ["exercises", "all"]:
            for scene in EXERCISE_SCENES:
                scenes_to_run.append(("exercise_one_solutions.py", scene))

    print(f"Found {len(scenes_to_run)} scenes to render.")
    
    # Render scenes
    for script_file, scene in scenes_to_run:
        print(f"\n========================================")
        print(f"Rendering {scene} from {script_file}")
        print(f"========================================")
        success = run_command(["python", "-m", "manim", "-qm", script_file, scene])
        if not success:
            print(f"Warning: Failed to render {scene}!")
            
    # Align scenes
    print("\n========================================")
    print("Aligning Voiceovers for all rendered scenes")
    print("========================================")
    
    if args.scene:
        run_command(["python", "align_voiceovers.py", "--scene", args.scene])
    else:
        run_command(["python", "align_voiceovers.py"])

    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()
