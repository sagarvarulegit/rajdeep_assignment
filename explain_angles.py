from manim import *
import numpy as np
import json
import re
import os
import subprocess
import asyncio
import edge_tts
import urllib.request
import urllib.error

# ElevenLabs Config
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "sk_691fe211addba6b1ed6d18f1818521f42281133339ad8268")
ELEVENLABS_VOICE_ID = "Ij5WqlrmfRUJMb1TYRFl" # FYISC Teacher (Cloned)
ELEVENLABS_MODEL_ID = "eleven_v3"

# Global Config
config.background_color = "#111111"

FFMPEG_PATH = r"C:\Users\sunwa\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFPROBE_PATH = FFMPEG_PATH.replace("ffmpeg.exe", "ffprobe.exe")

def generate_elevenlabs_audio(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": ELEVENLABS_MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    req_body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            with open(output_path, "wb") as f:
                f.write(audio_data)
            return True
    except Exception as e:
        print(f"ElevenLabs TTS failed: {e}")
        return False

def get_audio_duration_and_file(text, scene_name, index):
    cache_dir = os.path.join("voiceovers", "cache_elevenlabs_v3", scene_name)
    os.makedirs(cache_dir, exist_ok=True)
    audio_path = os.path.join(cache_dir, f"sub_{index}.mp3")
    
    if not os.path.exists(audio_path):
        safe_text = text[:40].encode("ascii", errors="replace").decode("ascii")
        print(f"Generating voiceover via ElevenLabs for: '{safe_text}...'")
        success = generate_elevenlabs_audio(text, audio_path)
        if not success:
            print("Falling back to edge-tts...")
            async def save_audio():
                communicate = edge_tts.Communicate(text, "en-IN-PrabhatNeural")
                await communicate.save(audio_path)
            try:
                asyncio.run(save_audio())
            except Exception as e:
                print(f"Failed to generate neural audio for: {text}. Error: {e}")
                try:
                    from gtts import gTTS
                    tts = gTTS(text=text, lang="en")
                    tts.save(audio_path)
                except Exception:
                    pass
        
    cmd = [
        FFPROBE_PATH,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        duration = float(res.stdout.strip())
    except Exception:
        words = len(text.split())
        duration = max(1.5, words / 2.3 + 0.5)
        
    return duration, audio_path


class SubtitledScene(Scene):
    current_subtitle = None
    
    def setup(self):
        super().setup()
        self.subtitle_log = []
        self.speech_end_time = 0.0
        
    def set_subtitle(self, text):
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = clean_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean_text = clean_text.strip()
        
        if clean_text:
            extra_wait = self.speech_end_time - self.time
            if extra_wait > 0:
                self.wait(extra_wait)
                
            idx = len(self.subtitle_log)
            duration, audio_path = get_audio_duration_and_file(clean_text, self.__class__.__name__, idx)
            
            self.subtitle_log.append({
                "time": self.time,
                "text": clean_text,
                "duration": duration,
                "audio_path": audio_path
            })
            self.speech_end_time = self.time + duration
            
        new_sub = MarkupText(text, font="Segoe UI", font_size=15, color="#E2E8F0")
        new_sub.to_edge(DOWN, buff=0.35)
        bg = SurroundingRectangle(new_sub, color="#111111", fill_color="#111111", fill_opacity=0.75, stroke_width=0, buff=0.12)
        bg.round_corners(0.08)
        new_grp = VGroup(bg, new_sub)
        
        if self.current_subtitle is not None:
            self.play(
                FadeOut(self.current_subtitle, run_time=0.25),
                FadeIn(new_grp, run_time=0.25)
            )
        else:
            self.play(FadeIn(new_grp, run_time=0.35))
        self.current_subtitle = new_grp
        
    def clear_subtitle(self):
        if self.current_subtitle is not None:
            self.play(FadeOut(self.current_subtitle, run_time=0.35))
            self.current_subtitle = None
        extra_wait = self.speech_end_time - self.time
        if extra_wait > 0:
            self.wait(extra_wait)
            
    def tear_down(self):
        super().tear_down()
        class_name = self.__class__.__name__
        os.makedirs("voiceovers", exist_ok=True)
        log_path = os.path.join("voiceovers", f"{class_name}_subtitles.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(self.subtitle_log, f, indent=4, ensure_ascii=False)


class TitleScene(SubtitledScene):
    def construct(self):
        title = MarkupText("<span foreground='#22D3EE'><b>ANGLE AND ITS MEASUREMENT</b></span>", font="Segoe UI", font_size=40)
        subtitle = MarkupText("A Comprehensive Visual Guide", font="Segoe UI", font_size=20, color="#94A3B8")
        author = MarkupText("Vikram Tutors", font="Segoe UI", font_size=18, color="#F59E0B")
        
        title.shift(UP * 1.0)
        subtitle.next_to(title, DOWN, buff=0.3)
        author.next_to(subtitle, DOWN, buff=0.5)
        
        # Decorative rotating rays
        origin = Dot(point=ORIGIN, color=GRAY)
        ray1 = Line(ORIGIN, RIGHT * 2.2, color="#22D3EE", stroke_width=4)
        ray2 = Line(ORIGIN, RIGHT * 2.2, color="#F59E0B", stroke_width=4)
        
        ray_group = VGroup(origin, ray1, ray2).shift(DOWN * 1.2)
        
        self.set_subtitle("Welcome! Today, we're going to master the chapter 'Angle and its Measurement' through visual animations.")
        
        self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=UP), FadeIn(author, shift=UP))
        self.wait(1)
        self.play(Create(origin), Create(ray1))
        self.wait(0.5)
        self.play(Create(ray2))
        
        # Rotate terminal ray to form an angle
        self.play(Rotate(ray2, angle=145*DEGREES, about_point=origin.get_center()), run_time=2.5)
        
        # Show an arc between them
        arc = Arc(radius=0.6, start_angle=0, angle=145*DEGREES, arc_center=origin.get_center(), color="#34D399", stroke_width=4)
        arc.add_tip(tip_length=0.1)
        self.play(Create(arc))
        self.wait(2.5)
        
        self.clear_subtitle()
        
        # Transition out
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(author),
            FadeOut(origin), FadeOut(ray1), FadeOut(ray2), FadeOut(arc)
        )
        self.wait(0.5)


