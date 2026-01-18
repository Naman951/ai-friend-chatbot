# 💜 AI Friend Chat - Streamlit Edition

An intelligent chatbot with a beautiful UI powered by Hugging Face DialoGPT!

**Beautiful UI • Hugging Face Powered • Instant Deployment • No Complex Setup**

---

## 🎯 Features

✨ **Hugging Face DialoGPT** - State-of-the-art conversation AI  
💾 **Chat History** - Automatic session memory  
🌈 **Colorful UI** - Beautiful gradient design with animations  
⚡ **Super Simple** - Single Python file, easy to deploy  
🚀 **One-Click Deploy** - Deploy to Streamlit Cloud for free  
🤖 **Smart Fallback** - Works even without API (keyword + generic responses)  

---

## 📁 Project Structure

```
today_pro/
├── streamlit_app.py        # Complete app (UI + Backend)
├── requirements.txt        # Dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── .env                    # Environment variables
└── README.md               # This file
```

**That's it! Everything in one file!**

---

## 🚀 Quick Start (Local)

### 1. Get Hugging Face API Key
1. Go to https://huggingface.co
2. Sign up (free)
3. Go to Settings → Access Tokens
4. Create a new token (read access is fine)
5. Copy the token

### 2. Set Up & Run

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo HF_API_KEY=your_token_here > .env

# Run the app
streamlit run streamlit_app.py
```

✅ App opens at `http://localhost:8501` 💬

---

## 🌍 Deploy to Streamlit Cloud (Free!)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `ai-friend-chatbot`
5. Select branch: `main`
6. Select file path: `streamlit_app.py`
7. Click Deploy!

### Step 3: Add Your API Key

1. After deployment, click the "..." menu
2. Select "Settings"
3. Go to "Secrets"
4. Add this secret:
   ```
   HF_API_KEY = your_hugging_face_api_key_here
   ```
5. Save and the app auto-restarts

✅ Your app is live! Share the URL! 🚀

---

## 💡 How It Works

**Three-Layer AI System:**
1. **Hugging Face API** - Attempts to get smart responses from DialoGPT model
2. **Keyword Matching** - Falls back to predefined responses for common phrases
3. **Generic Fallback** - Responds with helpful generic messages

**If any step fails, the next takes over - always responds!**
---

## 🎨 Customize

### Change Colors

Edit `.streamlit/config.toml`:

```toml
primaryColor = "#FF6B9D"        # Main accent color
backgroundColor = "#667eea"    # Page background
secondaryBackgroundColor = "#764ba2"  # Sidebar background
textColor = "#FFFFFF"          # Text color
```

Popular color combos:
- **Purple**: `#667eea` → `#764ba2`
- **Blue**: `#0984E3` → `#0B5394`
- **Green**: `#00B894` → `#00A651`

### Change AI Model

Edit `streamlit_app.py`, find this line:

```python
HF_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
```

Change to other models:
- `DialoGPT-large` - Better quality, slower
- `gpt2` - Simpler, faster
- Any model from Hugging Face Hub

### Add More Fallback Responses

Edit the `AI_RESPONSES` dictionary in `streamlit_app.py`:

```python
AI_RESPONSES = {
    "hello": "Hey there! How are you doing today? 😊",
    "your custom phrase": "Your custom response!",
    # Add more here...
}
```

---

## ⚠️ Troubleshooting

**"App not running"?**
- Make sure you ran: `streamlit run streamlit_app.py`
- Check all dependencies installed: `pip install -r requirements.txt`
- Try reinstalling: `pip install --upgrade streamlit`

**"No API responses"?**
- Check `.env` file has `HF_API_KEY=your_key`
- Or set it in Streamlit Cloud secrets
- Verify key is valid at https://huggingface.co/settings/tokens
- Check your HF account hasn't run out of quota

**"API timeout or error"?**
- Hugging Face free tier has rate limits
- App will use fallback responses automatically
- Try again in a few seconds

**"Chat history lost on refresh"?**
- This is normal - Streamlit session state resets on refresh
- To add persistent storage, integrate a database like SQLite

---

## 📦 What's Included

- **Streamlit** for the web framework
- **Requests** for Hugging Face API calls
- **Python-dotenv** for environment variables
- **Beautiful CSS & animations** built into Streamlit
- **Session state** for chat history during session

---

## 🎯 Advanced Features

### Add Persistent Storage

Add SQLite to store chats permanently:

```python
import sqlite3

def save_to_db(user_msg, ai_response):
    conn = sqlite3.connect('chat.db')
    # Add your code here
```

### Add User Authentication

Use Streamlit's `@st.cache_resource`:

```python
import streamlit_authenticator as stauth
# Add authentication logic
```

### Deploy Custom Domain

Deploy to Streamlit Cloud then add custom domain in settings

---

## 📞 Support

- **GitHub Issues**: https://github.com/Naman951/ai-friend-chatbot/issues
- **Streamlit Docs**: https://docs.streamlit.io
- **HF API Docs**: https://huggingface.co/docs/api-inference
---

## 📞 Support

- **GitHub Issues**: https://github.com/Naman951/ai-friend-chatbot/issues
- **Streamlit Docs**: https://docs.streamlit.io
- **HF API Docs**: https://huggingface.co/docs/api-inference

---

## 🎓 Learning Resources

- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)
- [Hugging Face API Guide](https://huggingface.co/docs/api-inference)
- [DialoGPT Model](https://huggingface.co/microsoft/DialoGPT-medium)

---

## 🙌 Credits

- **Streamlit** - Making web apps simple
- **Hugging Face** - Providing free AI models  
- **DialoGPT** - The conversation model we use
- **You** - For using this project!

---

**Built with ❤️ using Streamlit, Hugging Face, and Python**

