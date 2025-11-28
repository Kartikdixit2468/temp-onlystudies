"""
Anti Gravity - Voiceover Backend

This module extends the Artist class to generate VoiceoverScene code
with integrated voice narration using manim-voiceover and SoX.
"""

import os
import subprocess
import shutil
import google.generativeai as genai
from dotenv import load_dotenv
import time
from google.api_core import exceptions

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ===== Voice Configuration Presets =====

VOICE_PRESETS = {
    "teaching_assistant": {
        "description": "Friendly, energetic teaching assistant",
        "sox_effects": ["pitch", "100", "tempo", "1.1", "treble", "3"],
    },
    "professor": {
        "description": "Authoritative, calm professor",
        "sox_effects": ["pitch", "-50", "tempo", "0.95", "bass", "2"],
    },
    "enthusiastic": {
        "description": "Very cheerful and exciting",
        "sox_effects": ["pitch", "200", "tempo", "1.2", "treble", "5"],
    },
    "calm": {
        "description": "Soothing and relaxed",
        "sox_effects": ["pitch", "50", "tempo", "0.9"],
    },
    "neutral": {
        "description": "Standard voice without effects",
        "sox_effects": [],
    }
}

def get_model(quality):
    """Get AI model based on quality setting."""
    if quality == "High":
        return genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    elif quality == "Medium":
        return genai.GenerativeModel('gemini-2.0-flash')
    else:
        return genai.GenerativeModel('gemini-2.0-flash-lite')

def check_sox_available():
    """Check if SoX is available in system PATH."""
    return shutil.which("sox") is not None

