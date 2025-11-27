"""
Quick test to verify voiceover setup with SoX
"""
from voiceover_backend import VoiceoverArtist, check_sox_available

print("=" * 60)
print("Audio Setup Verification")
print("=" * 60)

# Check SoX
print("\n1. Checking SoX installation...")
if check_sox_available():
    print("   ✓ SoX is available")
else:
    print("   ✗ SoX not found")

# List voice presets
print("\n2. Available voice presets:")
VoiceoverArtist.list_voice_presets()

# Generate a simple test scene
print("\n3. Generating test voiceover scene...")
code = VoiceoverArtist.generate_voiceover_scene(
    topic="Pythagorean Theorem",
    subject="Mathematics",
    quality="Low",  # Use Low for faster testing
    voice_preset="teaching_assistant",
    use_sox=True
)

if code.startswith("# Error"):
    print(f"   ✗ Error generating code: {code}")
else:
    print("   ✓ Code generated successfully")
    print(f"\n   Preview (first 500 chars):")
    print("   " + "-" * 56)
    print("   " + code[:500].replace("\n", "\n   "))
    print("   ...")
    
    # Save the test code
    with open("test_voiceover_scene.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("\n   ✓ Saved to test_voiceover_scene.py")
    print("\n   To render: manim -pql test_voiceover_scene.py SceneTopic")

print("\n" + "=" * 60)
