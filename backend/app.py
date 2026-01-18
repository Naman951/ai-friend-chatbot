from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
HF_API_KEY = os.getenv('HF_API_KEY', '')
HF_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
CHAT_HISTORY_FILE = "chat_history.json"

# Simple AI responses (fallback)
AI_RESPONSES = {
    "hello": "Hey there! How are you doing today? 😊",
    "hi": "Hi! Great to see you! What's on your mind? 💭",
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "thanks": "You're welcome! Happy to help! 🙌",
    "goodbye": "Goodbye! Talk to you later! 👋",
    "bye": "See you soon! Take care! 👋",
    "help": "I'm here to chat with you! Just type anything and I'll respond. What would you like to talk about?",
    "who are you": "I'm your AI friend! I'm here to have fun conversations with you! 🤖💜",
    "what can you do": "I can chat with you about anything! Try asking me questions or telling me about your day!",
}

def get_fallback_response(user_input):
    """Generate a simple response when API is unavailable."""
    user_lower = user_input.lower().strip()
    
    # Check for keyword matches
    for keyword, response in AI_RESPONSES.items():
        if keyword in user_lower:
            return response
    
    # Generic responses
    generic_responses = [
        "That's interesting! Tell me more! 🤔",
        "Wow, I didn't know that! What else? 😊",
        "That sounds cool! How did that happen? 🎉",
        "Oh interesting! I like that! ✨",
        "Tell me more about that! 👂",
        "That's awesome! What else is on your mind? 💭",
        "I hear you! That's really something! 🌟",
    ]
    
    return random.choice(generic_responses)

def load_chat_history():
    """Load chat history from JSON file."""
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading chat history: {e}")
    return {"messages": []}

def save_chat_history(history):
    """Save chat history to JSON file."""
    try:
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving chat history: {e}")

def generate_response(user_input):
    """Get AI response from Hugging Face API with fallback."""
    if not user_input or not user_input.strip():
        return "Please say something! 😊"
    
    # Try Hugging Face API first if key is set
    if HF_API_KEY and HF_API_KEY != 'your_hugging_face_api_key_here':
        try:
            print(f"🔄 Trying Hugging Face API...")
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": user_input}
            
            response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=20)
            
            print(f"📊 API Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '').strip()
                    if text.startswith(user_input):
                        text = text[len(user_input):].strip()
                    if text:
                        print(f"✅ Got HF response!")
                        return text
            elif response.status_code == 503:
                print("⏳ Model loading... using fallback")
                return get_fallback_response(user_input)
            else:
                print(f"⚠️ API error {response.status_code}, using fallback")
                return get_fallback_response(user_input)
        except Exception as e:
            print(f"❌ HF API failed: {e}, using fallback")
            return get_fallback_response(user_input)
    
    # Use fallback if no API key or API failed
    print("📌 Using fallback AI")
    return get_fallback_response(user_input)

# Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle incoming chat messages."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Generate AI response
        bot_response = generate_response(user_message)
        
        # Save to history
        history = load_chat_history()
        history["messages"].append({
            "type": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        history["messages"].append({
            "type": "ai",
            "content": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        save_chat_history(history)
        
        return jsonify({"response": bot_response, "status": "success"})
    
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all chat messages."""
    try:
        history = load_chat_history()
        return jsonify(history)
    except Exception as e:
        print(f"History endpoint error: {e}")
        return jsonify({"error": str(e), "messages": []}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear all chat messages."""
    try:
        save_chat_history({"messages": []})
        return jsonify({"message": "Chat cleared successfully", "status": "success"})
    except Exception as e:
        print(f"Clear endpoint error: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "api_configured": bool(HF_API_KEY and HF_API_KEY != 'your_hugging_face_api_key_here'),
        "mode": "huggingface_api" if (HF_API_KEY and HF_API_KEY != 'your_hugging_face_api_key_here') else "fallback_ai"
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Friend Chatbot Backend...")
    print(f"📍 Running on http://localhost:5000")
    print(f"✅ CORS enabled for all origins")
    if HF_API_KEY and HF_API_KEY != 'your_hugging_face_api_key_here':
        print(f"🤖 Mode: Hugging Face API")
    else:
        print(f"💬 Mode: Fallback AI (built-in responses)")
    app.run(debug=True, port=5000, host='0.0.0.0')
