# AI Friend Chatbot 💜

A simple, colorful AI chatbot with chat memory and easy deployment!

**Simple Setup • Beautiful UI • Hugging Face Powered • Cloud Ready**

---

## 🎨 Features

✨ **Hugging Face API** - Uses DialoGPT model  
💾 **Chat Memory** - Saves all conversations  
🌈 **Colorful UI** - Vibrant playful design  
⚡ **Super Simple** - Just Python + HTML  
🚀 **Easy Deploy** - Frontend on Vercel, Backend on Railway  

---

## 📁 Project Structure

```
today_pro/
├── backend/
│   ├── app.py              # Flask backend
│   ├── requirements.txt    # Python packages
│   ├── .env                # Configuration
│   └── chat_history.json   # Chat data
│
└── frontend/
    └── index.html          # Complete UI (one file!)
```

**That's it! No complex build tools needed.**

---

## 🚀 Quick Start (Local)

### 1. Get Hugging Face API Key
1. Go to https://huggingface.co
2. Sign up (free)
3. Go to Settings → Access Tokens
4. Create a new token (read access is fine)
5. Copy the token

### 2. Start Backend

```bash
cd backend
pip install -r requirements.txt
```

Update `.env` with your Hugging Face API key:
```
HF_API_KEY=your_token_here
```

Then run:
```bash
python app.py
```

✅ Backend running on `http://localhost:5000`

### 3. Open Frontend

Simply open `frontend/index.html` in your browser!

```bash
# Or serve it with Python
cd frontend
python -m http.server 8000
# Then visit http://localhost:8000
```

✅ Start chatting! 💬

---

## 🌍 Deploy to Cloud

### Deploy Backend on Railway

1. Push your `backend/` folder to GitHub
2. Go to https://railway.app
3. Sign up (free)
4. Create New Project → Deploy from GitHub
5. Select your repo → Deploy backend folder
6. Add Environment Variable:
   - Key: `HF_API_KEY`
   - Value: Your Hugging Face token
7. Railway gives you a public URL (e.g., `https://your-app.railway.app`)

### Deploy Frontend on Vercel

1. Create a `vercel.json` in your frontend folder:

```json
{
  "buildCommand": "",
  "outputDirectory": ".",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-cache"
        }
      ]
    }
  ]
}
```

2. Edit `index.html` and change:
```javascript
const API_URL = 'https://your-railway-url.railway.app';
```

3. Push to GitHub
4. Go to https://vercel.com
5. Import your repo
6. Deploy!

✅ Your app is now live! 🎉

---

## 📝 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Send message & get AI response |
| `/api/history` | GET | Get all chat messages |
| `/api/clear` | POST | Clear chat history |

### Example API Call

```javascript
fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello!' })
})
.then(r => r.json())
.then(data => console.log(data.response));
```

---

## 🎨 Customize

### Change Colors

Edit `frontend/index.html` CSS section:

```css
/* Primary color (pink) */
background: linear-gradient(135deg, #FF6B9D 0%, #C44569 100%);

/* Accent color (yellow/orange) */
background: linear-gradient(135deg, #FFE066, #FFA502);
```

Popular color combos:
- **Purple**: `#667eea` → `#764ba2`
- **Blue**: `#0984E3` → `#0B5394`
- **Green**: `#00B894` → `#00A651`

### Change AI Model

Edit `backend/app.py`:

```python
HF_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
```

Other models:
- `microsoft/DialoGPT-large` - Better quality, slower
- `gpt2` - Simpler, faster
- Any model from Hugging Face Hub

---

## ⚠️ Troubleshooting

**"CORS error" or "Backend not found"?**
- Make sure backend is running on port 5000
- Check firewall isn't blocking port 5000
- Restart backend: `python app.py`

**"API error" or "Invalid API key"?**
- Check your Hugging Face token is valid
- Go to huggingface.co and copy a new token
- Update `.env` and restart

**Frontend not connecting to backend?**
- Backend must be running first
- Check `const API_URL` in `index.html` is correct

**Deployment not working?**
- Make sure backend is public on Railway
- Update frontend API URL to your Railway URL
- Check environment variables are set

---

## 📦 What's Included

**Backend** (Python)
- Flask for API
- Flask-CORS for frontend connection
- Requests for Hugging Face API

**Frontend** (HTML/CSS/JS)
- No build tools needed!
- Vanilla JavaScript
- Pure CSS animations
- Responsive design

---

## 🎯 Next Steps

- Add user authentication
- Support image sharing
- Add more AI personalities
- Mobile app version
- Voice input/output

---

**Built with ❤️ using Hugging Face, Flask, and HTML5**
