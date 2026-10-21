import streamlit as st
import os

from transcription import transcribe_audio
from emotion import detect_emotion
from explanation import explain_emotion


st.title("🎤 Emotion + LLM Explanation System")

st.write(
    "Select the language, speak using your microphone, "
    "and the system will generate the transcript, detect emotion, "
    "and provide an explanation."
)

# Language selection
language = st.selectbox(
    "Select speech language",
    ["English", "Hindi"]
)

# Microphone
audio = st.audio_input("🎤 Click here and speak")

if audio is not None:

    st.success("Speech recorded successfully!")

    st.audio(audio)

    os.makedirs("audio", exist_ok=True)

    audio_file = "audio/recorded_audio.wav"

    with open(audio_file, "wb") as f:
        f.write(audio.getbuffer())

    st.write("### Processing...")

    # -------------------------
    # STEP 1: TRANSCRIPTION
    # -------------------------

    st.write("📝 Converting speech to text...")

    text = transcribe_audio(
        audio_file,
        language
    )

    # -------------------------
    # STEP 2: EMOTION
    # -------------------------

    st.write("🎭 Detecting emotion...")

    emotion_result = detect_emotion(audio_file)

    highest_emotion = emotion_result[0]

    emotion = highest_emotion["label"]
    confidence = highest_emotion["score"]

    # -------------------------
    # STEP 3: EXPLANATION
    # -------------------------

    st.write("💡 Generating explanation...")

    explanation = explain_emotion(
        text,
        emotion
    )

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------

    st.write("## 📄 Transcript")

    if text:
        st.write(text)
    else:
        st.warning("Speech could not be transcribed.")

    st.write("## 😊 Detected Emotion")
    st.write(emotion)

    st.write("## 📊 Confidence")
    st.write(round(confidence, 3))

    st.write("## 💡 Explanation")
    st.write(explanation)