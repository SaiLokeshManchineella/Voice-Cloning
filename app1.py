import streamlit as st
import pyttsx3
from gtts import gTTS
import speech_recognition as sr
import base64
from deep_translator import GoogleTranslator  # For multi-language support

# Function to convert binary file to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set the background image in Streamlit
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-position: center;
    background-size: cover;
    }}
    </style>
    '''
    st.markdown('<style>h1 { color: Black; }</style>', unsafe_allow_html=True)
    st.markdown('<style>p { color: Black; font-weight: bold; }</style>', unsafe_allow_html=True)
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background (ensure the image file exists in the directory)
set_background('2.jpg')

# Function to generate speech from text using pyttsx3 (this can be replaced by a voice cloning model)
def generate_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

# Function to recognize speech using SpeechRecognition
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        st.write("Sorry, there was an issue with the speech service.")
        return ""

# Multi-language conversion using Google Translator (deep-translator)
def translate_text(text, target_language):
    translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated

# Streamlit app interface
st.title("Voice Cloning and Mimicking System with Multi-Language Support")

# Option to choose language for cloning (For multi-language support)
lang_choice = st.selectbox("Select Language for Cloning:", ['en', 'es', 'fr', 'de', 'it', 'pt', 'hi'])

# User input text
user_text = st.text_area("Enter Text to Clone:", "Hello, how are you today?")

# Button to generate speech from text
if st.button("Generate Speech from Text"):
    st.write("Generating cloned speech...")
    # Here, the generated speech is in the selected language
    translated_text = translate_text(user_text, target_language=lang_choice)
    generate_speech(translated_text)  # Using pyttsx3 for speech generation (can be replaced with voice cloning)
    st.audio("output.mp3", format='audio/mp3')

# Button to practice speech and compare (uses voice input to generate cloned voice)
if st.button("Start Speech Practice"):
    st.write("Please speak the text aloud. Press 'Start' and speak into the microphone.")
    
    recognized_text = recognize_speech_from_mic()
    
    if recognized_text:
        # Translate recognized speech into the selected language
        translated_recognition = translate_text(recognized_text, target_language=lang_choice)
        st.write(f"Converted Speech to Text: {recognized_text}")
        st.write(f"Cloned speech will be in {lang_choice} language: {translated_recognition}")
        
        # Generate cloned voice
        generate_speech(translated_recognition)  # Can be replaced with voice cloning
        st.audio("output.mp3", format='audio/mp3')

# Option to upload a custom voice model (Advanced option for real cloned voice)
uploaded_file = st.file_uploader("Upload Custom Voice Model (Optional)", type=["pkl", "h5", "pt"])

# You can add logic to handle custom models and integrate voice cloning techniques here.
