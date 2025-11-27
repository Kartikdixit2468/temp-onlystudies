import os
from voiceover_backend import VoiceoverArtist
from backend import Studio

def test_retry_logic():
    print("Testing Retry Logic & Self-Correction...")
    
    topic = "The Square"
    subject = "Geometry"
    quality = "Low" # Faster for testing
    
    # 1. Generate initial code
    print(f"\n1. Generating code for '{topic}'...")
    code = VoiceoverArtist.generate_voiceover_scene(topic, subject, quality=quality)
    
    if code.startswith("# Error"):
        print(f"Generation failed: {code}")
        return

    print("Code generated.")
    
    # 2. Inject a Syntax Error
    print("\n2. Injecting a syntax error...")
    broken_code = code.replace("def construct(self):", "def construct(self)  # Missing colon")
    
    # 3. Simulate the Retry Loop
    max_retries = 3
    current_code = broken_code
    success = False
    
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries}")
        
        output_filename = "test_retry.mp4"
        
        # Try to render
        render_success, render_error, rendered_path = Studio.render_video(current_code, output_filename, quality=quality)
        
        if render_success:
            print("Render SUCCESS!")
            success = True
            break
        else:
            print(f"Render FAILED. Error snippet: {render_error[:100]}...")
            
            if attempt < max_retries - 1:
                print("Attempting self-correction...")
                current_code = VoiceoverArtist.fix_code(current_code, render_error, topic, quality)
                print("Code patched.")
    
    if success:
        print("\nTest PASSED: System successfully recovered from error.")
    else:
        print("\nTest FAILED: System could not recover.")

if __name__ == "__main__":
    test_retry_logic()
