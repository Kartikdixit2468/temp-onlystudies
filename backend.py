import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import time
from google.api_core import exceptions
import requests
import base64
import uuid
from datetime import datetime

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_model(quality):
    if quality == "High":
        return genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    elif quality == "Medium":
        return genai.GenerativeModel('gemini-2.0-flash')
    else:
        # Low
        return genai.GenerativeModel('gemini-2.0-flash-lite')

def get_fallback_model():
    return genai.GenerativeModel('gemini-2.0-flash-lite')

def upload_to_github(file_path, repo_name, token, commit_message="Upload generated video"):
    """
    Uploads a file to a GitHub repository.
    Returns the download URL of the uploaded file.
    """
    if not os.path.exists(file_path):
        return None, "File not found"

    with open(file_path, "rb") as f:
        content = f.read()
    
    encoded_content = base64.b64encode(content).decode("utf-8")
    
    # Generate a unique path in the repo to avoid conflicts and keep history
    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{os.path.splitext(filename)[0]}_{timestamp}_{uuid.uuid4().hex[:6]}{os.path.splitext(filename)[1]}"
    path_in_repo = f"generated_videos/{unique_filename}"
    
    url = f"https://api.github.com/repos/{repo_name}/contents/{path_in_repo}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": commit_message,
        "content": encoded_content
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        # Return the download URL. For public repos, raw_url is good.
        # For private, we might need the 'download_url' from response which might be a tokenized link or raw link.
        # The 'download_url' in the response is usually the raw.githubusercontent.com link.
        return response.json().get("content", {}).get("download_url") or response.json().get("download_url"), None
    else:
        return None, f"GitHub upload failed: {response.status_code} - {response.text}"

class Artist:
    @staticmethod
    def generate_video_code(topic, subject, quality="Medium"):
        # Clear any previous temp files to ensure fresh context
        if os.path.exists("temp_topic.py"):
            try:
                os.remove("temp_topic.py")
            except Exception:
                pass  # Ignore if file is locked
        
        model = get_model(quality)
        prompt = f"""
        CONTEXT: This is a FRESH REQUEST. Ignore any previous topics or examples.
        
        TOPIC TO EXPLAIN: "{topic}"
        SUBJECT AREA: {subject}
        
        Type: High-quality 2D Motion Graphics for Education.

        CRITICAL INSTRUCTION: ALL THREE SECTIONS (Definition, Analogy, AND Concrete Example) MUST be about "{topic}" ONLY. 
        Do NOT mix with other topics, algorithms, or examples. Stay 100% focused on "{topic}".

        Visual Style:
        - Aesthetic: "Kurzgesagt" or "Vox" style. Flat vector art. Minimalist design. High contrast.
        - Background: Solid, clean, dark background (e.g., charcoal or deep blue) to make foreground elements pop.
        - Text: Large, bold Sans-Serif font. White text. Text must appear sequentially: erase old text before writing new text to avoid pile-up.

        Motion & Physics Rules (STRICT):
        - No Morphing: Objects must remain solid and rigid. They slide or fade in/out; they do not melt or change shape.
        - No Overlapping: Distinct elements must maintain separation. Do not stack objects on top of each other.
        - Stable Camera: Fixed, locked-off camera angle. No zooming or shaky cam.

        Geometry Rules (STRICT):
        - Anchor Object: Draw the main shape first (e.g., Triangle) and fix it in the center.
        - Geometric Snapping: Objects must touch edges precisely. No floating shapes.
        - Rotation: Shapes attached to diagonal lines must be rotated to match the angle.
        - Text Safety: Text must appear *outside* the shapes, never overlapping lines.

        Scene Description (All sections MUST relate to "{topic}" ONLY):
        1. Definition/Theory: Clear text explanation of "{topic}". Clear the screen afterwards.
        
        2. Real-world Analogy: Use simple shapes to demonstrate "{topic}" specifically. Clear the screen afterwards.
        
        3. Concrete Example: A visual demonstration or implementation of "{topic}" specifically.
           - If "{topic}" is a mathematical concept (theorem, formula, equation):
             * Show a worked numerical example with step-by-step calculations
             * Use geometric shapes, diagrams, or visual proofs if applicable
             * Animate the solution process clearly
           
           - If "{topic}" is an algorithm or computational process:
             * Write the actual Python loop (e.g., for i in range...) to generate the animation commands
             * Do NOT hardcode steps. Let the loop drive the animation
             * Use `VGroup` of `Square` objects with `Text` inside for arrays/lists
             * Use `animate.move_to` to swap/move positions visually based on current state
             * Color Code: Yellow for comparison/active, Red for changes/swaps, Green for completed/sorted
             * Pacing: Use `run_time=1.0` for moves/swaps. Do not make it instant
           
           - If "{topic}" is a scientific concept:
             * Create a step-by-step visual demonstration
             * Use labeled shapes and clear text annotations
             * Show the process or phenomenon in action
           
           - **CRITICAL**: Clear the screen of previous text/shapes before starting the example
           - **CRITICAL**: The example MUST demonstrate "{topic}" specifically, NOT any other topic

        Negative Prompt: 3D rendering, realistic photography, cinematic depth of field, motion blur, morphing, melting, liquid simulation, chaotic motion, overlapping text, double exposure, illegible text, ghosting, vibrating objects, stacking objects, cluttered, busy, messy, mixing different topics, unrelated examples, external assets, SVGs, images.

        Requirements:
        - The class name must be 'SceneTopic'.
        - Inherit from `Scene`.
        - Create a continuous animation that lasts at least 60 seconds.
        - **IMPORTANT**: Do NOT use `MathTex` or LaTeX. Use `Text` for ALL text and formulas.
        - Output ONLY the Python code. No markdown, no explanations.
        - Do NOT include `config.media_width` or similar config settings in the code.
        - Import manim: `from manim import *`
        - VERIFY: All three sections explain/demonstrate "{topic}" ONLY
        - **CRITICAL**: Do NOT use `SVGMobject`, `ImageMobject`, or any external assets. Use ONLY built-in Manim shapes (Circle, Square, Line, Polygon, etc.).
        """
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                code = response.text.replace("```python", "").replace("```", "").strip()
                # Ensure essential imports are present
                if "import math" not in code:
                    code = "import math\n" + code
                if "import random" not in code:
                    code = "import random\n" + code
                return code
            except exceptions.ResourceExhausted:
                print(f"Quota exceeded on attempt {attempt + 1}. Switching to fallback model...")
                model = get_fallback_model()
                time.sleep(2)
            except Exception as e:
                return f"# Error: {e}"
        return "# Error: Failed to generate code after retries"

