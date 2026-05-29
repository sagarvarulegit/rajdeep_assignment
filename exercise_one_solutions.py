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


class WhiteboardSubtitledScene(SubtitledScene):
    def setup(self):
        super().setup()
        self.camera.background_color = "#FDFBF7"
        
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
            
        new_sub = MarkupText(text, font="Segoe UI", font_size=15, color="#1E293B")
        new_sub.to_edge(DOWN, buff=0.35)
        bg = SurroundingRectangle(new_sub, color="#CBD5E1", fill_color="#F1F5F9", fill_opacity=0.95, stroke_width=1.5, buff=0.12)
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


class Q1Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 1: Drawing Angles &amp; Quadrants</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], x_length=5, y_length=5, axis_config={"color": GRAY, "stroke_width": 2})
        x_label = Text("x", font="Segoe UI", font_size=14, color=GRAY).next_to(axes.x_axis.get_end(), DOWN+RIGHT, buff=0.1)
        y_label = Text("y", font="Segoe UI", font_size=14, color=GRAY).next_to(axes.y_axis.get_end(), UP+RIGHT, buff=0.1)
        axes_labels = VGroup(x_label, y_label)
        axes_grp = VGroup(axes, axes_labels).shift(RIGHT * 1.8 + DOWN * 0.4)
        
        self.play(Create(axes), Write(axes_labels))
        
        # Q1(a)(i) -135 degrees
        self.set_subtitle("Question 1(a)(i): Draw -135 degrees and find its quadrant.")
        initial_arm = Line(axes.c2p(0,0), axes.c2p(2,0), color="#22D3EE", stroke_width=5)
        terminal_arm = Line(axes.c2p(0,0), axes.c2p(2,0), color="#F59E0B", stroke_width=5)
        self.play(Create(initial_arm), Create(terminal_arm))
        
        self.set_subtitle("Since the angle is negative, we rotate clockwise by 135 degrees.")
        self.play(Rotate(terminal_arm, angle=-135*DEGREES, about_point=axes.c2p(0,0)), run_time=2)
        
        arc1 = Arc(radius=0.7, start_angle=0, angle=-135*DEGREES, arc_center=axes.c2p(0,0), color="#F472B6", stroke_width=4)
        arc1.add_tip(tip_length=0.1)
        label1 = MarkupText("-135°", font="Segoe UI", font_size=14, color="#F472B6").move_to(axes.c2p(0.8, -0.8))
        self.play(Create(arc1), Write(label1))
        
        self.set_subtitle("This lands in the third quadrant. So, -135 degrees lies in Quadrant III.")
        q3_label = MarkupText("Quadrant III", font="Segoe UI", font_size=14, color="#F472B6").move_to(axes.c2p(-1.8, -1.8))
        self.play(Write(q3_label))
        self.wait(2.5)
        
        # Q1(b) Co-terminal angle
        self.set_subtitle("Question 1(b): Find another positive angle co-terminal with -135 degrees.")
        self.play(FadeOut(q3_label))
        
        arc_coterm = Arc(radius=0.9, start_angle=0, angle=225*DEGREES, arc_center=axes.c2p(0,0), color="#34D399", stroke_width=4)
        arc_coterm.add_tip(tip_length=0.1)
        label_coterm = MarkupText("225°", font="Segoe UI", font_size=14, color="#34D399").move_to(axes.c2p(-1.0, 0.8))
        
        self.set_subtitle("Rotating counterclockwise to the same terminal arm, we get 360 minus 135, which is 225 degrees.")
        self.play(Create(arc_coterm), Write(label_coterm))
        self.wait(3.0)
        
        # Reset and clean up for Q1(a)(ii) 740 degrees
        self.play(
            FadeOut(arc1), FadeOut(label1), FadeOut(arc_coterm), FadeOut(label_coterm),
            Rotate(terminal_arm, angle=135*DEGREES, about_point=axes.c2p(0,0))
        )
        
        self.set_subtitle("Question 1(a)(ii): Draw 740 degrees and find its quadrant.")
        self.wait(1.0)
        
        self.set_subtitle("Since 740 is positive, we rotate counterclockwise. 740 degrees is two full rounds of 360, plus 20 degrees.")
        self.play(Rotate(terminal_arm, angle=740*DEGREES, about_point=axes.c2p(0,0)), run_time=3.5, rate_func=linear)
        
        center_pt = axes.c2p(0,0)
        x_val = lambda t: center_pt[0] + (0.3 + 0.08 * t) * np.cos(t)
        y_val = lambda t: center_pt[1] + (0.3 + 0.08 * t) * np.sin(t)
        spiral = ParametricFunction(lambda t: np.array([x_val(t), y_val(t), 0]), t_range=[0, 740*DEGREES], color="#34D399", stroke_width=3)
        
        label_740 = MarkupText("740°", font="Segoe UI", font_size=14, color="#34D399").move_to(axes.c2p(1.2, 0.6))
        self.play(Create(spiral), Write(label_740))
        
        self.set_subtitle("This lands in the first quadrant. So, 740 degrees lies in Quadrant I.")
        q1_label = MarkupText("Quadrant I", font="Segoe UI", font_size=14, color="#34D399").move_to(axes.c2p(1.8, 1.8))
        self.play(Write(q1_label))
        self.wait(3.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(axes_grp, initial_arm, terminal_arm, spiral, label_740, q1_label, title)))
        self.wait(0.5)


