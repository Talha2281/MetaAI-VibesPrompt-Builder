import streamlit as st
from google import genai

# Load API key from Streamlit Secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="MetaAI Video Prompt Generator", page_icon="🎬", layout="wide")

st.title("🎬 MetaAI Video Prompt Generator")
st.write("Create **powerful prompts** for video generation with MetaAI. ✨")

# Show structure as guidance only (not for output)
with st.expander("📖 Prompt Structure Guide"):
    st.markdown("""
    **A good video prompt usually includes:**
    - **Subject** → Who/what is in the video (e.g., astronaut, cat, car, dancer).  
    - **Action / Scene** → What is happening (e.g., walking on Mars, jumping in slow motion).  
    - **Environment / Background** → Where it takes place (e.g., futuristic city, beach at sunset).  
    - **Style / Mood** → Realistic, cinematic, anime, cartoon, documentary.  
    - **Camera / Quality** → 4K, cinematic lighting, wide-angle, close-up, drone shot.  
    - **Extra details** → Colors, atmosphere, time of day, weather, etc.  
    """)

# User free text
user_input = st.text_area("📝 Describe your idea for the video:", placeholder="Example: A futuristic city at night with flying cars...")

if st.button("✨ Generate Prompt"):
    if not user_input.strip():
        st.warning("Please enter your idea first!")
    else:
        with st.spinner("Generating best prompt..."):
            try:
                # Ask Gemini to generate a short natural prompt
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
                    You are an expert prompt engineer for video generation.
                    The user gave this idea: {user_input}

                    Use the best structure (subject, action, environment, style, camera, details) as a **hidden guide**.
                    But return only a **single final clean prompt** without headings, labels, or bullet points.
                    Keep it natural, creative, and under 2–3 sentences.
                    """
                )

                final_prompt = response.output_text.strip()
                st.success("✅ Best Prompt Generated!")
                st.text_area("🎬 Final Prompt:", value=final_prompt, height=150)

            except Exception as e:
                st.error(f"⚠️ Failed to generate prompt. Error: {str(e)}")
