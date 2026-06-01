# Graph Report - .  (2026-06-01)

## Corpus Check
- 35 files · ~7,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 118 nodes · 188 edges · 36 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Explanation Scenes Core|Explanation Scenes Core]]
- [[_COMMUNITY_Exercise Scenes Group A|Exercise Scenes Group A]]
- [[_COMMUNITY_Exercise Scenes Group B|Exercise Scenes Group B]]
- [[_COMMUNITY_Exercise Scenes Group C|Exercise Scenes Group C]]
- [[_COMMUNITY_Exercise Solutions Logic|Exercise Solutions Logic]]
- [[_COMMUNITY_Mathematical Formulas|Mathematical Formulas]]
- [[_COMMUNITY_Degree-Radian Conversions|Degree-Radian Conversions]]
- [[_COMMUNITY_Whiteboard Animation Setup|Whiteboard Animation Setup]]
- [[_COMMUNITY_Voiceover Alignment|Voiceover Alignment]]
- [[_COMMUNITY_Project Infrastructure|Project Infrastructure]]
- [[_COMMUNITY_Circular Geometry Applications|Circular Geometry Applications]]
- [[_COMMUNITY_Bulk Rendering|Bulk Rendering]]
- [[_COMMUNITY_Question 18 Logic|Question 18 Logic]]
- [[_COMMUNITY_Question 8 Logic|Question 8 Logic]]
- [[_COMMUNITY_Question 20 Logic|Question 20 Logic]]
- [[_COMMUNITY_Question 13 Logic|Question 13 Logic]]
- [[_COMMUNITY_Question 9 Logic|Question 9 Logic]]
- [[_COMMUNITY_Question 6 Logic|Question 6 Logic]]
- [[_COMMUNITY_Question 11 Logic|Question 11 Logic]]
- [[_COMMUNITY_Question 19 Logic|Question 19 Logic]]
- [[_COMMUNITY_Question 12 Logic|Question 12 Logic]]
- [[_COMMUNITY_Pendulum Concept|Pendulum Concept]]
- [[_COMMUNITY_Directed Angle Concept|Directed Angle Concept]]
- [[_COMMUNITY_Clock Hands Concept|Clock Hands Concept]]
- [[_COMMUNITY_Standard Position Concept|Standard Position Concept]]
- [[_COMMUNITY_Exercise Solutions Code|Exercise Solutions Code]]
- [[_COMMUNITY_Quadrant Analysis|Quadrant Analysis]]
- [[_COMMUNITY_Area Formulas|Area Formulas]]
- [[_COMMUNITY_Question 17 Concept|Question 17 Concept]]
- [[_COMMUNITY_Question 18 Concept|Question 18 Concept]]
- [[_COMMUNITY_Question 19 Concept|Question 19 Concept]]
- [[_COMMUNITY_Question 2 Concept|Question 2 Concept]]
- [[_COMMUNITY_Question 5 Concept|Question 5 Concept]]
- [[_COMMUNITY_Question 6 Concept|Question 6 Concept]]
- [[_COMMUNITY_Question 7 Concept|Question 7 Concept]]
- [[_COMMUNITY_Title Scene|Title Scene]]