class Q2Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 2: Angle Quadrant Analysis</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        # Quadrant Grid
        grid = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4, y_length=4, axis_config={"color": GRAY, "stroke_width": 2})
        grid.shift(RIGHT * 2 + DOWN * 0.4)
        
        q1 = MarkupText("I", font="Segoe UI", font_size=16, color=GRAY).move_to(grid.c2p(1, 1))
        q2 = MarkupText("II", font="Segoe UI", font_size=16, color="#22D3EE").move_to(grid.c2p(-1, 1))
        q3 = MarkupText("III", font="Segoe UI", font_size=16, color=GRAY).move_to(grid.c2p(-1, -1))
        q4 = MarkupText("IV", font="Segoe UI", font_size=16, color=GRAY).move_to(grid.c2p(1, -1))
        quads = VGroup(q1, q2, q3, q4)
        
        self.play(Create(grid), FadeIn(quads))
        
        self.set_subtitle("If θ lies in the second quadrant, then θ is between 90 degrees and 180 degrees.")
        
        info = VGroup(
            MarkupText("Given: θ lies in Q2", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("90° &lt; θ &lt; 180°", font="Segoe UI", font_size=18, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        
        self.play(Write(info))
        self.wait(2.5)
        
        # Sub-q (i) theta / 2
        self.set_subtitle("Part (i): For θ over 2, dividing the boundaries by 2 gives 45 degrees to 90 degrees.")
        
        ans_i = VGroup(
            MarkupText("<b>(i) θ / 2:</b>", font="Segoe UI", font_size=16, color="#34D399"),
            MarkupText("45° &lt; θ/2 &lt; 90°", font="Segoe UI", font_size=16, color="#E2E8F0"),
            MarkupText("→ Lies in <b>Quadrant I</b>", font="Segoe UI", font_size=16, color="#34D399")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(info, DOWN, buff=0.5).align_to(info, LEFT)
        
        q1_high = q1.copy().set_color("#34D399").scale(1.3)
        self.play(Write(ans_i), Transform(q1, q1_high))
        self.wait(3.0)
        
        # Sub-q (ii) 2*theta
        self.set_subtitle("Part (ii): For 2 θ, multiplying the boundaries by 2 gives 180 degrees to 360 degrees.")
        
        ans_ii = VGroup(
            MarkupText("<b>(ii) 2θ:</b>", font="Segoe UI", font_size=16, color="#F59E0B"),
            MarkupText("180° &lt; 2θ &lt; 360°", font="Segoe UI", font_size=16, color="#E2E8F0"),
            MarkupText("→ Lies in <b>Quadrant III or IV</b>", font="Segoe UI", font_size=16, color="#F59E0B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ans_i.get_center())
        
        q3_high = q3.copy().set_color("#F59E0B").scale(1.3)
        q4_high = q4.copy().set_color("#F59E0B").scale(1.3)
        
        self.play(
            FadeOut(ans_i),
            Transform(q1, q1.copy().set_color(GRAY).scale(1/1.3)),
            FadeIn(ans_ii),
            Transform(q3, q3_high),
            Transform(q4, q4_high)
        )
        self.wait(3.5)
        
        # Sub-q (iii) -theta
        self.set_subtitle("Part (iii): For negative θ, multiplying by minus 1 reverses the inequality, giving -180 to -90 degrees.")
        
        ans_iii = VGroup(
            MarkupText("<b>(iii) -θ:</b>", font="Segoe UI", font_size=16, color="#F472B6"),
            MarkupText("-180° &lt; -θ &lt; -90°", font="Segoe UI", font_size=16, color="#E2E8F0"),
            MarkupText("→ Lies in <b>Quadrant III</b>", font="Segoe UI", font_size=16, color="#F472B6")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ans_ii.get_center())
        
        self.play(
            FadeOut(ans_ii),
            Transform(q3, q3.copy().set_color(GRAY).scale(1/1.3)),
            Transform(q4, q4.copy().set_color(GRAY).scale(1/1.3)),
            FadeIn(ans_iii),
            Transform(q3, q3.copy().set_color("#F472B6").scale(1.3))
        )
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(grid, quads, q3, info, ans_iii, title)))
        self.wait(0.5)


class Q3Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 3: Degrees to Radians</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("To convert degrees to radians, we multiply the degree measure by pi over 180.")
        
        formula = MarkupText("Formula:  Radian = Degree × (π / 180)", font="Segoe UI", font_size=20, color="#F59E0B")
        formula.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(formula, shift=DOWN))
        self.wait(2.5)
        
        # Sub-q 1: 240
        self.set_subtitle("Part (i): Converting 240 degrees. We multiply 240 by pi over 180, which simplifies to 4 pi over 3 radians.")
        q1_text = MarkupText("<b>(i) 240°</b>  =  240 × (π / 180)  =  <b>4π / 3  rad</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q1_text.next_to(formula, DOWN, buff=0.6).to_edge(LEFT, buff=1.5)
        self.play(Write(q1_text))
        self.wait(3.5)
        
        # Sub-q 2: -315
        self.set_subtitle("Part (ii): Converting minus 315 degrees. Multiplying by pi over 180 simplifies to minus 7 pi over 4 radians.")
        q2_text = MarkupText("<b>(ii) -315°</b>  =  -315 × (π / 180)  =  <b>-7π / 4  rad</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q2_text.next_to(q1_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(q2_text))
        self.wait(3.5)
        
        # Sub-q 3: 570
        self.set_subtitle("Part (iii): Converting 570 degrees. Multiplying by pi over 180 simplifies to 19 pi over 6 radians.")
        q3_text = MarkupText("<b>(iii) 570°</b>  =  570 × (π / 180)  =  <b>19π / 6  rad</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q3_text.next_to(q2_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(q3_text))
        self.wait(3.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, formula, q1_text, q2_text, q3_text)))
        self.wait(0.5)


class Q4Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 4: Radians to Degrees</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("To convert radians to degrees, we multiply the radian measure by 180 over pi.")
        
        formula = MarkupText("Formula:  Degree = Radian × (180 / π)", font="Segoe UI", font_size=20, color="#F59E0B")
        formula.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(formula, shift=DOWN))
        self.wait(2.5)
        
        # Sub-q 1: 5pi/3
        self.set_subtitle("Part (i): Converting 5 pi over 3 radians. Multiplying by 180 over pi, pi cancels out, giving 300 degrees.")
        q1_text = MarkupText("<b>(i) 5π/3 rad</b>  =  (5π / 3) × (180 / π)  =  <b>300°</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q1_text.next_to(formula, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)
        self.play(Write(q1_text))
        self.wait(4.0)
        
        # Sub-q 2: 13pi/4
        self.set_subtitle("Part (ii): Converting 13 pi over 4 radians. Multiplying by 180 over pi simplifies to 585 degrees.")
        q2_text = MarkupText("<b>(ii) 13π/4 rad</b>  =  (13π / 4) × (180 / π)  =  <b>585°</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q2_text.next_to(q1_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(q2_text))
        self.wait(3.5)
        
        # Sub-q 3: -24pi/5
        self.set_subtitle("Part (iii): Converting minus 24 pi over 5 radians. Multiplying by 180 over pi yields minus 864 degrees.")
        q3_text = MarkupText("<b>(iii) -24π/5 rad</b>  =  (-24π / 5) × (180 / π)  =  <b>-864°</b>", font="Segoe UI", font_size=18, color="#E2E8F0")
        q3_text.next_to(q2_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(q3_text))
        self.wait(3.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, formula, q1_text, q2_text, q3_text)))
        self.wait(0.5)


class Q5Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 5: Degrees &amp; Minutes to Radians</b>", font="Segoe UI", font_size=26, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Recall that 1 degree equals 60 minutes. We must first convert the minutes to a fraction of a degree.")
        
        relation = MarkupText("Relation: 1° = 60' (Minutes)  →  1' = (1 / 60)°", font="Segoe UI", font_size=18, color="#F59E0B")
        relation.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(relation))
        self.wait(3.5)
        
        # Sub-q 3: 40 deg 20 min
        self.set_subtitle("Part (iii): Let's convert 40 degrees and 20 minutes. 20 minutes is 20 over 60 degrees, which is 1 over 3 degrees.")
        
        step1 = MarkupText("<b>(iii) 40° 20'</b> = (40 + 20/60)° = (40 + 1/3)° = <b>(121 / 3)°</b>", font="Segoe UI", font_size=16, color="#E2E8F0")
        step1.next_to(relation, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(Write(step1))
        self.wait(4.0)
        
        self.set_subtitle("Now multiply 121 over 3 degrees by pi over 180. This gives 121 pi over 540 radians.")
        step1_conv = MarkupText("Radian = (121 / 3) × (π / 180) = <b>121π / 540 rad</b>", font="Segoe UI", font_size=16, color="#34D399").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(Write(step1_conv))
        self.wait(4.5)
        
        # Sub-q 4: -37 deg 30 min
        self.set_subtitle("Part (iv): Convert minus 37 degrees and 30 minutes. 30 minutes is half a degree, giving minus 75 over 2 degrees.")
        
        step2 = MarkupText("<b>(iv) -37° 30'</b> = -(37 + 30/60)° = -(37 + 1/2)° = <b>-(75 / 2)°</b>", font="Segoe UI", font_size=16, color="#E2E8F0")
        step2.next_to(step1_conv, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(step2))
        self.wait(4.0)
        
        self.set_subtitle("Multiplying minus 75 over 2 degrees by pi over 180 simplifies to minus 5 pi over 24 radians.")
        step2_conv = MarkupText("Radian = -(75 / 2) × (π / 180) = <b>-5π / 24 rad</b>", font="Segoe UI", font_size=16, color="#F472B6").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(Write(step2_conv))
        self.wait(4.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, relation, step1, step1_conv, step2, step2_conv)))
        self.wait(0.5)