class DirectedAngleScene(SubtitledScene):
    def construct(self):
        # Section Title
        sec_title = MarkupText("<b>1. Concept of Directed Angle</b>", font="Segoe UI", font_size=32, color="#22D3EE")
        sec_title.to_edge(UP)
        self.play(Write(sec_title))
        self.wait(0.5)
        
        # Setup Vertex and Initial Arm
        self.set_subtitle("Let's start with the fundamental building block: the Directed Angle.")
        
        vertex = Dot(point=LEFT * 2, color=WHITE, radius=0.08)
        vertex_label = MarkupText("Vertex O", font="Segoe UI", font_size=14, color=WHITE).next_to(vertex, DOWN)
        
        initial_side = Line(LEFT * 2, RIGHT * 1, color="#22D3EE", stroke_width=4)
        initial_label = MarkupText("Initial Arm (OA)", font="Segoe UI", font_size=16, color="#22D3EE").next_to(initial_side, DOWN, buff=0.2)
        
        self.play(Create(vertex), FadeIn(vertex_label))
        self.play(Create(initial_side), FadeIn(initial_label))
        self.wait(1.5)
        
        # Positive Angle rotation (Counterclockwise)
        self.set_subtitle("It consists of a fixed vertex O, an initial arm OA, and a terminal arm OB.")
        
        terminal_side = Line(LEFT * 2, RIGHT * 1, color="#F59E0B", stroke_width=4)
        terminal_label = MarkupText("Terminal Arm (OB)", font="Segoe UI", font_size=16, color="#F59E0B")
        
        self.play(Create(terminal_side))
        self.wait(1.5)
        
        self.set_subtitle("If the terminal arm rotates in a counterclockwise direction, we get a positive angle. Here, it is plus 60 degrees.")
        
        self.play(Rotate(terminal_side, angle=60*DEGREES, about_point=LEFT*2), run_time=2)
        terminal_label.next_to(terminal_side.get_end(), UP+RIGHT, buff=0.1)
        self.play(FadeIn(terminal_label))
        
        # Draw positive angle arc
        arc = Arc(radius=1.0, start_angle=0, angle=60*DEGREES, arc_center=LEFT*2, color="#34D399", stroke_width=4)
        arc.add_tip(tip_length=0.12)
        angle_val = MarkupText("+60°", font="Segoe UI", font_size=18, color="#34D399").next_to(arc, RIGHT, buff=0.2).shift(UP*0.2)
        
        self.play(Create(arc), FadeIn(angle_val))
        
        desc_pos = MarkupText("Rotation: <span foreground='#34D399'>Counterclockwise</span> (Positive +)", font="Segoe UI", font_size=18).to_edge(DOWN).shift(UP * 0.9)
        self.play(Write(desc_pos))
        self.wait(3.5)
        
        # Fade out positive specific elements
        self.play(FadeOut(terminal_label), FadeOut(arc), FadeOut(angle_val), FadeOut(desc_pos))
        
        # Reset terminal side back to initial arm
        self.play(Rotate(terminal_side, angle=-60*DEGREES, about_point=LEFT*2), run_time=1)
        
        # Negative Angle rotation (Clockwise)
        self.set_subtitle("But if the arm rotates in a clockwise direction, we get a negative angle. Here, it is minus 60 degrees.")
        
        self.play(Rotate(terminal_side, angle=-60*DEGREES, about_point=LEFT*2), run_time=2)
        terminal_label.next_to(terminal_side.get_end(), DOWN+RIGHT, buff=0.1)
        self.play(FadeIn(terminal_label))
        
        # Draw negative angle arc
        arc_neg = Arc(radius=1.0, start_angle=0, angle=-60*DEGREES, arc_center=LEFT*2, color="#F472B6", stroke_width=4)
        arc_neg.add_tip(tip_length=0.12)
        angle_val_neg = MarkupText("-60°", font="Segoe UI", font_size=18, color="#F472B6").next_to(arc_neg, RIGHT, buff=0.2).shift(DOWN*0.2)
        
        self.play(Create(arc_neg), FadeIn(angle_val_neg))
        
        desc_neg = MarkupText("Rotation: <span foreground='#F472B6'>Clockwise</span> (Negative -)", font="Segoe UI", font_size=18).to_edge(DOWN).shift(UP * 0.9)
        self.play(Write(desc_neg))
        self.wait(4.0)
        
        self.clear_subtitle()
        
        self.play(FadeOut(VGroup(vertex, vertex_label, initial_side, initial_label, terminal_side, terminal_label, arc_neg, angle_val_neg, desc_neg, sec_title)))
        self.wait(0.5)


