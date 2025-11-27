import os
from voiceover_backend import VoiceoverArtist

def test_complex_topic():
    print("Testing Complex Topic Generation...")
    
    # Test 1: Bubble Sort (Algorithm)
    print("\n1. Generating code for 'Bubble Sort'...")
    code_sort = VoiceoverArtist.generate_voiceover_scene("Bubble Sort", "Computer Science", quality="Low")
    
    if code_sort.startswith("# Error"):
        print(f"Generation failed: {code_sort}")
    else:
        print("Analyzing Bubble Sort code...")
        has_vgroup = "VGroup" in code_sort
        has_move_to = ".move_to" in code_sort
        # Check for list update pattern (heuristic)
        has_list_update = "submobjects" in code_sort or "squares[" in code_sort
        
        print(f"Has VGroup: {'YES' if has_vgroup else 'NO'}")
        print(f"Has .move_to (Swap Logic): {'YES' if has_move_to else 'NO'}")
        print(f"Has List Update Logic: {'YES' if has_list_update else 'NO'}")
        
        if has_vgroup and has_move_to:
            print("PASS: Bubble Sort follows algorithm pattern.")
        else:
            print("WARNING: Bubble Sort might be missing key patterns.")

    # Test 2: Pythagoras (Geometry)
    print("\n2. Generating code for 'Pythagorean Theorem'...")
    code_geo = VoiceoverArtist.generate_voiceover_scene("Pythagorean Theorem", "Mathematics", quality="Low")
    
    if code_geo.startswith("# Error"):
        print(f"Generation failed: {code_geo}")
    else:
        print("Analyzing Pythagoras code...")
        has_polygon = "Polygon" in code_geo or "Triangle" in code_geo
        has_next_to = ".next_to" in code_geo
        
        print(f"Has Polygon/Triangle: {'YES' if has_polygon else 'NO'}")
        print(f"Has .next_to (Label Safety): {'YES' if has_next_to else 'NO'}")
        
        if has_polygon and has_next_to:
            print("PASS: Pythagoras follows geometry pattern.")
        else:
            print("WARNING: Pythagoras might be missing key patterns.")

if __name__ == "__main__":
    test_complex_topic()