class Q6Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 6: Radians to Degrees, Minutes, &amp; Seconds</b>", font="Segoe UI", font_size=24, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("To convert radians to degrees, we multiply by 180 over pi. We will approximate pi as 22 over 7.")
        
        relation = MarkupText("Multiply by 180/π  (Use π ≈ 22/7)", font="Segoe UI", font_size=18, color="#F59E0B")
        relation.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(relation))
        self.wait(3.5)
        
        # Sub-q 1: 6 radians
        self.set_subtitle("Part (i): Convert 6 radians. Multiply 6 by 180, and then by 7 over 22, yielding approximately 343.636 degrees.")
        
        calc1 = MarkupText("6 rad = 6 × (180 / π) ≈ 6 × 180 × 7 / 22 = <b>(3780 / 11)° ≈ 343.636°</b>", font="Segoe UI", font_size=15, color="#E2E8F0")
        calc1.next_to(relation, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        self.play(Write(calc1))
        self.wait(4.5)
        
        self.set_subtitle("Let's convert the decimal part to minutes and seconds: 0.636 degrees times 60 is 38.18 minutes.")
        calc2 = MarkupText("• 0.636° × 60 = 38.18' (Minutes)", font="Segoe UI", font_size=15, color="#94A3B8").next_to(calc1, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(calc2))
        self.wait(3.5)
        
        self.set_subtitle("Next, 0.18 minutes times 60 is approximately 11 seconds. So, 6 radians is 343 degrees, 38 minutes, and 11 seconds.")
        calc3 = MarkupText("• 0.18' × 60 ≈ 11\" (Seconds)  →  <b>Answer: 343° 38' 11\"</b>", font="Segoe UI", font_size=15, color="#34D399").next_to(calc2, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(calc3))
        self.wait(4.5)
        
        # Sub-q 2: 3/4 radians
        self.set_subtitle("Part (ii): Convert 3 over 4 radians. Multiplying by 180 over pi gives approximately 42.95 degrees.")
        calc4 = MarkupText("3/4 rad = (3/4) × (180 × 7 / 22) ≈ <b>42.955°</b>", font="Segoe UI", font_size=15, color="#E2E8F0").next_to(calc3, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(calc4))
        self.wait(3.5)
        
        self.set_subtitle("Converting the decimal gives 42 degrees, 57 minutes, and 16 seconds.")
        calc5 = MarkupText("• 0.955° × 60 = 57.3'  →  0.3' × 60 = 18\"  →  <b>Answer: 42° 57' 16\"</b>", font="Segoe UI", font_size=15, color="#34D399").next_to(calc4, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(calc5))
        self.wait(4.5)
        
        # Sub-q 3: -3 radians
        self.set_subtitle("Part (iii): Convert minus 3 radians. The minus sign remains as is. Multiplying by 180 over pi gives approximately minus 171.818 degrees.")
        calc6 = MarkupText("-3 rad = -3 × (180 × 7 / 22) = <b>-(3780 / 22)° ≈ -171.818°</b>", font="Segoe UI", font_size=15, color="#E2E8F0").next_to(calc5, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(calc6))
        self.wait(4.5)
        
        self.set_subtitle("Converting the decimal part gives minus 171 degrees, 49 minutes, and 5 seconds.")
        calc7 = MarkupText("• 0.818° × 60 = 49.09'  →  0.09' × 60 ≈ 5\"  →  <b>Answer: -171° 49' 5\"</b>", font="Segoe UI", font_size=15, color="#34D399").next_to(calc6, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(calc7))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, relation, calc1, calc2, calc3, calc4, calc5, calc6, calc7)))
        self.wait(0.5)