class StandardPositionScene(SubtitledScene):
    def construct(self):
        sec_title = MarkupText("<b>2. Standard Position &amp; Quadrants</b>", font="Segoe UI", font_size=30, color="#22D3EE")
        sec_title.to_edge(UP)
        self.play(Write(sec_title))
        
        self.set_subtitle("Next, what is an angle in standard position?")
        
        # Standard axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=5.5,
            y_length=5.5,
            axis_config={"color": GRAY, "stroke_width": 2},
        )
        x_label = Text("x", font="Segoe UI", font_size=16, color=GRAY).next_to(axes.x_axis.get_end(), DOWN+RIGHT, buff=0.1)
        y_label = Text("y", font="Segoe UI", font_size=16, color=GRAY).next_to(axes.y_axis.get_end(), UP+RIGHT, buff=0.1)
        axes_labels = VGroup(x_label, y_label)
        axes_grp = VGroup(axes, axes_labels).shift(RIGHT * 1.5 + DOWN * 0.4)
        
        # Quadrant labels
        q1 = MarkupText("Quadrant I", font="Segoe UI", font_size=14, color="#94A3B8").move_to(axes.coords_to_point(1.8, 1.8))
        q2 = MarkupText("Quadrant II", font="Segoe UI", font_size=14, color="#94A3B8").move_to(axes.coords_to_point(-1.8, 1.8))
        q3 = MarkupText("Quadrant III", font="Segoe UI", font_size=14, color="#94A3B8").move_to(axes.coords_to_point(-1.8, -1.8))
        q4 = MarkupText("Quadrant IV", font="Segoe UI", font_size=14, color="#94A3B8").move_to(axes.coords_to_point(1.8, -1.8))
        quadrants = VGroup(q1, q2, q3, q4)
        
        self.play(Create(axes), Write(axes_labels))
        self.play(FadeIn(quadrants))
        self.wait(1.5)
        
        self.set_subtitle("An angle is in standard position when its vertex is at the origin, and its initial arm lies along the positive x-axis.")
        
        # Definition of Standard Position
        def_text = MarkupText(
            "<b>Standard Position:</b>\n"
            "• Vertex is at Origin (0,0)\n"
            "• Initial Arm is along +x axis",
            font="Segoe UI", font_size=16, color="#E2E8F0"
        )
        def_text.to_edge(LEFT, buff=0.8).shift(UP * 0.5)
        self.play(Write(def_text))
        
        # Initial arm along positive x-axis
        initial_arm = Line(axes.coords_to_point(0,0), axes.coords_to_point(2.2, 0), color="#22D3EE", stroke_width=5)
        self.play(Create(initial_arm))
        self.wait(2.5)
        
        # -- Case 1: -135 degrees --
        self.set_subtitle("Let's draw minus 135 degrees. We rotate clockwise from the initial side, landing in Quadrant 3.")
        
        case_info = VGroup(
            MarkupText("<b>Example 1: -135°</b>", font="Segoe UI", font_size=18, color="#F472B6"),
            MarkupText("• Rotates clockwise", font="Segoe UI", font_size=15, color="#E2E8F0"),
            MarkupText("• Lies in Quadrant III", font="Segoe UI", font_size=15, color="#F472B6")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(def_text, DOWN, buff=0.6).align_to(def_text, LEFT)
        
        self.play(Write(case_info))
        
        terminal_arm = Line(axes.coords_to_point(0,0), axes.coords_to_point(2.2, 0), color="#F59E0B", stroke_width=5)
        self.play(Rotate(terminal_arm, angle=-135*DEGREES, about_point=axes.coords_to_point(0,0)), run_time=2)
        
        # Arc for -135
        arc_case1 = Arc(radius=0.7, start_angle=0, angle=-135*DEGREES, arc_center=axes.coords_to_point(0,0), color="#F472B6", stroke_width=4)
        arc_case1.add_tip(tip_length=0.1)
        label_case1 = MarkupText("-135°", font="Segoe UI", font_size=16, color="#F472B6").move_to(axes.coords_to_point(0.8, -0.8))
        
        # Highlight Quadrant III
        q3_highlight = q3.copy().set_color("#F472B6").scale(1.25)
        
        self.play(Create(arc_case1), Write(label_case1))
        self.play(Transform(q3, q3_highlight))
        self.wait(3.5)
        
        # -- Case 2: Co-terminal angle (225 degrees) --
        self.set_subtitle("Now, let's find a positive angle with the exact same terminal side: 225 degrees. These are called co-terminal angles.")
        
        self.play(FadeOut(case_info))
        coterm_info = VGroup(
            MarkupText("<b>Co-terminal Angle: 225°</b>", font="Segoe UI", font_size=18, color="#34D399"),
            MarkupText("• Shares same initial\n  and terminal arms!", font="Segoe UI", font_size=15, color="#E2E8F0"),
            MarkupText("• 225° - (-135°) = 360°", font="Segoe UI", font_size=15, color="#34D399")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(def_text, DOWN, buff=0.6).align_to(def_text, LEFT)
        
        self.play(Write(coterm_info))
        
        # Arc for +225
        arc_coterm = Arc(radius=0.9, start_angle=0, angle=225*DEGREES, arc_center=axes.coords_to_point(0,0), color="#34D399", stroke_width=4)
        arc_coterm.add_tip(tip_length=0.1)
        label_coterm = MarkupText("225°", font="Segoe UI", font_size=16, color="#34D399").move_to(axes.coords_to_point(-1.0, 0.8))
        
        self.play(Create(arc_coterm), Write(label_coterm))
        self.wait(4.5)
        
        # Fade out case 1 & co-terminal elements
        self.play(
            FadeOut(arc_case1), FadeOut(label_case1),
            FadeOut(arc_coterm), FadeOut(label_coterm),
            FadeOut(coterm_info),
            Rotate(terminal_arm, angle=135*DEGREES, about_point=axes.coords_to_point(0,0)), # reset terminal
            Transform(q3, q3.copy().set_color("#94A3B8").scale(1/1.25)) # reset Q3
        )
        self.wait(1)
        
        # -- Case 3: 740 degrees (Multiple rotations) --
        self.set_subtitle("Finally, let's look at 740 degrees. This involves two full rotations of 360 degrees, plus an extra 20 degrees, landing in Quadrant 1.")
        
        case3_info = VGroup(
            MarkupText("<b>Example 2: 740°</b>", font="Segoe UI", font_size=18, color="#34D399"),
            MarkupText("• 740° = 2 × 360° + 20°", font="Segoe UI", font_size=15, color="#34D399"),
            MarkupText("• 2 Full rotations + 20°", font="Segoe UI", font_size=15, color="#E2E8F0"),
            MarkupText("• Lies in Quadrant I", font="Segoe UI", font_size=15, color="#34D399")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(def_text, DOWN, buff=0.6).align_to(def_text, LEFT)
        
        self.play(Write(case3_info))
        
        # Rotate terminal side 740 degrees (slow linear rotation)
        self.play(Rotate(terminal_arm, angle=740*DEGREES, about_point=axes.coords_to_point(0,0)), run_time=3.5, rate_func=linear)
        
        # Spiral arc: r = 0.35 + 0.1 * t
        center_pt = axes.coords_to_point(0,0)
        x_val = lambda t: center_pt[0] + (0.35 + 0.1 * t) * np.cos(t)
        y_val = lambda t: center_pt[1] + (0.35 + 0.1 * t) * np.sin(t)
        
        spiral = ParametricFunction(
            lambda t: np.array([x_val(t), y_val(t), 0]),
            t_range=[0, 740*DEGREES],
            color="#34D399",
            stroke_width=4
        )
        label_case3 = MarkupText("740°", font="Segoe UI", font_size=16, color="#34D399").move_to(axes.coords_to_point(1.3, 0.7))
        
        q1_highlight = q1.copy().set_color("#34D399").scale(1.25)
        
        self.play(Create(spiral), Write(label_case3))
        self.play(Transform(q1, q1_highlight))
        self.wait(4.5)
        
        self.clear_subtitle()
        
        # Clean up scene
        self.play(
            FadeOut(axes), FadeOut(axes_labels), FadeOut(quadrants), FadeOut(q1), FadeOut(q3),
            FadeOut(initial_arm), FadeOut(terminal_arm), FadeOut(case3_info), FadeOut(spiral),
            FadeOut(label_case3), FadeOut(def_text), FadeOut(sec_title)
        )
        self.wait(0.5)


class MeasurementSystemsScene(SubtitledScene):
    def construct(self):
        sec_title = MarkupText("<b>3. Measurement Systems</b>", font="Segoe UI", font_size=30, color="#22D3EE")
        sec_title.to_edge(UP)
        self.play(Write(sec_title))
        
        self.set_subtitle("How do we measure angles? There are two main systems: the Sexagesimal system and the Circular system.")
        
        # Sexagesimal System
        sex_title = MarkupText("<b>A. Sexagesimal System (Degrees)</b>", font="Segoe UI", font_size=20, color="#F59E0B")
        sex_title.next_to(sec_title, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        
        bullet1 = MarkupText("• 1 Full Rotation = 360°", font="Segoe UI", font_size=18, color="#E2E8F0")
        bullet2 = MarkupText("• 1 Degree (1°) = 60 Minutes (60')", font="Segoe UI", font_size=18, color="#E2E8F0")
        bullet3 = MarkupText("• 1 Minute (1') = 60 Seconds (60\")", font="Segoe UI", font_size=18, color="#E2E8F0")
        
        bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bullets.next_to(sex_title, DOWN, buff=0.3).align_to(sex_title, LEFT)
        
        self.play(Write(sex_title))
        self.play(FadeIn(bullets, shift=RIGHT))
        self.wait(2.5)
        
        self.set_subtitle("In the Sexagesimal system, we use degrees, minutes, and seconds. One degree is 60 minutes, and one minute is 60 seconds.")
        self.wait(4.0)
        
        # Transition to Radian System
        self.play(FadeOut(sex_title), FadeOut(bullets))
        
        self.set_subtitle("In the Circular system, we use Radians. One radian is the angle subtended by an arc whose length equals the radius.")
        
        rad_title = MarkupText("<b>B. Circular System (Radians)</b>", font="Segoe UI", font_size=20, color="#A78BFA")
        rad_title.next_to(sec_title, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        self.play(Write(rad_title))
        
        # Visualize Radian Definition
        circle = Circle(radius=1.8, color=GRAY, stroke_width=2).shift(RIGHT * 2.2 + DOWN * 0.5)
        center = Dot(point=circle.get_center(), color=WHITE)
        
        # Initial Radius (pointing right)
        r_start = circle.get_center()
        r_end = circle.get_center() + RIGHT * 1.8
        radius_line1 = Line(r_start, r_end, color="#22D3EE", stroke_width=4)
        radius_label1 = MarkupText("Radius (r)", font="Segoe UI", font_size=14, color="#22D3EE").next_to(radius_line1, DOWN, buff=0.1)
        
        self.play(Create(circle), Create(center))
        self.play(Create(radius_line1), FadeIn(radius_label1))
        self.wait(0.5)
        
        # Angle in radians is 1.0 (approx 57.3 degrees)
        angle_rad = 1.0
        
        # Terminal Radius
        radius_line2 = Line(r_start, circle.get_center() + np.array([1.8 * np.cos(angle_rad), 1.8 * np.sin(angle_rad), 0]), color="#22D3EE", stroke_width=4)
        radius_label2 = MarkupText("Radius (r)", font="Segoe UI", font_size=14, color="#22D3EE").next_to(radius_line2.get_end(), UP+LEFT, buff=0.1)
        
        # Arc
        arc_r = Arc(radius=1.8, start_angle=0, angle=angle_rad, arc_center=circle.get_center(), color="#A78BFA", stroke_width=6)
        arc_label = MarkupText("Arc Length (s) = r", font="Segoe UI", font_size=14, color="#A78BFA").next_to(arc_r, RIGHT, buff=0.15).shift(UP * 0.4)
        
        # Angle label
        angle_arc = Arc(radius=0.5, start_angle=0, angle=angle_rad, arc_center=circle.get_center(), color="#34D399")
        angle_label = MarkupText("1ᶜ", font="Segoe UI", font_size=18, color="#34D399").move_to(circle.get_center() + np.array([0.75 * np.cos(0.5), 0.75 * np.sin(0.5), 0]))
        
        def_explain = VGroup(
            MarkupText("<b>1 Radian (1ᶜ):</b>", font="Segoe UI", font_size=18, color="#34D399"),
            MarkupText("The measure of an angle\nsubtended at the center of\na circle by an arc whose\nlength is equal to the\nradius of the circle.", font="Segoe UI", font_size=15, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rad_title, DOWN, buff=0.4).align_to(rad_title, LEFT)
        
        self.play(Write(def_explain))
        self.play(Create(arc_r), FadeIn(arc_label))
        self.play(Create(radius_line2), FadeIn(radius_label2))
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(4.5)
        
        # Transition to conversion formula
        self.play(
            FadeOut(circle), FadeOut(center), FadeOut(radius_line1), FadeOut(radius_label1),
            FadeOut(radius_line2), FadeOut(radius_label2), FadeOut(arc_r), FadeOut(arc_label),
            FadeOut(angle_arc), FadeOut(angle_label), FadeOut(def_explain), FadeOut(rad_title)
        )
        
        self.set_subtitle("We convert between these systems using the relation: pi radians equals 180 degrees. To convert degrees to radians, multiply by pi over 180.")
        
        conv_title = MarkupText("<b>Angle Conversion Formulas</b>", font="Segoe UI", font_size=22, color="#34D399")
        conv_title.next_to(sec_title, DOWN, buff=0.4)
        
        formula1 = MarkupText("<b>π Radians = 180°</b>", font="Segoe UI", font_size=20, color="#F59E0B")
        formula2 = MarkupText("• <b>Degrees to Radians:</b>  Radian = Degree × (π / 180)", font="Segoe UI", font_size=18, color="#E2E8F0")
        formula3 = MarkupText("• <b>Radians to Degrees:</b>  Degree = Radian × (180 / π)", font="Segoe UI", font_size=18, color="#E2E8F0")
        
        conversion_box = VGroup(formula1, formula2, formula3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        conversion_box.next_to(conv_title, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        
        self.play(Write(conv_title))
        self.play(FadeIn(conversion_box, shift=UP))
        self.wait(5.0)
        
        self.set_subtitle("For example, converting 30 degrees gives us pi over 6 radians.")
        
        # Example conversion
        example_text = MarkupText("<b>Example:</b> Convert 30° to Radians\n30° × (π / 180) = <b>π / 6 Radians</b>", font="Segoe UI", font_size=18, color="#22D3EE").next_to(conversion_box, DOWN, buff=0.6).align_to(conversion_box, LEFT)
        self.play(Write(example_text))
        self.wait(3.5)
        
        self.clear_subtitle()
        
        self.play(FadeOut(VGroup(sec_title, conv_title, conversion_box, example_text)))
        self.wait(0.5)


class FormulasScene(SubtitledScene):
    def construct(self):
        sec_title = MarkupText("<b>4. Arc Length &amp; Sector Area</b>", font="Segoe UI", font_size=30, color="#22D3EE")
        sec_title.to_edge(UP)
        self.play(Write(sec_title))
        
        self.set_subtitle("We can relate the radius, arc length, and central angle in radians using two key formulas.")
        
        # Circle sector on the right
        circle = Circle(radius=1.8, color=GRAY, stroke_width=2).shift(RIGHT * 2.5 + DOWN * 0.5)
        center = Dot(point=circle.get_center(), color=WHITE)
        
        # Sector with angle = 1.25 radians (~71.6 degrees)
        theta = 1.25
        r_start = circle.get_center()
        r_end1 = circle.get_center() + RIGHT * 1.8
        r_end2 = circle.get_center() + np.array([1.8 * np.cos(theta), 1.8 * np.sin(theta), 0])
        
        rad1 = Line(r_start, r_end1, color="#22D3EE", stroke_width=3)
        rad2 = Line(r_start, r_end2, color="#22D3EE", stroke_width=3)
        arc = Arc(radius=1.8, start_angle=0, angle=theta, arc_center=circle.get_center(), color="#A78BFA", stroke_width=5)
        
        # Shaded sector area using AnnularSector
        sector_fill = AnnularSector(
            inner_radius=0,
            outer_radius=1.8,
            angle=theta,
            start_angle=0,
            color="#A78BFA",
            fill_opacity=0.25,
            arc_center=circle.get_center()
        )
        
        labels_grp = VGroup(
            MarkupText("r", font="Segoe UI", font_size=16, color="#22D3EE").next_to(rad1, DOWN, buff=0.1),
            MarkupText("s", font="Segoe UI", font_size=18, color="#A78BFA").next_to(arc, RIGHT, buff=0.15).shift(UP * 0.4),
            MarkupText("θ", font="Segoe UI", font_size=18, color="#34D399").move_to(circle.get_center() + np.array([0.65 * np.cos(0.6), 0.65 * np.sin(0.6), 0])),
            MarkupText("Area (A)", font="Segoe UI", font_size=16, color="#A78BFA").move_to(circle.get_center() + np.array([1.1 * np.cos(0.65), 1.1 * np.sin(0.65), 0]))
        )
        
        self.play(Create(circle), Create(center))
        self.play(Create(rad1), Create(rad2), Create(arc), FadeIn(sector_fill))
        self.play(FadeIn(labels_grp))
        self.wait(2.0)
        
        self.set_subtitle("The arc length s is equal to r times theta, and the sector area A is half r-squared times theta. Remember, theta must be in radians!")
        
        # Formulas on the left
        formula1 = MarkupText("<b>Arc Length (s):</b>\n<span foreground='#A78BFA'>s = r × θ</span>", font="Segoe UI", font_size=18)
        formula2 = MarkupText("<b>Sector Area (A):</b>\n<span foreground='#A78BFA'>A = ½ r² × θ</span>", font="Segoe UI", font_size=18)
        warning = MarkupText("<i>Note: θ MUST be in Radians!</i>", font="Segoe UI", font_size=15, color="#EF4444")
        
        formula_box = VGroup(formula1, formula2, warning).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        formula_box.next_to(sec_title, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        
        self.play(FadeIn(formula_box, shift=RIGHT))
        self.wait(5.0)
        
        # Transition to the Clock Problem
        self.play(
            FadeOut(circle), FadeOut(center), FadeOut(rad1), FadeOut(rad2), FadeOut(arc),
            FadeOut(sector_fill), FadeOut(labels_grp), FadeOut(formula_box)
        )
        
        self.set_subtitle("Let's apply this to a clock problem from our exercise sheet.")
        
        prob_title = MarkupText("<b>Practical Application (Clock Problem)</b>", font="Segoe UI", font_size=22, color="#F59E0B")
        prob_title.next_to(sec_title, DOWN, buff=0.4)
        self.play(Write(prob_title))
        
        self.wait(2.0)
        
        self.set_subtitle("A clock hand is 21 centimeters long. How far does the tip move in 20 minutes?")
        
        # Problem from Exercise-1 (Q13)
        prob_desc = MarkupText(
            "<b>Problem (Exercise 1, Q13):</b>\n"
            "The large hand of a clock is 21 cm long.\n"
            "How much distance does its extremity move in 20 minutes?",
            font="Segoe UI", font_size=16, color="#E2E8F0"
        ).next_to(prob_title, DOWN, buff=0.3)
        self.play(Write(prob_desc))
        self.wait(4.5)
        
        self.set_subtitle("In 20 minutes, the hand covers one-third of a full rotation, which is 2 pi over 3 radians.")
        
        # Step-by-step solution
        step1 = MarkupText(
            "<b>Step 1: Find angle θ in Radians</b>\n"
            "• In 60 minutes, the minute hand turns 360° (2π radians).\n"
            "• In 20 minutes, the rotation fraction is 20/60 = 1/3.\n"
            "• Angle θ = 1/3 × 2π = <span foreground='#34D399'>2π/3 radians</span>",
            font="Segoe UI", font_size=15, color="#94A3B8"
        )
        
        self.play(FadeIn(step1, shift=UP))
        self.wait(5.0)
        
        self.set_subtitle("Using s equals r times theta, we multiply 21 by 2 pi over 3, giving us 14 pi, which is approximately 44 centimeters.")
        
        step2 = MarkupText(
            "<b>Step 2: Use Arc Length Formula (s = r × θ)</b>\n"
            "• Radius r = 21 cm (length of hand)\n"
            "• s = 21 × (2π/3) = 14π cm\n"
            "• Using π ≈ 22/7:\n"
            "  s ≈ 14 × (22/7) = <span foreground='#34D399'>44 cm</span>",
            font="Segoe UI", font_size=15, color="#94A3B8"
        )
        
        steps = VGroup(step1, step2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob_desc, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        
        self.play(FadeIn(step2, shift=UP))
        self.wait(3.0)
        
        # Final Highlight Box
        ans_box = MarkupText(
            "<b>Answer: The tip moves 44 cm</b>",
            font="Segoe UI", font_size=18, color="#111111"
        )
        ans_bg = SurroundingRectangle(ans_box, color="#34D399", fill_color="#34D399", fill_opacity=0.9, corner_radius=0.1, buff=0.25)
        final_ans = VGroup(ans_bg, ans_box).next_to(steps, RIGHT, buff=0.8).shift(UP * 0.5)
        
        self.play(Create(ans_bg), Write(ans_box))
        self.wait(4.5)
        
        self.clear_subtitle()
        
        # Clean up
        self.play(FadeOut(VGroup(sec_title, prob_title, prob_desc, steps, final_ans)))
        self.wait(0.5)


class OutroScene(SubtitledScene):
    def construct(self):
        thank_you = MarkupText("<span foreground='#22D3EE'><b>Thank You!</b></span>", font="Segoe UI", font_size=40)
        sub = MarkupText("Hope this video helps you master Angle and its Measurement.", font="Segoe UI", font_size=18, color="#94A3B8")
        tut = MarkupText("Vikram Tutors", font="Segoe UI", font_size=20, color="#F59E0B")
        
        v_grp = VGroup(thank_you, sub, tut).arrange(DOWN, buff=0.4)
        
        self.set_subtitle("Thank you for watching! We hope this video helps you master Angle and its Measurement. Happy learning!")
        
        self.play(FadeIn(v_grp, shift=UP))
        self.wait(4.5)
        
        self.clear_subtitle()
        
        self.play(FadeOut(v_grp))
        self.wait(0.5)
