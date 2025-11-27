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
        
        prompt = f"""
        CONTEXT: Generate a VoiceoverScene for Manim with voice narration instead of text captions.
        
        TOPIC TO EXPLAIN: "{topic}"
        SUBJECT AREA: {subject}
        
        Type: Educational animation with AI-generated voiceover.
        
        CRITICAL INSTRUCTIONS:
        1. Use VoiceoverScene instead of Scene
        2. Use `with self.voiceover(text="...")` blocks for narration
        3. DO NOT display text captions - use voice narration instead
        4. Synchronize animations with voiceover blocks
        5. Keep narration concise and natural-sounding
        
        Visual Style:
        - Aesthetic: "Kurzgesagt" or "Vox" style. Flat vector art. Minimalist design.
        - Background: Solid, clean, dark background (charcoal or deep blue)
        - Focus on visuals: shapes, diagrams, animations (not text)
        - Motion: Smooth, clean animations that sync with voice
        
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
                print(f"Quota exceeded on attempt {{attempt + 1}}. Switching to fallback...")
                model = genai.GenerativeModel('gemini-2.0-flash-lite')
                time.sleep(2)
            except Exception as e:
                return f"# Error: {e}"
        
        return "# Error: Failed to generate code after retries"
    
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