class Q7Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 7: Wheel Revolutions</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: A wheel makes 360 revolutions in a minute. How many radians does it turn in one second?")
        
        desc = MarkupText("Revolutions: 360 rev / min", font="Segoe UI", font_size=18, color="#E2E8F0").next_to(title, DOWN, buff=0.5)
        self.play(Write(desc))
        self.wait(3.5)
        
        # Geometry: Rotating wheel
        circle = Circle(radius=1.5, color=GRAY, stroke_width=2).shift(RIGHT * 2.5 + DOWN * 0.5)
        spoke = Line(circle.get_center(), circle.get_center() + RIGHT * 1.5, color="#22D3EE", stroke_width=3)
        wheel = VGroup(circle, spoke)
        self.play(Create(wheel))
        
        self.set_subtitle("First, since one minute is 60 seconds, the wheel makes 360 divided by 60, which is 6 revolutions in one second.")
        
        step1 = MarkupText("In 1 second = 360 / 60 = <b>6 revolutions</b>", font="Segoe UI", font_size=18, color="#F59E0B").next_to(desc, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        self.play(Write(step1))
        self.wait(4.0)
        
        self.set_subtitle("In one full revolution, the wheel rotates through 360 degrees, which is 2 pi radians.")
        
        # Spin wheel once
        self.play(Rotate(wheel, angle=2*PI, about_point=circle.get_center()), run_time=2)
        
        step2 = MarkupText("1 revolution = 2π radians", font="Segoe UI", font_size=18, color="#E2E8F0").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.0)
        
        self.set_subtitle("Therefore, in six revolutions, the wheel turns 6 times 2 pi, which equals 12 pi radians.")
        
        step3 = MarkupText("6 revolutions = 6 × 2π = <b>12π radians</b>", font="Segoe UI", font_size=18, color="#34D399").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        
        # Spin wheel faster to show continuous rotation
        self.play(Rotate(wheel, angle=4*PI, about_point=circle.get_center()), run_time=1.5, rate_func=linear)
        self.wait(2.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, desc, wheel, step1, step2, step3)))
        self.wait(0.5)


