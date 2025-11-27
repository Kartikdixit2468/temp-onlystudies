"""
Anti Gravity - Teaching Assistant Voice Integration Example

This example demonstrates how to create a VoiceoverScene with:
1. GTTSService for text-to-speech generation
2. SoX integration for audio post-processing (pitch/tempo/tone)
3. Error detection for missing SoX installation
4. Voice character configuration for a friendly Teaching Assistant
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import subprocess
import shutil

class AssistantIntro(VoiceoverScene):
    """
    Example scene where the Teaching Assistant introduces itself.
    Uses SoX to modify the voice for a friendly, engaging character.
    """
    
    def construct(self):
        # ===== SoX Detection & Configuration =====
        sox_available = self.check_sox_installation()
        
        if sox_available:
            # SoX is available - configure voice processing
            self.configure_voice_service_with_sox()
        else:
            # SoX not found - use basic voice without processing
            self.configure_voice_service_basic()
        
        # ===== Animation with Voiceover =====
        
        # Title
        title = Text("Anti Gravity", font_size=60, color=BLUE)
        subtitle = Text("Your AI Teaching Assistant", font_size=30, color=WHITE)
        subtitle.next_to(title, DOWN)
        
        # Voiceover: Introduction
        with self.voiceover(text="Hello! I'm your Anti Gravity teaching assistant."):
            self.play(Write(title), run_time=2)
            self.play(FadeIn(subtitle), run_time=1)
        
        self.wait(1)
        
        # Voiceover: Purpose
        with self.voiceover(text="I'm here to make learning fun and interactive through animations."):
            self.play(
                title.animate.scale(0.7).to_edge(UP),
                FadeOut(subtitle)
            )
        
        # Create some visual elements
        circle = Circle(radius=1, color=YELLOW)
        square = Square(side_length=2, color=GREEN)
        triangle = Triangle(color=RED).scale(1.5)
        
        shapes = VGroup(circle, square, triangle).arrange(RIGHT, buff=1)
        
        # Voiceover: Demonstration
        with self.voiceover(text="Watch as we bring concepts to life with dynamic visuals."):
            self.play(Create(shapes), run_time=3)
        
        # Voiceover: Closing
        with self.voiceover(text="Let's start learning together!"):
            self.play(
                Rotate(circle, angle=PI),
                square.animate.scale(0.5),
                triangle.animate.shift(UP),
                run_time=2
            )
        
        self.wait(2)
        self.play(FadeOut(title, shapes), run_time=1)
    
    def check_sox_installation(self):
        """
        Check if SoX is installed and available in the system PATH.
        
        Returns:
            bool: True if SoX is available, False otherwise
        """
        sox_path = shutil.which("sox")
        
        if sox_path:
            print(f"✓ SoX found at: {sox_path}")
            return True
        else:
            print("⚠ SoX not found in PATH")
            print("  Voice will be generated without audio post-processing.")
            print("  To enable SoX effects:")
            print("  1. Download SoX from: https://sourceforge.net/projects/sox/")
            print("  2. Install and add to system PATH")
            print("  3. Restart your terminal/IDE")
            return False
    
    def configure_voice_service_with_sox(self):
        """
        Configure GTTSService with SoX audio post-processing.
        
        SoX Effects Applied:
        - Pitch: Shift up by 100 cents (1 semitone) for lighter voice
        - Tempo: Speed up by 10% for more energetic delivery
        - Treble: Boost high frequencies for clarity
        """
        print("🎙 Configuring voice with SoX effects...")
        
        # SoX arguments for Teaching Assistant voice character
        # Format: ["effect1", "param1", "param2", "effect2", ...]
        sox_effects = [
            "pitch", "100",          # Pitch shift: +100 cents (lighter voice)
            "tempo", "1.1",          # Speed: 10% faster (more energetic)
            "treble", "3"            # Treble boost: +3dB (clearer)
        ]
        
        # Alternative SoX configurations you can try:
        # 
        # For a deeper, authoritative voice:
        # sox_effects = ["pitch", "-150", "tempo", "0.95", "bass", "2"]
        #
        # For a very cheerful, high-pitched voice:
        # sox_effects = ["pitch", "200", "tempo", "1.2", "treble", "5"]
        #
        # For a calm, soothing voice:
        # sox_effects = ["pitch", "50", "tempo", "0.9", "reverb", "20"]
        
        self.set_speech_service(
            GTTSService(
                lang="en",
                tld="com",
                sox_effects=sox_effects  # Apply SoX processing
            )
        )
        
        print("✓ Voice service configured with SoX effects")
    
    def configure_voice_service_basic(self):
        """
        Configure GTTSService without SoX processing (fallback).
        """
        print("🎙 Configuring basic voice service (no SoX)...")
        
        self.set_speech_service(
            GTTSService(
                lang="en",
                tld="com"
            )
        )
        
        print("✓ Basic voice service configured")


# ===== Alternative: Azure Service with SoX =====
# 
# For higher quality voice, you can use AzureService:
# (Requires Azure Speech Service API key)
#
# from manim_voiceover.services.azure import AzureService
#
# class AssistantIntroAzure(VoiceoverScene):
#     def construct(self):
#         # Configure Azure with SoX
#         self.set_speech_service(
#             AzureService(
#                 voice="en-US-JennyNeural",  # Friendly female voice
#                 style="cheerful",            # Speaking style
#                 subscription_key="YOUR_API_KEY",
#                 region="eastus",
#                 sox_effects=["pitch", "50", "tempo", "1.05"]
#             )
#         )
#         
#         with self.voiceover(text="Hello from Azure!"):
#             title = Text("Azure Voice Demo")
#             self.play(Write(title))


# ===== Advanced SoX Effects Reference =====
#
# Common SoX effects you can use:
#
# 1. Pitch shift: ["pitch", "cents"]
#    - Positive: higher pitch (100 = 1 semitone up)
#    - Negative: lower pitch (-100 = 1 semitone down)
#
# 2. Tempo: ["tempo", "factor"]
#    - >1.0: faster (1.2 = 20% faster)
#    - <1.0: slower (0.8 = 20% slower)
#
# 3. Speed: ["speed", "factor"]
#    - Changes both tempo AND pitch
#
# 4. Reverb: ["reverb", "reverberance"]
#    - 0-100: amount of room echo (50 = medium room)
#
# 5. Echo: ["echo", "gain-in", "gain-out", "delay", "decay"]
#    - Example: ["echo", "0.8", "0.7", "60", "0.3"]
#
# 6. Treble/Bass: ["treble", "dB"] or ["bass", "dB"]
#    - Positive: boost frequencies
#    - Negative: reduce frequencies
#
# 7. Equalizer: ["equalizer", "frequency", "width", "gain"]
#    - Target specific frequency ranges
#
# 8. Chorus: ["chorus", "gain-in", "gain-out", "delay", ...]
#    - Create layered vocal effect
#
# Combine multiple effects for custom voice characters!
