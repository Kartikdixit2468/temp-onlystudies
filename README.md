# README.md 🎓

This file provides an introduction, key features, tech stack, and setup steps for OnlyStudies, guiding you through project usage and configuration.

## Project Overview

OnlyStudies transforms simple text into three-minute educational animations. It leverages AI to automate scriptwriting, scene generation, and rendering. Users can illustrate complex concepts through visual storytelling with minimal effort.

## Key Features 🚀

- **Automated Video Pipeline**: Generates a full 3-minute lesson without manual steps.  
- **Intelligent Structuring**: Enforces a **Theory → Analogy → Example** pedagogical format.  
- **Smart Stitching**: Generates separate scenes to bypass AI context limits and stitches them into a seamless MP4.  
- **Sleek UX**: Offers a dark-mode Streamlit interface with live terminal logs and Lottie loading animations.

## Tech Stack 🛠️

- **Frontend**: Streamlit (Python)  
- **AI Logic**: Google Gemini 1.5 Pro via the `google-generativeai` package  
- **Animation Engine**: Manim Community Edition  
- **Video Processing**: FFmpeg & MoviePy  

## Installation & Setup ⚙️

Follow these steps to install dependencies and run the application locally.

**Prerequisites**  
- Python 3.10 or higher  
- FFmpeg installed and added to your system `PATH`  
- LaTeX (optional, for math formulas)  

**Steps**  
1. Clone the repository.  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Configure environment variables:  
   - Copy `.env.example` to `.env`.  
   - Add your `GOOGLE_API_KEY`.  
4. Run the app:  
   ```bash
   streamlit run app.py
   ```  

## File Relationships 🔗

This table maps **README.md** sections to key repository files, showing how each component supports the project.

| File                              | Role                                            | Related Section         |
|-----------------------------------|-------------------------------------------------|-------------------------|
| `requirements.txt`                | Defines Python dependencies                     | Installation & Setup    |
| `.env.example`                    | Sample environment variable template            | Installation & Setup    |
| `app.py`                          | Main Streamlit application entry point          | Installation & Setup    |
| `Dockerfile`                      | Container deployment configuration              | Alternative Deployment  |
| `backend.py`, `voiceover_backend.py` | Core AI and video generation logic          | Tech Stack              |
| `list_models.py`                  | Lists available Gemini AI models                | Tech Stack              |
| `VOICEOVER_QUICKREF.md`           | Quick reference for Manim Voiceover usage       | Auxiliary Documentation |
| `render.yaml`                     | Render service configuration (e.g., Fly.io)     | Deployment              |
| `test_complex_topic.py`           | Automated tests for topic code generation       | Testing                 |
| `assistant_intro.py`, `temp_topic.py` | Example Manim scenes showcasing voice integration | Examples                |

This documentation highlights how **README.md** guides users through setup, illustrates project capabilities, and ties into the core codebase.
