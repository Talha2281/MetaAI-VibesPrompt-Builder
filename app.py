import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(page_title="MetaAI Video Prompt Builder", layout="centered")

st.title("🎬 MetaAI Video Prompt Builder")
st.write("Write your idea below and let Gimni structure it into a professional MetaAI video prompt.")

# Prompt Structure Guide
with st.expander("📌 Prompt Structure Guide (Click to View)"):
    st.markdown("""
    **Best Practice Structure for MetaAI Video Prompts**  
    1. **Subject** → Who/What is the video about (e.g., "a young woman in a red dress")  
    2. **Action** → What are they doing (e.g., "walking through the city")  
    3. **Environment** → Where it happens (e.g., "a neon-lit futuristic street at night")  
    4. **Camera** → Angle & movement (e.g., "cinematic tracking shot, then close-up")  
    5. **Style** → Cinematic, Anime, Fantasy, Realistic, etc.  
    6. **Mood/Atmosphere** → Emotional tone (e.g., "mysterious and dramatic")  
    7. **Duration & Resolution** → Example: "10 seconds, 4K"  
    8. **Constraints** → What to avoid (e.g., "no blurry visuals, no distortions")  
    """)

# User Input
user_idea = st.text_area(
    "📝 Describe your video idea in your own words:",
    height=50,
    placeholder="Example: A knight riding a horse across a battlefield at sunrise, epic cinematic style..."
)

# Load API key from Streamlit secrets
api_key = st.secrets["GIMNI_API_KEY"]
genai.configure(api_key=api_key)

# Fixed model
MODEL_NAME = "gemini-2.5-flash"

# Generate structured prompt
if st.button("✨ Generate Professional Prompt"):
    if user_idea.strip():
        try:
            st.sidebar.write(f"✅ Using model: {MODEL_NAME}")
            model = genai.GenerativeModel(MODEL_NAME)

            system_instruction = (
                "You are an expert video prompt engineer for MetaAI. "
                "Take the user’s raw idea and rewrite it into a highly detailed, professional MetaAI video prompt. "
                "Follow this structure: Subject, Action, Environment, Camera, Style, Mood, Duration/Resolution, Constraints. "
                "Ensure clarity, cinematic quality, and remove vagueness."
            )
            response = model.generate_content([system_instruction, user_idea])
            final_prompt = response.text.strip()

            st.subheader("✅ Your Generated Prompt:")
            st.write(final_prompt)

            st.download_button("📥 Download Prompt", final_prompt, file_name="metaai_video_prompt.txt")
        except Exception as e:
            st.error(f"⚠️ Failed to generate prompt. Error: {e}")
    else:
        st.warning("⚠️ Please enter your video idea first.")
