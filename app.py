import streamlit as st
import requests

st.set_page_config(page_title="MetaAI Video Prompt Builder", layout="centered")

st.title("🎬 MetaAI Video Prompt Builder + Gimni Enhancer")
st.write("Create professional video prompts for MetaAI. Fill in details or use presets, then enhance with Gimni AI.")

# --- Preset Prompts ---
presets = {
    "Cinematic Action": {
        "subject": "a spy in a black suit",
        "action": "running across rooftops",
        "environment": "a neon-lit futuristic city at night",
        "camera": "a fast tracking shot, then a close-up",
        "style": "Cinematic",
        "mood": "intense and thrilling",
        "duration": "12 seconds",
        "resolution": "4K",
        "constraints": "blurry visuals, text artifacts"
    },
    "Anime Fantasy": {
        "subject": "a magical girl with glowing wings",
        "action": "flying above the city skyline",
        "environment": "a sparkling night sky with stars",
        "camera": "a wide-angle upward pan",
        "style": "Anime",
        "mood": "dreamy and magical",
        "duration": "10 seconds",
        "resolution": "1080p",
        "constraints": "text artifacts, glitches"
    },
    "Nature Documentary": {
        "subject": "a majestic tiger",
        "action": "walking slowly",
        "environment": "a dense jungle with sunlight breaking through the trees",
        "camera": "a low tracking shot",
        "style": "Documentary",
        "mood": "powerful and mysterious",
        "duration": "12 seconds",
        "resolution": "4K",
        "constraints": "blurry textures, distortions"
    }
}

preset_choice = st.selectbox("🎭 Choose a Preset (optional)", ["Custom"] + list(presets.keys()))

# --- Fill fields with preset if chosen ---
if preset_choice != "Custom":
    preset = presets[preset_choice]
    subject = st.text_input("Main Subject/Character", preset["subject"])
    action = st.text_input("Action", preset["action"])
    environment = st.text_input("Environment/Setting", preset["environment"])
    camera = st.text_input("Camera angle & movement", preset["camera"])
    style = st.selectbox("Visual Style", ["Cinematic", "Ultra Realistic", "Anime", "Cartoon", "Fantasy", "Documentary"], index=["Cinematic","Ultra Realistic","Anime","Cartoon","Fantasy","Documentary"].index(preset["style"]))
    mood = st.text_input("Mood/Atmosphere", preset["mood"])
    duration = st.text_input("Duration", preset["duration"])
    resolution = st.selectbox("Resolution", ["1080p", "4K"], index=["1080p", "4K"].index(preset["resolution"]))
    constraints = st.text_area("Things to Avoid", preset["constraints"])
else:
    subject = st.text_input("Main Subject/Character", "a young woman in a red dress")
    action = st.text_input("Action (what is happening)", "walking through the city")
    environment = st.text_input("Environment/Setting", "a neon-lit futuristic street at night")
    camera = st.text_input("Camera angle & movement", "cinematic tracking shot from behind, then close-up")
    style = st.selectbox("Visual Style", ["Cinematic", "Ultra Realistic", "Anime", "Cartoon", "Fantasy", "Documentary"])
    mood = st.text_input("Mood/Atmosphere", "mysterious and dramatic")
    duration = st.text_input("Duration", "10 seconds")
    resolution = st.selectbox("Resolution", ["1080p", "4K"])
    constraints = st.text_area("Things to Avoid", "blurry visuals, text artifacts, distortions")

# --- Generate Raw Prompt ---
if st.button("✨ Generate Prompt"):
    raw_prompt = (
        f"A {subject} {action} in {environment}. "
        f"The camera shows {camera}. "
        f"The style is {style.lower()}. "
        f"The atmosphere feels {mood}. "
        f"Video should be {duration}, {resolution}, smooth motion. "
        f"Avoid {constraints}."
    )

    st.subheader("✅ Draft Prompt:")
    st.write(raw_prompt)

    # --- Gimni API Integration ---
    gimni_api_key = st.text_input("🔑 Enter your Gimni API Key", type="password")

    if gimni_api_key and st.button("🤖 Enhance with Gimni AI"):
        try:
            url = "https://api.gimni.ai/v1/chat/completions"  # Update if Gimni docs give another endpoint
            headers = {
                "Authorization": f"Bearer {gimni_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gimni-1.5-pro",  # Replace with your available Gimni model
                "messages": [
                    {"role": "system", "content": "You are an expert in prompt engineering for AI video generation."},
                    {"role": "user", "content": f"Refine this into the best MetaAI video prompt: {raw_prompt}"}
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            enhanced_prompt = result["choices"][0]["message"]["content"]

            st.subheader("🚀 Enhanced Prompt (by Gimni):")
            st.write(enhanced_prompt)

            st.download_button("📥 Download Enhanced Prompt", enhanced_prompt, file_name="metaai_best_prompt.txt")

        except Exception as e:
            st.error(f"Error with Gimni API: {e}")