class VoiceoverArtist:
    """Enhanced Artist class for generating VoiceoverScene code."""
    
    @staticmethod
    def generate_voiceover_scene(
        topic, 
        subject, 
        quality="Medium",
        voice_preset="teaching_assistant",
        use_sox=True
    ):
        """
        Generate a VoiceoverScene with narration instead of text captions.
        
        Args:
            topic: The educational topic to explain
            subject: Subject area (Math, Physics, etc.)
            quality: AI model quality (Low/Medium/High)
            voice_preset: Voice character preset (see VOICE_PRESETS)
            use_sox: Whether to use SoX effects (auto-detected if True)
        
        Returns:
            str: Python code for VoiceoverScene
        """
        # Check SoX availability
        sox_available = check_sox_available() if use_sox else False
        sox_effects = VOICE_PRESETS.get(voice_preset, VOICE_PRESETS["neutral"])["sox_effects"]
        
        model = get_model(quality)
        
        # Build SoX effects string for the prompt
        if sox_available and sox_effects:
            sox_config = f'sox_effects={sox_effects}'
        else:
            sox_config = ''
        
        # Few-shot examples to ground the model
        FEW_SHOT_EXAMPLES = """
        Example 1:
        Topic: "The Circle"
        Code:
        ```python
        class SceneTopic(VoiceoverScene):
            def construct(self):
                self.set_speech_service(GTTSService(lang="en", tld="com"))
                
                with self.voiceover(text="This is a circle. It is the set of all points equidistant from a center."):
                    circle = Circle(radius=2, color=BLUE)
                    center = Dot(color=RED)
                    self.play(Create(circle), Create(center))
                    
                with self.voiceover(text="The distance from the center to the edge is called the radius."):
                    line = Line(center.get_center(), circle.get_right(), color=YELLOW)
                    label = Text("Radius", font_size=24).next_to(line, UP)
                    self.play(Create(line), Write(label))
        ```

        Example 2:
        Topic: "Bubble Sort"
        Code:
        ```python
        class SceneTopic(VoiceoverScene):
            def construct(self):
                self.set_speech_service(GTTSService(lang="en", tld="com"))

                # Create array elements
                values = [4, 2, 5, 1, 3]
                squares = VGroup()
                for i, val in enumerate(values):
                    sq = Square(side_length=1, color=BLUE)
                    num = Text(str(val)).move_to(sq.get_center())
                    group = VGroup(sq, num)
                    squares.add(group)
                
                # Arrange nicely
                squares.arrange(RIGHT, buff=0.5)
                
                with self.voiceover(text="We start with an unsorted array."):
                    self.play(Create(squares))
                
                # Demonstrate Swap (CRITICAL: Use move_to and update list)
                with self.voiceover(text="The first two elements are out of order, so we swap them."):
                    # Highlight
                    self.play(squares[0].animate.set_color(RED), squares[1].animate.set_color(RED))
                    
                    # Swap positions visually
                    self.play(
                        squares[0].animate.move_to(squares[1].get_center()),
                        squares[1].animate.move_to(squares[0].get_center())
                    )
                    
                    # Update VGroup list to match visual state
                    squares.submobjects[0], squares.submobjects[1] = squares.submobjects[1], squares.submobjects[0]
                    
                    # Reset color
                    self.play(squares[0].animate.set_color(BLUE), squares[1].animate.set_color(BLUE))
        ```

        Example 3:
        Topic: "Pythagorean Theorem"
        Code:
        ```python
        class SceneTopic(VoiceoverScene):
            def construct(self):
                self.set_speech_service(GTTSService(lang="en", tld="com"))
                
                with self.voiceover(text="The Pythagorean theorem relates the sides of a right triangle."):
                    # Create triangle points
                    p1 = [-1, -1, 0]
                    p2 = [2, -1, 0]
                    p3 = [2, 1, 0]
                    
                    # Draw triangle
                    triangle = Polygon(p1, p2, p3, color=WHITE)
                    self.play(Create(triangle))
                    
                    # Add labels (Use next_to for safety)
                    a_label = Text("a").next_to(Line(p2, p3), RIGHT, buff=0.2)
                    b_label = Text("b").next_to(Line(p1, p2), DOWN, buff=0.2)
                    c_label = Text("c").next_to(Line(p1, p3), UP, buff=0.2)
                    
                    self.play(Write(a_label), Write(b_label), Write(c_label))
                    
                with self.voiceover(text="The square of the hypotenuse equals the sum of squares of the other two sides."):
                    equation = Text("a² + b² = c²", font_size=48).to_edge(UP)
                    self.play(Write(equation))
        ```
        """

        prompt = f"""
        CONTEXT: Generate a VoiceoverScene for Manim with voice narration.
        
        TOPIC TO EXPLAIN: "{topic}"
        SUBJECT AREA: {subject}
        
        Type: Educational animation with AI-generated voiceover.
        
        CRITICAL INSTRUCTIONS:
        1. Use VoiceoverScene instead of Scene
        2. Use `with self.voiceover(text="...")` blocks for narration
        3. DO NOT display text captions - use voice narration instead
        4. Synchronize animations with voiceover blocks
        5. Keep narration concise and natural-sounding
        6. **AVOID OVERLAPPING**: Use `.next_to(target, DIRECTION)` or `.shift(VECTOR)` to place elements.
        7. **CLEANUP**: FadeOut elements before introducing new conflicting ones.
        8. **CRITICAL**: Do NOT use `SVGMobject`, `ImageMobject`, or any external assets. Use ONLY built-in Manim shapes (Circle, Square, Line, Polygon, etc.).
        
        Visual Style:
        - Aesthetic: "Kurzgesagt" or "Vox" style. Flat vector art. Minimalist design.
        - Background: Solid, clean, dark background (charcoal or deep blue)
        - Focus on visuals: shapes, diagrams, animations (not text)
        - Motion: Smooth, clean animations that sync with voice
        
        {FEW_SHOT_EXAMPLES}

        Scene Structure (All narrated, minimal text):
        
        1. Introduction (15-20 seconds)
           - Voiceover introduces the topic
           - Show title briefly, then focus on visuals
        
        2. Concept Explanation (20-25 seconds)
           - Voiceover explains the core concept
           - Visual diagrams and shapes demonstrate the idea
           - Use colors to highlight key elements
        
        3. Practical Example (20-25 seconds)
           - Voiceover walks through a concrete example
           - If algorithm: animate the process with colored elements
           - If math: show step-by-step visual solution
           - If science: demonstrate the phenomenon
        
        4. Conclusion (5-10 seconds)
           - Brief voiceover summary
           - Clean visual wrap-up
        
        Code Requirements:
        - Class name: 'SceneTopic'
        - Inherit from: VoiceoverScene
        - Import: from manim import *
        - Import: from manim_voiceover import VoiceoverScene
        - Import: from manim_voiceover.services.gtts import GTTSService
        
        - In construct(), first set up the voice service:
          ```python
          self.set_speech_service(
              GTTSService(
                  lang="en",
                  tld="com",
                  {sox_config}
              )
          )
          ```
        
        - Use voiceover blocks:
          ```python
          with self.voiceover(text="Your narration here"):
              self.play(Animation(...))
          ```
        
        - Duration: Total 60+ seconds of animation
        - DO NOT use MathTex or LaTeX - use simple Text for any necessary labels
        - Focus on VISUALS, not text - let the voice do the explaining
        
        Output ONLY the Python code. No markdown, no explanations.
        """
        
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                code = response.text.replace("```python", "").replace("```", "").strip()
                return code
            except exceptions.ResourceExhausted:
                print(f"Quota exceeded on attempt {attempt + 1}. Switching to fallback...")
                model = genai.GenerativeModel('gemini-2.0-flash-lite')
                time.sleep(2)
            except Exception as e:
                return f"# Error: {e}"
        
        return "# Error: Failed to generate code after retries"

    @staticmethod
    def regenerate_video_code(original_code, feedback, topic, subject, quality="Medium"):
        """
        Regenerate the video code based on user feedback.
        """
        model = get_model(quality)
        
        prompt = f"""
        CONTEXT: You are fixing/improving a Python script for Manim (VoiceoverScene) based on USER FEEDBACK.
        
        TOPIC: "{topic}"
        SUBJECT: "{subject}"
        
        THE ORIGINAL CODE:
        ```python
        {original_code}
        ```
        
        USER FEEDBACK (The user disliked the previous video because):
        "{feedback}"
        
        INSTRUCTIONS:
        1. Analyze the original code and the user's feedback.
        2. Modify the code to ADDRESS the feedback specifically.
        3. Ensure the core logic still explains the topic correctly.
        4. Keep the same visual style (Kurzgesagt/Vox, dark background, flat vector).
        5. Ensure all imports and setup (Voiceover, SoX) remain correct.
        6. **CRITICAL**: Do NOT use `SVGMobject` or `ImageMobject`. Use ONLY built-in shapes.
        7. Output ONLY the fixed Python code. No markdown.
        """
        
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                code = response.text.replace("```python", "").replace("```", "").strip()
                return code
            except exceptions.ResourceExhausted:
                print(f"Quota exceeded on attempt {attempt + 1}. Switching to fallback...")
                model = genai.GenerativeModel('gemini-2.0-flash-lite')
                time.sleep(2)
            except Exception as e:
                return f"# Error: {e}"
        
        return "# Error: Failed to regenerate code after retries"

    @staticmethod
    def fix_code(original_code, error_message, topic, quality="Medium"):
        """
        Attempt to fix the generated code based on the Manim error message.
        """
        model = get_model(quality)
        
        prompt = f"""
        CONTEXT: You are fixing a Python script for Manim (VoiceoverScene).
        
        TOPIC: "{topic}"
        
        THE CODE THAT FAILED:
        ```python
        {original_code}
        ```
        
        THE ERROR MESSAGE:
        {error_message}
        
        INSTRUCTIONS:
        1. Analyze the error message to understand what went wrong.
        2. Fix the code to resolve the error.
        3. Ensure the logic still explains the topic correctly.
        4. **CRITICAL**: Do NOT use `SVGMobject` or `ImageMobject`. Use ONLY built-in shapes.
        5. Output ONLY the fixed Python code. No markdown.
        """
        
        try:
            response = model.generate_content(prompt)
            code = response.text.replace("```python", "").replace("```", "").strip()
            return code
        except Exception as e:
            return f"# Error fixing code: {e}"
    
    @staticmethod
    def list_voice_presets():
        """List available voice presets with descriptions."""
        print("\nAvailable Voice Presets:")
        print("=" * 60)
        for preset_name, preset_data in VOICE_PRESETS.items():
            print(f"\n{preset_name}:")
            print(f"  Description: {preset_data['description']}")
            print(f"  SoX Effects: {preset_data['sox_effects']}")
        print("\n" + "=" * 60)

# ===== Example Usage =====

if __name__ == "__main__":
    # Check SoX installation
    print("Checking SoX installation...")
    if check_sox_available():
        print("✓ SoX is available")
    else:
        print("⚠ SoX not found - voice will be generated without effects")
        print("  Run check_sox.py for installation instructions")
    
    print()
    
    # List available voice presets
    VoiceoverArtist.list_voice_presets()
    
    print("\nExample Usage:")
    print("-" * 60)
    print("""
# Generate voiceover scene
from voiceover_backend import VoiceoverArtist

code = VoiceoverArtist.generate_voiceover_scene(
    topic="Bubble Sort",
    subject="Computer Science",
    quality="Medium",
    voice_preset="teaching_assistant",
    use_sox=True
)

# Save and render
with open("temp_voiceover.py", "w", encoding="utf-8") as f:
    f.write(code)

# Render with Manim
import subprocess
subprocess.run(["manim", "-pql", "temp_voiceover.py", "SceneTopic"])
    """)
