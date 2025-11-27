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

# Initialize Session State
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = ""
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "feedback_mode" not in st.session_state:
    st.session_state.feedback_mode = False

topic = st.text_input("Enter a topic to explain:", placeholder="e.g., Newton's Third Law, Bubble Sort, Photosynthesis")

def generate_video(topic_text, subject_text, quality_setting, voice_preset_setting, existing_code=None, feedback=None):
    status_container = st.container()
    
    with status_container:
        if existing_code and feedback:
            st.info(f"🔄 Regenerating '{topic_text}' with feedback: {feedback}...")
            current_code = VoiceoverArtist.regenerate_video_code(
                original_code=existing_code,
                feedback=feedback,
                topic=topic_text,
                subject=subject_text,
                quality=quality_setting
            )
        else:
            st.info(f"🎬 Planning and animating '{topic_text}' ({subject_text})...")
            current_code = VoiceoverArtist.generate_voiceover_scene(
                topic=topic_text,
                subject=subject_text,
                quality=quality_setting,
                voice_preset=voice_preset_setting,
                use_sox=True
            )
        
        max_retries = 3
        success = False
        new_video_path = None
        error_msg = ""

        for attempt in range(max_retries):
            if current_code.startswith("# Error"):
                st.error(f"Failed to generate animation code: {current_code}")
                break
            
            st.write(f"🎥 Rendering video (Attempt {attempt + 1}/{max_retries})...")
            output_filename = "lesson.mp4"
            
            # Try to render
            render_success, render_error, rendered_path = Studio.render_video(current_code, output_filename, quality=quality_setting)
            
            if render_success and rendered_path:
                success = True
                new_video_path = rendered_path
                break
            else:
                if attempt < max_retries - 1:
                    st.warning(f"Render failed on attempt {attempt + 1}. Retrying with self-correction...")
                    error_msg = render_error
                    # Self-correct
                    current_code = VoiceoverArtist.fix_code(current_code, error_msg, topic_text, quality_setting)
                else:
                    error_msg = render_error
        
        if success and new_video_path:
            st.session_state.generated_code = current_code
            st.session_state.current_topic = topic_text
            st.session_state.current_subject = subject_text
            st.session_state.video_path = new_video_path
            st.session_state.feedback_mode = False # Reset feedback mode on new success
            return True
        else:
            st.error(f"Failed to render video after {max_retries} attempts.")
            with st.expander("Show Error Details"):
                st.code(error_msg)
            return False

if st.button("Generate Lesson"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        generate_video(topic, subject, quality, voice_preset)

# Display Video and Feedback if available
if st.session_state.video_path:
    # Check if it's a URL or local path
    is_url = st.session_state.video_path.startswith("http")
    
    if is_url or os.path.exists(st.session_state.video_path):
        st.success("🎉 Video Ready!")
        st.video(st.session_state.video_path)
        
        # Download button logic
        if is_url:
            import requests
            try:
                response = requests.get(st.session_state.video_path)
                if response.status_code == 200:
                    st.download_button(
                        label="Download MP4",
                        data=response.content,
                        file_name=f"{st.session_state.current_topic.replace(' ', '_')}_lesson.mp4",
                        mime="video/mp4"
                    )
                else:
                    st.error("Could not fetch video for download.")
            except Exception as e:
                st.error(f"Error fetching video: {e}")
        else:
            with open(st.session_state.video_path, "rb") as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=f"{st.session_state.current_topic.replace(' ', '_')}_lesson.mp4",
                    mime="video/mp4"
                )
    
    st.divider()
    st.write("### Feedback")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 Good"):
            st.balloons()
            st.success("Thanks for your feedback!")
            st.session_state.feedback_mode = False
            
    with col2:
        if st.button("👎 Bad"):
            st.session_state.feedback_mode = True
            
    if st.session_state.feedback_mode:
        with st.form("feedback_form"):
            feedback_text = st.text_area("What was wrong with the video?", placeholder="e.g., The text was overlapping, the explanation was wrong...")
            submit_feedback = st.form_submit_button("Regenerate with Feedback")
            
            if submit_feedback and feedback_text:
                success = generate_video(
                    st.session_state.current_topic,
                    st.session_state.current_subject,
                    quality,
                    voice_preset,
                    existing_code=st.session_state.generated_code,
                    feedback=feedback_text
                )
                if success:
                    st.rerun()

if st.button("Clear Workspace"):
    Editor.cleanup()
    st.success("Workspace cleared.")
