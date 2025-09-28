import streamlit as st
from google import genai

# ✅ Load Gemini API key from Streamlit Secrets safely
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 GEMINI_API_KEY is missing in Streamlit Secrets. Please add it in the Secrets manager.")
    st.stop()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# ✅ Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="MetaAI Vibes Prompt Builder", page_icon="🎬", layout="centered")

st.title("🎬 MetaAI Vibes Prompt Builder")
st.markdown("Create short, optimized prompts for **Meta AI video generation**.")

# --- Prompt Guide (just a reference, not forced) ---
with st.expander("📖 Prompt Guide (Optional)", expanded=False):
    st.markdown("""
    A good video prompt often includes:
    - **Subject** → Who/what is in the video (person, animal, object, scene).  
    - **Action** → What’s happening (running, dancing, flying, etc.).  
    - **Environment** → Where it happens (city, forest, space, underwater).  
    - **Style/Mood** → Cinematic, realistic, anime, cartoon, dreamy, etc.  
    - **Camera/Lighting (Optional)** → Close-up, aerial view, soft lighting, neon glow.  

    Example:  
    *"A cinematic close-up of a young woman running through a neon-lit cyberpunk street, dramatic lighting, futuristic atmosphere."*
    """)

# --- User Input ---
user_idea = st.text_area("💡 Describe your video idea:", placeholder="Example: A panda surfing on ocean waves at sunset...")

if st.button("✨ Generate Optimized Prompt"):
    if not user_idea.strip():
        st.warning("⚠️ Please enter your video idea first.")
    else:
        try:
            with st.spinner("Generating optimized prompt with Gemini..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",  # ✅ correct model
                    contents=f"Make this idea into a concise, professional prompt for video generation (no headings, just the final prompt): {user_idea}"
                )

            optimized_prompt = response.text.strip()
            st.success("✅ Prompt generated successfully!")
            st.text_area("🎯 Optimized Prompt:", optimized_prompt, height=120)

        except Exception as e:
            st.error(f"⚠️ Failed to generate prompt. Error: {str(e)}")
