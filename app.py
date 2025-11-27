import streamlit as st
import os
from backend import Studio, Editor
from voiceover_backend import VoiceoverArtist

st.set_page_config(page_title="OnlyStudies", page_icon="🎓", layout="wide")

st.title("OnlyStudies 🎓✨")
st.subheader("Turn Text into Educational Animations in Minutes.")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    
    # Subject Selection
    subject = st.selectbox(
        "Subject",
        ["General", "Mathematics", "Computer Science", "Physics", "Chemistry", "Biology", "Economics", "History"],
        index=0,
        help="Helps the AI tailor the explanation and examples."
    )
    
    # Quality Selection
    quality = st.selectbox(
        "Video Quality", 
        ["Low", "Medium", "High"], 
        index=1, 
        help="Low/Medium use faster models. High uses the most advanced model."
    )
    
    # Voice Preset Selection
    voice_preset = st.selectbox(
        "Voice Style",
        ["teaching_assistant", "professor", "enthusiastic", "calm", "neutral"],
        index=0,
        help="Choose the voice character for narration."
    )

topic = st.text_input("Enter a topic to explain:", placeholder="e.g., Newton's Third Law, Bubble Sort, Photosynthesis")

if st.button("Generate Lesson"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        status_container = st.container()
        
        with status_container:
            st.info(f"🎬 Planning and animating '{topic}' ({subject})...")
            
            # Generate Code with Voiceover
            code = VoiceoverArtist.generate_voiceover_scene(
                topic=topic,
                subject=subject,
                quality=quality,
                voice_preset=voice_preset,
                use_sox=True
            )
            
            if code.startswith("# Error"):
                st.error(f"Failed to generate animation code: {code}")
            else:
                st.write(f"🎥 Rendering video (this may take a minute)...")
                output_filename = "lesson.mp4"
                
                success, error_msg, video_path = Studio.render_video(code, output_filename, quality=quality)
                
                if success and video_path:
                    st.success("🎉 Video Ready!")
                    st.video(video_path)
                    
                    with open(video_path, "rb") as file:
                        st.download_button(
                            label="Download MP4",
                            data=file,
                            file_name=f"{topic.replace(' ', '_')}_lesson.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error(f"Failed to render video.")
                    st.error(error_msg) # Hidden as requested

if st.button("Clear Workspace"):
    Editor.cleanup()
    st.success("Workspace cleared.")