## God Nodes (most connected - your core abstractions)
1. `SubtitledScene` - 27 edges
2. `SubtitledScene` - 12 edges
3. `WhiteboardSubtitledScene` - 5 edges
4. `get_audio_duration_and_file()` - 4 edges
5. `Q16Scene` - 4 edges
6. `align_scene()` - 3 edges
7. `Q1Scene` - 3 edges
8. `Q2Scene` - 3 edges
9. `Q3Scene` - 3 edges
10. `Q4Scene` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Question 16: Angle at 3:30` --references--> `Q16Scene`  [EXTRACTED]
  angles_its_measurement/final_videos/Q16Scene_with_voiceover.mp4 → angles_its_measurement\exercise_one_solutions.py
- `FYISC Angle and Measurement Exercise 1` --cites--> `Degree to Radian Conversion Formula`  [INFERRED]
  angles_its_measurement/FYISC - Angle and it's Measurement.pdf → angles_its_measurement/youtube_questions_transcript.txt
- `Question 16: Angle at 3:30` --conceptually_related_to--> `Radian-Degree Relation (π rad = 180°)`  [INFERRED]
  angles_its_measurement/final_videos/Q16Scene_with_voiceover.mp4 → angles_its_measurement/FYISC - Angle and it's Measurement.pdf
- `Question 20: Diameter of the Sun` --conceptually_related_to--> `Arc Length Formula (s = rθ)`  [INFERRED]
  angles_its_measurement/final_videos/Q20Scene_with_voiceover.mp4 → angles_its_measurement/FYISC - Angle and it's Measurement.pdf
- `Question 3: Degrees to Radians` --conceptually_related_to--> `Radian-Degree Relation (π rad = 180°)`  [INFERRED]
  angles_its_measurement/final_videos/Q3Scene_with_voiceover.mp4 → angles_its_measurement/FYISC - Angle and it's Measurement.pdf

## Hyperedges (group relationships)
- **Mathematical Animation Workflow** — readme_manim, readme_elevenlabs_tts_api, readme_explain_angles_py [EXTRACTED 1.00]
- **Circular Geometry Concepts** — youtube_questions_transcript_arc_length, youtube_questions_transcript_area_of_sector, youtube_questions_transcript_degree_to_radian [INFERRED 0.85]
- **Angle and its Measurement Video Solutions** — q1scene_with_voiceover, q2scene_with_voiceover, q3scene_with_voiceover, q4scene_with_voiceover, q5scene_with_voiceover, q6scene_with_voiceover, q7scene_with_voiceover, q8scene_with_voiceover, q9scene_with_voiceover, q10scene_with_voiceover, q16scene_with_voiceover, q17scene_with_voiceover, q18scene_with_voiceover, q19scene_with_voiceover, q20scene_with_voiceover [EXTRACTED 1.00]
- **Core Angle Concepts Visualized** — titlescene_with_voiceover, standardpositionscene_with_voiceover, q1scene_with_voiceover, q3scene_with_voiceover, q4scene_with_voiceover [INFERRED 0.80]

## Communities

### Community 0 - "Explanation Scenes Core"
Cohesion: 0.19
Nodes (10): DirectedAngleScene, FormulasScene, generate_elevenlabs_audio(), get_audio_duration_and_file(), MeasurementSystemsScene, OutroScene, StandardPositionScene, SubtitledScene (+2 more)

### Community 1 - "Exercise Scenes Group A"
Cohesion: 0.29
Nodes (3): Q10Scene, Q15Scene, Q3Scene

### Community 2 - "Exercise Scenes Group B"
Cohesion: 0.29
Nodes (3): Q2Scene, Q5Scene, Q7Scene

### Community 3 - "Exercise Scenes Group C"
Cohesion: 0.29
Nodes (3): Q14Scene, Q4Scene, SubtitledScene

### Community 4 - "Exercise Solutions Logic"
Cohesion: 0.33
Nodes (4): generate_elevenlabs_audio(), get_audio_duration_and_file(), Q17Scene, Q1Scene

### Community 5 - "Mathematical Formulas"
Cohesion: 0.33
Nodes (6): Formulas and Concepts Video Scene, FYISC Angle and Measurement Exercise 1, Measurement Systems Video Scene, Arc Length Formula (S = r * theta), Degree to Radian Conversion Formula, Sun Diameter and Parallax Calculation

### Community 6 - "Degree-Radian Conversions"
Cohesion: 0.33
Nodes (5): Q16Scene, Question 16: Angle at 3:30, Question 3: Degrees to Radians, Question 4: Radians to Degrees, Radian-Degree Relation (π rad = 180°)

### Community 7 - "Whiteboard Animation Setup"
Cohesion: 0.4
Nodes (2): Q13SceneWhiteboard, WhiteboardSubtitledScene

### Community 8 - "Voiceover Alignment"
Cohesion: 0.83
Nodes (3): align_scene(), main(), run_command()

### Community 9 - "Project Infrastructure"
Cohesion: 0.5
Nodes (4): Angle and its Measurement Video Series, ElevenLabs TTS API, explain_angles.py Source Code, Manim Animation Engine

### Community 10 - "Circular Geometry Applications"
Cohesion: 0.5
Nodes (4): Arc Length Formula (s = rθ), Question 20: Diameter of the Sun, Question 8: Pendulum Swing, Question 9: Radius from Arc Length

### Community 11 - "Bulk Rendering"
Cohesion: 1.0
Nodes (2): main(), run_command()

### Community 12 - "Question 18 Logic"
Cohesion: 1.0
Nodes (1): Q18Scene

### Community 13 - "Question 8 Logic"
Cohesion: 1.0
Nodes (1): Q8Scene

### Community 14 - "Question 20 Logic"
Cohesion: 1.0
Nodes (1): Q20Scene

### Community 15 - "Question 13 Logic"
Cohesion: 1.0
Nodes (1): Q13Scene

### Community 16 - "Question 9 Logic"
Cohesion: 1.0
Nodes (1): Q9Scene

### Community 17 - "Question 6 Logic"
Cohesion: 1.0
Nodes (1): Q6Scene

### Community 18 - "Question 11 Logic"
Cohesion: 1.0
Nodes (1): Q11Scene

### Community 19 - "Question 19 Logic"
Cohesion: 1.0
Nodes (1): Q19Scene

### Community 20 - "Question 12 Logic"
Cohesion: 1.0
Nodes (1): Q12Scene

### Community 21 - "Pendulum Concept"
Cohesion: 1.0
Nodes (2): Pendulum (Q14) Video Scene, Pendulum Swings and Arc Measurement

### Community 22 - "Directed Angle Concept"
Cohesion: 1.0
Nodes (2): Directed Angle Video Scene, Negative Angles and Clockwise Direction

### Community 23 - "Clock Hands Concept"
Cohesion: 1.0
Nodes (2): Clock Hands (Q13) Video Scene, Angle Between Clock Hands

### Community 24 - "Standard Position Concept"
Cohesion: 1.0
Nodes (2): Question 1: Drawing Angles & Quadrants, Concept: Standard Position

### Community 25 - "Exercise Solutions Code"
Cohesion: 1.0
Nodes (1): exercise_one_solutions.py Source Code

### Community 26 - "Quadrant Analysis"
Cohesion: 1.0
Nodes (1): Quadrant Determination

### Community 27 - "Area Formulas"
Cohesion: 1.0
Nodes (1): Area of Sector Formula

### Community 28 - "Question 17 Concept"
Cohesion: 1.0
Nodes (1): Question 17: Third Angle of a Triangle

### Community 29 - "Question 18 Concept"
Cohesion: 1.0
Nodes (1): Question 18: Acute Angles of Right Triangle

### Community 30 - "Question 19 Concept"
Cohesion: 1.0
Nodes (1): Question 19: Triangle Angles in A.P.

### Community 31 - "Question 2 Concept"
Cohesion: 1.0
Nodes (1): Question 2: Angle Quadrant Analysis

### Community 32 - "Question 5 Concept"
Cohesion: 1.0
Nodes (1): Question 5: Degrees & Minutes to Radians

### Community 33 - "Question 6 Concept"
Cohesion: 1.0
Nodes (1): Question 6: Radians to Degrees, Minutes, & Seconds

### Community 34 - "Question 7 Concept"
Cohesion: 1.0
Nodes (1): Question 7: Wheel Revolutions

### Community 35 - "Title Scene"
Cohesion: 1.0
Nodes (1): Title Scene: Angle and its Measurement

## Knowledge Gaps
- **31 isolated node(s):** `Angle and its Measurement Video Series`, `Manim Animation Engine`, `ElevenLabs TTS API`, `exercise_one_solutions.py Source Code`, `Negative Angles and Clockwise Direction` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Question 18 Logic`** (2 nodes): `Q18Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 8 Logic`** (2 nodes): `Q8Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 20 Logic`** (2 nodes): `Q20Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 13 Logic`** (2 nodes): `Q13Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 9 Logic`** (2 nodes): `Q9Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 6 Logic`** (2 nodes): `Q6Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 11 Logic`** (2 nodes): `Q11Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 19 Logic`** (2 nodes): `Q19Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 12 Logic`** (2 nodes): `Q12Scene`, `.construct()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pendulum Concept`** (2 nodes): `Pendulum (Q14) Video Scene`, `Pendulum Swings and Arc Measurement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Directed Angle Concept`** (2 nodes): `Directed Angle Video Scene`, `Negative Angles and Clockwise Direction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Clock Hands Concept`** (2 nodes): `Clock Hands (Q13) Video Scene`, `Angle Between Clock Hands`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Standard Position Concept`** (2 nodes): `Question 1: Drawing Angles & Quadrants`, `Concept: Standard Position`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exercise Solutions Code`** (1 nodes): `exercise_one_solutions.py Source Code`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Quadrant Analysis`** (1 nodes): `Quadrant Determination`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Area Formulas`** (1 nodes): `Area of Sector Formula`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 17 Concept`** (1 nodes): `Question 17: Third Angle of a Triangle`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 18 Concept`** (1 nodes): `Question 18: Acute Angles of Right Triangle`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 19 Concept`** (1 nodes): `Question 19: Triangle Angles in A.P.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 2 Concept`** (1 nodes): `Question 2: Angle Quadrant Analysis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 5 Concept`** (1 nodes): `Question 5: Degrees & Minutes to Radians`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 6 Concept`** (1 nodes): `Question 6: Radians to Degrees, Minutes, & Seconds`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Question 7 Concept`** (1 nodes): `Question 7: Wheel Revolutions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Title Scene`** (1 nodes): `Title Scene: Angle and its Measurement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SubtitledScene` connect `Exercise Scenes Group C` to `Explanation Scenes Core`, `Exercise Scenes Group A`, `Exercise Scenes Group B`, `Exercise Solutions Logic`, `Degree-Radian Conversions`, `Whiteboard Animation Setup`, `Question 18 Logic`, `Question 8 Logic`, `Question 20 Logic`, `Question 13 Logic`, `Question 9 Logic`, `Question 6 Logic`, `Question 11 Logic`, `Question 19 Logic`, `Question 12 Logic`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Why does `Q16Scene` connect `Degree-Radian Conversions` to `Exercise Scenes Group C`, `Exercise Solutions Logic`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **What connects `Angle and its Measurement Video Series`, `Manim Animation Engine`, `ElevenLabs TTS API` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._