class Studio:
    @staticmethod
    def render_video(code, output_filename, quality="Medium"):
        # Save code to file with UTF-8 encoding
        script_path = f"temp_topic.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # Determine Manim quality flag
        quality_flag = "-ql" # Default Low
        if quality == "Medium":
            quality_flag = "-qm"
        elif quality == "High":
            quality_flag = "-qh"

        # Ensure LaTeX is in the PATH (Windows MiKTeX)
        tex_path = r"C:\Users\Siddhant\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
        env = os.environ.copy()
        if tex_path not in env["PATH"]:
            env["PATH"] += f";{tex_path}"

        # Run Manim
        # We use a fixed scene name 'SceneTopic' as requested in the prompt
        command = f"manim {quality_flag} -o {output_filename} {script_path} SceneTopic"
        
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            return False, stderr, None
            
        # Robustly find the output file
        # Manim output structure can vary, so we search for the file
        expected_name = output_filename
        if not expected_name.endswith(".mp4"):
            expected_name += ".mp4"
            
        search_dir = "media"
        found_path = None
        
        for root, dirs, files in os.walk(search_dir):
            if expected_name in files:
                found_path = os.path.join(root, expected_name)
                # Prefer the one in the quality folder if multiple exist (heuristic)
                if quality == "Low" and "480p15" in root:
                    break
                if quality == "Medium" and "720p30" in root:
                    break
                if quality == "High" and "1080p60" in root:
                    break
        
        if found_path:
            # Upload to GitHub
            github_token = os.getenv("GITHUB_TOKEN")
            github_repo = os.getenv("GITHUB_REPO")
            
            if not github_token or not github_repo:
                 # Fallback to local if no credentials (though user asked for GitHub storage)
                 # But we should probably warn or error. For now, let's assume they exist as per plan.
                 return False, "GITHUB_TOKEN or GITHUB_REPO not set in environment variables.", None

            url, upload_error = upload_to_github(found_path, github_repo, github_token)
            
            if url:
                # Cleanup local file
                try:
                    os.remove(found_path)
                except Exception as e:
                    print(f"Error removing local file: {e}")
                
                Editor.remove_partial_files()
                return True, "", url
            else:
                Editor.remove_partial_files()
                return False, f"Rendered but upload failed: {upload_error}", None
        else:
            Editor.remove_partial_files()
            return False, "Rendered successfully but could not locate output file.", None

class Editor:
    @staticmethod
    def cleanup():
        """Clean up temporary files and clear context"""
        # Remove temp Python script
        if os.path.exists("temp_topic.py"):
            try:
                os.remove("temp_topic.py")
            except Exception as e:
                print(f"Could not remove temp_topic.py: {e}")
        
        # Remove any .pyc cache files
        if os.path.exists("__pycache__"):
            import shutil
            try:
                shutil.rmtree("__pycache__")
            except Exception as e:
                print(f"Could not remove __pycache__: {e}")

    @staticmethod
    def remove_partial_files():
        """Recursively finds and deletes 'partial_movie_files' directories within 'media'."""
        search_dir = "media"
        if not os.path.exists(search_dir):
            return

        import shutil
        import stat
        import time

        def remove_readonly(func, path, _):
            "Clear the readonly bit and reattempt the removal"
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass

        for root, dirs, files in os.walk(search_dir, topdown=False):
            for name in dirs:
                if name == "partial_movie_files":
                    dir_path = os.path.join(root, name)
                    # Retry logic
                    for attempt in range(3):
                        try:
                            shutil.rmtree(dir_path, onerror=remove_readonly)
                            break # Success
                        except Exception as e:
                            if attempt < 2:
                                time.sleep(0.5) # Wait a bit before retrying
                            else:
                                print(f"Error deleting {dir_path} after retries: {e}")