class Q8Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 8: Pendulum Swing</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the angle in radians through which a pendulum swings if its length is 75 cm and arc length is 10 cm.")
        
        # Draw pendulum
        top = UP * 1.5 + RIGHT * 2.5
        rod = Line(top, top + DOWN * 2.5, color=GRAY, stroke_width=3)
        bob = Dot(point=rod.get_end(), color="#22D3EE", radius=0.15)
        pendulum = VGroup(rod, bob)
        
        self.play(Create(pendulum))
        
        # Animate swing
        self.play(Rotate(pendulum, angle=25*DEGREES, about_point=top), run_time=1)
        self.play(Rotate(pendulum, angle=-50*DEGREES, about_point=top), run_time=1.5)
        self.play(Rotate(pendulum, angle=25*DEGREES, about_point=top), run_time=1)
        
        self.set_subtitle("The length of the pendulum acts as the radius of the circle, r = 75 cm, and the tip describes an arc length, s = 10 cm.")
        
        info = VGroup(
            MarkupText("• Radius (r) = 75 cm", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("• Arc Length (s) = 10 cm", font="Segoe UI", font_size=18, color="#A78BFA")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        
        self.play(Write(info))
        self.wait(4.0)
        
        self.set_subtitle("Using the arc length formula, s equals r times theta, we solve for theta: s divided by r.")
        
        formula = MarkupText("Formula: s = r × θ  →  θ = s / r", font="Segoe UI", font_size=18, color="#F59E0B").next_to(info, DOWN, buff=0.5).align_to(info, LEFT)
        self.play(Write(formula))
        self.wait(3.5)
        
        self.set_subtitle("Plugging in 10 and 75, we simplify the fraction to 2 over 15 radians.")
        
        calc = MarkupText("θ = 10 / 75 = <b>2 / 15 rad</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        self.play(Write(calc))
        self.wait(3.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, pendulum, info, formula, calc)))
        self.wait(0.5)


class Q9Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 9: Radius from Arc Length</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the radius of a circle where a central angle of 45° makes an arc of length 187 cm. Use pi = 22/7.")
        
        # Text details
        info = VGroup(
            MarkupText("Given:", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("• Angle θ = 45°", font="Segoe UI", font_size=16, color="#E2E8F0"),
            MarkupText("• Arc Length s = 187 cm", font="Segoe UI", font_size=16, color="#A78BFA")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0)
        
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("First, convert 45 degrees to radians by multiplying by pi over 180. Using 22 over 7 for pi, we get 11 over 14 radians.")
        
        step1 = MarkupText("θ = 45 × (π / 180) = π / 4 rad\n   ≈ (1 / 4) × (22 / 7) = <b>11 / 14 rad</b>", font="Segoe UI", font_size=16, color="#F59E0B").next_to(info, DOWN, buff=0.4).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("Now substitute the arc length and theta into the formula: s equals r times theta.")
        
        step2 = MarkupText("s = r × θ  →  187 = r × (11 / 14)", font="Segoe UI", font_size=18, color="#E2E8F0").next_to(step1, DOWN, buff=0.4).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Solving for r, we multiply 187 by 14 and divide by 11. This simplifies to 17 times 14, which is 238 cm.")
        
        step3 = MarkupText("r = 187 × (14 / 11) = 17 × 14 = <b>238 cm</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step2, DOWN, buff=0.4).align_to(step2, LEFT)
        self.play(Write(step3))
        self.wait(4.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2, step3)))
        self.wait(0.5)


class Q10Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 10: Arc Length from Diameter</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the arc length of a circle of diameter 20 cm which subtends 45° at the center.")
        
        info = VGroup(
            MarkupText("Given:", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("• Diameter d = 20 cm  →  Radius r = 10 cm", font="Segoe UI", font_size=16, color="#22D3EE"),
            MarkupText("• Central Angle θ = 45°", font="Segoe UI", font_size=16, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0)
        
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("Converting the central angle: 45 degrees is pi over 4 radians.")
        
        step1 = MarkupText("θ = 45° × (π / 180) = <b>π / 4 rad</b>", font="Segoe UI", font_size=18, color="#F59E0B").next_to(info, DOWN, buff=0.4).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(3.0)
        
        self.set_subtitle("Now, apply the formula s equals r times theta. Substituting r equals 10 and theta equals pi over 4, we get 5 pi over 2 cm.")
        
        step2 = MarkupText("s = r × θ  =  10 × (π / 4)  =  <b>5π / 2 cm</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step1, DOWN, buff=0.4).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2)))
        self.wait(0.5)


class Q11Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 11: Railway Track Curved Angle</b>", font="Segoe UI", font_size=26, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: A train runs on a circular track of radius 1500 m at 60 km/h. Find the angle turned in 10 seconds.")
        
        info = VGroup(
            MarkupText("• Radius (r) = 1500 m", font="Segoe UI", font_size=16, color="#22D3EE"),
            MarkupText("• Speed = 60 km / h", font="Segoe UI", font_size=16, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("First, find the distance covered in 10 seconds. Convert speed to meters per second by multiplying by 5 over 18.")
        
        step1 = MarkupText("Speed = 60 × (5 / 18) = 50 / 3 m/s\nDistance (s) in 10s = (50 / 3) × 10 = <b>500 / 3 m</b>", font="Segoe UI", font_size=16, color="#F59E0B").next_to(info, DOWN, buff=0.3).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("Now, apply s equals r times theta. The angle theta is s divided by r, which yields 1 over 9 radians.")
        
        step2 = MarkupText("θ = s / r = (500 / 3) / 1500 = <b>1 / 9 rad</b>", font="Segoe UI", font_size=16, color="#E2E8F0").next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(4.0)
        
        self.set_subtitle("Finally, convert 1 over 9 radians to degrees by multiplying by 180 over pi. This simplifies to 20 over pi degrees.")
        
        step3 = MarkupText("θ = (1 / 9) × (180 / π) = <b>(20 / π)°</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step2, DOWN, buff=0.3).align_to(step2, LEFT)
        self.play(Write(step3))
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2, step3)))
        self.wait(0.5)


class Q12Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 12: Ratio of Radii</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: If arcs of same length subtend 65° and 110° at the centers of two circles, find the ratio of their radii.")
        
        info = VGroup(
            MarkupText("Given: Arc lengths are equal (s₁ = s₂)", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("• θ₁ = 65°  and  θ₂ = 110°", font="Segoe UI", font_size=18, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("Using the formula s equals r times theta, we can set r1 times theta1 equal to r2 times theta2.")
        
        step1 = MarkupText("r₁ × θ₁ = r₂ × θ₂  →  r₁ / r₂ = θ₂ / θ₁", font="Segoe UI", font_size=18, color="#F59E0B").next_to(info, DOWN, buff=0.5).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(3.5)
        
        self.set_subtitle("Therefore, the ratio of the radii is 110 divided by 65, which simplifies to 22 over 13.")
        
        step2 = MarkupText("r₁ / r₂ = 110° / 65° = 22 / 13\n\n<b>Ratio  r₁ : r₂ = 22 : 13</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step1, DOWN, buff=0.5).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2)))
        self.wait(0.5)


class Q13Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 13: Clock Hand Movement</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: The large hand of a clock is 21 cm long. How much distance does its extremity move in 20 minutes?")
        
        # Clock Face
        circle = Circle(radius=1.8, color=GRAY, stroke_width=2).shift(RIGHT * 2.5 + DOWN * 0.4)
        center = Dot(circle.get_center(), color=WHITE)
        hand = Line(circle.get_center(), circle.get_center() + UP * 1.6, color="#22D3EE", stroke_width=4)
        self.play(Create(circle), Create(center), Create(hand))
        
        self.set_subtitle("In 20 minutes, the minute hand covers 1 over 3 of a full rotation, which corresponds to 120 degrees or 2 pi over 3 radians.")
        
        step1 = MarkupText("In 20 mins, fraction = 20 / 60 = 1 / 3\nθ = (1 / 3) × 2π = <b>2π / 3 rad</b>", font="Segoe UI", font_size=18, color="#F59E0B").to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        self.play(Write(step1))
        
        # Rotate minute hand
        self.play(Rotate(hand, angle=-120*DEGREES, about_point=circle.get_center()), run_time=2)
        self.wait(1.5)
        
        self.set_subtitle("Using s equals r times theta, we multiply the radius 21 by 2 pi over 3, which simplifies to 14 pi.")
        
        step2 = MarkupText("s = r × θ  =  21 × (2π / 3) = 14π", font="Segoe UI", font_size=18, color="#E2E8F0").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Substituting 22 over 7 for pi, the distance moved by the tip is exactly 44 cm.")
        
        step3 = MarkupText("s ≈ 14 × (22 / 7) = 2 × 22 = <b>44 cm</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, circle, center, hand, step1, step2, step3)))
        self.wait(0.5)


class Q13SceneWhiteboard(WhiteboardSubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 13: Clock Hand Movement</b>", font="Segoe Print", font_size=26, color="#1E293B")
        title.to_edge(UP, buff=0.4)
        divider = Line(LEFT * 6, RIGHT * 6, color="#CBD5E1", stroke_width=2).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Create(divider))
        
        self.set_subtitle("Problem: The large hand of a clock is 21 cm long. How much distance does its extremity move in 20 minutes?")
        
        # Clock Face
        circle = Circle(radius=1.8, color="#334155", stroke_width=4).shift(RIGHT * 2.5 + DOWN * 0.4)
        center = Dot(circle.get_center(), color="#334155", radius=0.08)
        
        # Add tick marks for 12 hours
        ticks = VGroup()
        for i in range(12):
            angle = i * 30 * DEGREES
            start = circle.get_center() + np.array([1.65 * np.sin(angle), 1.65 * np.cos(angle), 0])
            end = circle.get_center() + np.array([1.8 * np.sin(angle), 1.8 * np.cos(angle), 0])
            tick = Line(start, end, color="#475569", stroke_width=2.5)
            ticks.add(tick)
            
        hand = Line(circle.get_center(), circle.get_center() + UP * 1.6, color="#2563EB", stroke_width=5)
        
        self.play(Create(circle), Create(ticks), Create(center), Create(hand))
        
        self.set_subtitle("In 20 minutes, the minute hand covers 1 over 3 of a full rotation, which corresponds to 120 degrees or 2 pi over 3 radians.")
        
        step1 = MarkupText(
            "In 20 mins, fraction = 20 / 60 = 1 / 3\n"
            "θ = (1 / 3) × 2π = <span foreground='#D97706'><b>2π / 3 rad</b></span>",
            font="Segoe Print", font_size=16, color="#1E293B"
        ).to_edge(LEFT, buff=0.8).shift(UP * 0.5)
        self.play(Write(step1))
        
        # Arc showing the path of the hand's tip
        path_arc = Arc(
            radius=1.6,
            start_angle=90*DEGREES,
            angle=-120*DEGREES,
            arc_center=circle.get_center(),
            color="#EF4444",
            stroke_width=4
        )
        arc_label = MarkupText("s", font="Segoe Print", font_size=18, color="#EF4444").next_to(path_arc.point_from_proportion(0.5), UP+RIGHT, buff=0.1)
        
        # Rotate minute hand and draw arc path
        self.play(
            Rotate(hand, angle=-120*DEGREES, about_point=circle.get_center()),
            Create(path_arc),
            run_time=2.5
        )
        self.play(Write(arc_label))
        self.wait(1.5)
        
        self.set_subtitle("Using s equals r times theta, we multiply the radius 21 by 2 pi over 3, which simplifies to 14 pi.")
        
        step2 = MarkupText(
            "s = r × θ  =  21 × (2π / 3) = 14π",
            font="Segoe Print", font_size=16, color="#1E293B"
        ).next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Substituting 22 over 7 for pi, the distance moved by the tip is exactly 44 cm.")
        
        step3 = MarkupText(
            "s ≈ 14 × (22 / 7) = 2 × 22 = <span foreground='#059669'><b>44 cm</b></span>",
            font="Segoe Print", font_size=18, color="#1E293B"
        ).next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        self.wait(4.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, divider, circle, ticks, center, hand, path_arc, arc_label, step1, step2, step3)))
        self.wait(0.5)


class Q14Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 14: Pendulum Angle in Degrees</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the angle in degrees through which a pendulum swings if its length is 50 cm and arc length is 10 cm.")
        
        info = VGroup(
            MarkupText("Given: Radius r = 50 cm, Arc Length s = 10 cm", font="Segoe UI", font_size=18, color="#22D3EE")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, buff=0.5)
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("First, calculate the angle in radians. Theta is s divided by r, which is 10 over 50, or 1 over 5 radians.")
        
        step1 = MarkupText("θ = s / r = 10 / 50 = <b>1 / 5 rad</b>", font="Segoe UI", font_size=18, color="#F59E0B").next_to(info, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(Write(step1))
        self.wait(3.5)
        
        self.set_subtitle("Convert to degrees: multiply 1 over 5 by 180 over pi. This gives 36 over pi degrees.")
        
        step2 = MarkupText("θ = (1 / 5) × (180 / π) = <b>(36 / π)°</b>", font="Segoe UI", font_size=18, color="#E2E8F0").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Using pi as 22 over 7, the result is approximately 11.45 degrees, which converts to 11 degrees, 27 minutes, and 16 seconds.")
        
        step3 = MarkupText("θ ≈ 36 × (7 / 22) = (126 / 11)° ≈ 11.4545°\n\n<b>Answer: 11° 27' 16\"</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2, step3)))
        self.wait(0.5)


class Q15Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 15: Arc Length Calculation</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the length of an arc of a circle of radius 75 cm that spans a central angle of 126 degrees. Take pi = 3.1416.")
        
        info = VGroup(
            MarkupText("Given: Radius r = 75 cm, θ = 126°, π = 3.1416", font="Segoe UI", font_size=18, color="#22D3EE")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, buff=0.5)
        self.play(Write(info))
        self.wait(3.5)
        
        self.set_subtitle("Convert the angle to radians: multiply 126 by pi over 180.")
        
        step1 = MarkupText("θ = 126 × (π / 180) = 0.7π rad", font="Segoe UI", font_size=18, color="#F59E0B").next_to(info, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(Write(step1))
        self.wait(3.0)
        
        self.set_subtitle("Now, apply s equals r times theta. Substituting 75 for radius and using 3.1416 for pi, we get 164.934 cm.")
        
        step2 = MarkupText("s = r × θ = 75 × 126 × (3.1416 / 180)\n\n<b>Answer: 164.934 cm</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(4.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2)))
        self.wait(0.5)


class Q16Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 16: Angle at 3:30</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Find the angle in radians between the hands of a clock at 3:30.")
        
        # Clock Drawing
        circle = Circle(radius=1.8, color=GRAY, stroke_width=2).shift(RIGHT * 2.5 + DOWN * 0.4)
        center = Dot(circle.get_center(), color=WHITE)
        min_hand = Line(circle.get_center(), circle.get_center() + DOWN * 1.6, color="#22D3EE", stroke_width=4) # at 6
        # at 3:30, hour hand is exactly halfway between 3 and 4
        angle_hour = -3.5 * 30 * DEGREES
        hour_hand = Line(circle.get_center(), circle.get_center() + np.array([1.2 * np.cos(angle_hour + 90*DEGREES), 1.2 * np.sin(angle_hour + 90*DEGREES), 0]), color="#F59E0B", stroke_width=4)
        
        self.play(Create(circle), Create(center), Create(min_hand), Create(hour_hand))
        
        self.set_subtitle("At 3:30, the minute hand is at 6, and the hour hand is exactly halfway between 3 and 4.")
        self.wait(3.5)
        
        self.set_subtitle("The angle between consecutive clock markings is 30 degrees. The markings between the hands are 3.5 to 4, 4 to 5, and 5 to 6.")
        
        step1 = MarkupText("Angle = (Half division from 3 to 4) + (2 full divisions)\n          = 15° + 30° + 30° = <b>75°</b>", font="Segoe UI", font_size=16, color="#F59E0B").to_edge(LEFT, buff=0.8).shift(UP * 0.5)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("To express this in radians, multiply 75 by pi over 180. Simplifying the fraction gives 5 pi over 12 radians.")
        
        step2 = MarkupText("Radian = 75 × (π / 180)  =  <b>5π / 12 rad</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(step2))
        self.wait(4.5)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, circle, center, min_hand, hour_hand, step1, step2)))
        self.wait(0.5)


class Q17Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 17: Third Angle of a Triangle</b>", font="Segoe UI", font_size=26, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Two angles of a triangle are 1/2 and 1/3 radians. Find the third angle in degrees.")
        
        info = VGroup(
            MarkupText("Given: A = 1/2 rad,  B = 1/3 rad", font="Segoe UI", font_size=18, color="#22D3EE"),
            MarkupText("Find: Third angle C in degrees. (Use π ≈ 22/7)", font="Segoe UI", font_size=16, color="#E2E8F0")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        
        self.play(Write(info))
        self.wait(4.0)
        
        self.set_subtitle("First, find the sum of the two given angles in degrees. Multiply the sum of 1/2 and 1/3 by 180 over pi.")
        
        step1 = MarkupText("A + B = 1/2 + 1/3 = 5/6 rad\nSum in Degrees = (5/6) × (180 / π) = 150 / π degrees", font="Segoe UI", font_size=16, color="#F59E0B").next_to(info, DOWN, buff=0.3).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("Using 22 over 7 for pi, the sum of these two angles is approximately 47.73 degrees.")
        
        step2 = MarkupText("Sum ≈ 150 × (7 / 22) = 1050 / 22 ≈ 47.727°", font="Segoe UI", font_size=16, color="#E2E8F0").next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(4.0)
        
        self.set_subtitle("Since the sum of angles in a triangle is 180 degrees, the third angle C is 180 minus 47.73, which is 132 degrees, 16 minutes, and 22 seconds.")
        
        step3 = MarkupText("C = 180° - 47.727° = 132.273°\n\n<b>Answer: 132° 16' 22\"</b>", font="Segoe UI", font_size=20, color="#34D399").next_to(step2, DOWN, buff=0.3).align_to(step2, LEFT)
        self.play(Write(step3))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2, step3)))
        self.wait(0.5)


class Q18Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 18: Acute Angles of Right Triangle</b>", font="Segoe UI", font_size=26, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: The difference between two acute angles of a right-angled triangle is pi over 5 radians. Find the angles in degrees.")
        
        # Right Triangle Drawing
        tri = Polygon(LEFT * 1 + DOWN * 1.5, RIGHT * 2 + DOWN * 1.5, LEFT * 1 + UP * 1.0, color=GRAY, stroke_width=2).shift(RIGHT * 2)
        self.play(Create(tri))
        
        self.set_subtitle("Let the two acute angles be A and C. Their difference is pi over 5 radians, which is 36 degrees.")
        
        step1 = MarkupText("Difference: A - C = π / 5 rad\n                 = 180° / 5 = <b>36°</b>", font="Segoe UI", font_size=16, color="#F59E0B").to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("Since the triangle is right-angled, the sum of the two acute angles is exactly 90 degrees.")
        
        step2 = MarkupText("Sum: A + C = <b>90°</b>", font="Segoe UI", font_size=16, color="#E2E8F0").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Solving this system of equations, adding them gives twice A equals 126, so A is 63 degrees. Subtracting gives C equals 27 degrees.")
        
        step3 = MarkupText("Adding: 2A = 126°  →  <b>A = 63°</b>\nSubtracting: 2C = 54°  →  <b>C = 27°</b>\n\n<b>Answer: The angles are 63° and 27°</b>", font="Segoe UI", font_size=18, color="#34D399").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, tri, step1, step2, step3)))
        self.wait(0.5)


class Q19Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 19: Triangle Angles in A.P.</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: The angles of a triangle are in Arithmetic Progression, and the greatest angle is double the least. Find them in radians.")
        
        self.wait(1.5)
        
        self.set_subtitle("Let the angles be A, B, and C. Since they are in A.P., the middle angle B is exactly 60 degrees.")
        
        step1 = MarkupText("Angles in A.P. → B = (A + C) / 2\nA + B + C = 180°  →  3B = 180°  →  <b>B = 60°</b>", font="Segoe UI", font_size=16, color="#F59E0B").to_edge(LEFT, buff=1.0).shift(UP * 0.8)
        self.play(Write(step1))
        self.wait(4.5)
        
        self.set_subtitle("The greatest angle C is double the least angle A, so C equals 2A.")
        
        step2 = MarkupText("Greatest is double the least: <b>C = 2A</b>", font="Segoe UI", font_size=16, color="#E2E8F0").next_to(step1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step2))
        self.wait(3.5)
        
        self.set_subtitle("Substituting C equals 2A into A + B + C = 180, we find A is 40 degrees, and C is 80 degrees.")
        
        step3 = MarkupText("A + 60° + 2A = 180°\n3A = 120°  →  <b>A = 40°</b>\nC = 2 × 40°  →  <b>C = 80°</b>", font="Segoe UI", font_size=16, color="#E2E8F0").next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step3))
        self.wait(4.5)
        
        self.set_subtitle("Converting the angles to radians: 40 degrees is 2 pi over 9, 60 degrees is pi over 3, and 80 degrees is 4 pi over 9.")
        
        step4 = MarkupText("Convert to Radians:\n• A = 40 × (π/180) = <b>2π / 9 rad</b>\n• B = 60 × (π/180) = <b>π / 3 rad</b>\n• C = 80 × (π/180) = <b>4π / 9 rad</b>", font="Segoe UI", font_size=16, color="#34D399").next_to(step3, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(step4))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, step1, step2, step3, step4)))
        self.wait(0.5)


