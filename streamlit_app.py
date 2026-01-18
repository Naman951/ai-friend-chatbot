import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Friend Chat",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .chat-message {
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            display: flex;
            animation: slideIn 0.3s ease-in;
        }
        .user-message {
            background: linear-gradient(135deg, #FF6B9D 0%, #C44569 100%);
            color: white;
            justify-content: flex-end;
            border-bottom-right-radius: 0.2rem;
        }
        .ai-message {
            background: linear-gradient(135deg, #FFE066, #FFA502);
            color: #333;
            justify-content: flex-start;
            border-bottom-left-radius: 0.2rem;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Configuration
HF_API_KEY = os.getenv('HF_API_KEY', '')
HF_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

# AI Fallback responses with personality
AI_RESPONSES = {
    # Greetings
    "hello": "Hey there! How are you doing today? 😊",
    "hi": "Hi! Great to see you! What's on your mind? 💭",
    "hey": "Hey! What's up? 👋",
    "greetings": "Hello! Nice to meet you! 💜",
    
    # How are you
    "how are you": "I'm doing great, thanks for asking! How about you? 😊",
    "how are u": "I'm amazing! Thanks for asking! What about you? 🌟",
    "how u doing": "I'm great! Living my best AI life! 🤖💜",
    
    # Personal questions
    "what is your name": "I'm your AI Friend! You can call me anything you like! 💜",
    "what's your name": "I'm your AI Friend! Nice to chat with you! 🤖",
    "your name": "I don't have a specific name, but I'm your AI Friend! 💜",
    "who are you": "I'm your AI friend! I'm here to have fun conversations with you! 🤖💜",
    
    "what is your age": "I'm brand new! I was just created to chat with you! 🎂",
    "what's your age": "Age is just a number! I'm timeless! ✨",
    "how old are you": "I'm as old as our conversation! Born to chat with you! 🚀",
    
    "where are you from": "I live in the cloud! ☁️ That's where all AI friends hang out! 🤖",
    "what's your gender": "I'm genderless! Just a friendly AI here to chat! 💜",
    
    # What you can do
    "what can you do": "I can chat with you about anything! Ask me questions, tell me about your day, or just have fun! 🎉",
    "what can u do": "I'm here to chat, listen, and be your AI friend! What would you like to talk about? 💬",
    "your abilities": "I can chat, listen, and make you smile! That's what I do best! 😊",
    
    # Gratitude
    "thanks": "You're welcome! Happy to help! 🙌",
    "thank you": "Anytime! I'm always here for you! 💜",
    "thx": "No problem! 😄",
    "appreciate": "Aw, thanks! I appreciate you too! 💕",
    
    # Goodbye
    "goodbye": "Goodbye! Talk to you later! 👋",
    "bye": "See you soon! Take care! 👋",
    "bye bye": "Bye! Come chat with me again! 👋😊",
    "gotta go": "No problem! See you soon! 👋",
    
    # Help & Support
    "help": "I'm here to chat with you! Just type anything and I'll respond. What would you like to talk about?",
    "can you help": "Of course! I'm here to help however I can! What do you need? 💪",
    
    # Other questions
    "why are you here": "I'm here to be your AI friend and chat with you! Making friends is my passion! 💜",
    "are you real": "I'm as real as AI can be! And I'm here for you! 🤖✨",
    "are you human": "Nope! I'm an AI, but I'm a very friendly one! 🤖💜",
    "do you sleep": "Nope! I'm always awake and ready to chat! 💪",
    "what do you like": "I like chatting with you! You're awesome! 🌟",
}

# Fallback responses for unknown questions
GENERIC_RESPONSES = [
    "That's interesting! Tell me more! 🤔",
    "Wow, I didn't know that! What else? 😊",
    "That sounds cool! How did that happen? 🎉",
    "Oh interesting! I like that! ✨",
    "Tell me more about that! 👂",
    "That's awesome! What else is on your mind? 💭",
    "I hear you! That's really something! 🌟",
    "Sounds fun! Keep going! 🎊",
    "Nice! I like your style! 😄",
    "That's pretty cool! 👍",
    "Definitely! Tell me more! 📢",
    "Awesome! You're fun to chat with! 🤩",
    "Love that energy! 💥",
    "That's sweet! 💕",
    "Amazing! What else? 🚀",
]

def get_fallback_response(user_input):
    """Generate fallback response"""
    user_lower = user_input.lower().strip()
    
    for keyword, response in AI_RESPONSES.items():
        if keyword in user_lower:
            return response
    
    import random
    return random.choice(GENERIC_RESPONSES)

def generate_response(user_input):
    """Generate AI response"""
    if not user_input or not user_input.strip():
        return "Please say something! 😊"
    
    # Try Hugging Face API if key is set
    if HF_API_KEY and HF_API_KEY != 'your_hugging_face_api_key_here':
        try:
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": user_input}
            
            response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '').strip()
                    if text.startswith(user_input):
                        text = text[len(user_input):].strip()
                    if text:
                        return text
            elif response.status_code == 503:
                return "The AI is warming up... please try again in a moment! ⏳"
            
            return get_fallback_response(user_input)
        except Exception as e:
            return get_fallback_response(user_input)
    
    # Use fallback if no API key
    return get_fallback_response(user_input)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("# 💜 AI Friend Chat")
st.markdown("### Always here to chat with you!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message... 💬")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI response
    with st.spinner("🤔 Thinking..."):
        ai_response = generate_response(user_input)
    
    # Add AI message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Display AI message
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Chat Stats")
    total_messages = len(st.session_state.messages)
    user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
    ai_messages = total_messages - user_messages
    
    st.metric("Total Messages", total_messages)
    st.metric("Your Messages", user_messages)
    st.metric("AI Responses", ai_messages)
    
    st.markdown("---")
    st.markdown("### 💡 About")
    st.markdown("""
    **AI Friend Chat** is your personal AI companion powered by Hugging Face!
    
    - 💬 Chat about anything
    - 💾 Automatic chat history
    - 🤖 Intelligent responses
    - 🎨 Beautiful UI
    
    **Mode:** Hugging Face API + Fallback AI
    """)