class Q20Scene(SubtitledScene):
    def construct(self):
        title = MarkupText("<b>Question 20: Diameter of the Sun</b>", font="Segoe UI", font_size=28, color="#22D3EE")
        title.to_edge(UP)
        self.play(Write(title))
        
        self.set_subtitle("Problem: Estimate the diameter of the sun if it subtends an angle of 32 minutes at the observer's eye, at a distance of 91 million km.")
        
        info = VGroup(
            MarkupText("Distance (Radius r) = 91 × 10⁶ km", font="Segoe UI", font_size=16, color="#22D3EE"),
            MarkupText("Subtended Angle θ = 32' (Minutes)", font="Segoe UI", font_size=16, color="#A78BFA")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        self.play(Write(info))
        self.wait(4.5)
        
        self.set_subtitle("Convert 32 minutes to radians: first divide by 60 to get degrees, then multiply by pi over 180. Using 22 over 7 for pi, we get 44 over 4725 radians.")
        
        step1 = MarkupText("θ = (32 / 60)° = (8 / 15)°\nθ = (8 / 15) × (π / 180) rad\n   ≈ (8 / 15) × (22 / (7 × 180)) = <b>44 / 4725 rad</b>", font="Segoe UI", font_size=15, color="#F59E0B").next_to(info, DOWN, buff=0.3).align_to(info, LEFT)
        self.play(Write(step1))
        self.wait(5.0)
        
        self.set_subtitle("Since the sun is very far, its diameter is approximately the arc length s. Using s equals r times theta, we multiply 91 million by 44 over 4725.")
        
        step2 = MarkupText("Diameter (s) = r × θ\n                    = (91 × 10⁶) × (44 / 4725)\n                    ≈ <b>847,407.4 km</b>", font="Segoe UI", font_size=18, color="#34D399").next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        self.play(Write(step2))
        self.wait(5.0)
        
        self.clear_subtitle()
        self.play(FadeOut(VGroup(title, info, step1, step2)))
        self.wait(0.5)
