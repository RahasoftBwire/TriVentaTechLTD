# Bwire Global Tech AI Chatbot - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get an API Key (Choose One)

#### Option A: OpenAI (Recommended for beginners)
1. Go to https://platform.openai.com/signup
2. Create account
3. Go to API Keys: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. **Cost**: ~$0.002 per conversation (very cheap)

#### Option B: Anthropic Claude
1. Go to https://console.anthropic.com/
2. Create account
3. Get API key from dashboard
4. **Cost**: Similar to OpenAI, high quality

#### Option C: Free Tier (Limited)
- Use HuggingFace free tier
- Limited requests but completely free

### Step 2: Install & Configure

```powershell
# Navigate to backend folder
cd chatbot-backend

# Run setup script (does everything automatically)
.\setup.ps1

# Edit .env file and paste your API key
notepad .env
```

**In .env file:**
```env
# Paste your API key here
OPENAI_API_KEY=sk-your-key-paste-here

# Keep these settings
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

Save and close.

### Step 3: Start the Server

```powershell
# Activate environment (if not already)
.\venv\Scripts\Activate

# Start server
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test It Works

**Open browser:** http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "llm_status": "active"
}
```

### Step 5: Connect to Your Website

Two options:

#### Option A: Use the provided integration (Easy)
1. Copy `frontend-integration.js` to your website folder
2. Include it in index.html **after** your existing chatbot code:
```html
<script src="frontend-integration.js"></script>
```

#### Option B: Quick Test (Immediate)
Open browser console on your website and run:
```javascript
// Test the AI backend
fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: 'Hello, I need a website!',
        user_name: 'Test User'
    })
})
.then(r => r.json())
.then(data => console.log('AI Response:', data.response));
```

### Step 6: Deploy to Internet (Make it Live)

#### Easiest: Render.com (Free Tier)

1. **Push code to GitHub:**
```powershell
cd chatbot-backend
git init
git add .
git commit -m "Initial chatbot backend"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/chatbot-backend.git
git push -u origin main
```

2. **Deploy on Render:**
- Go to https://render.com/
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Fill in:
  - **Name**: triventatech-chatbot
  - **Environment**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add Environment Variables:
  - `OPENAI_API_KEY`: your-key-here
  - `ALLOWED_ORIGINS`: https://www.triventatech.com,https://triventatech.com
- Click "Create Web Service"

3. **Update your website:**
In `frontend-integration.js`, change:
```javascript
backendURL: 'https://triventatech-chatbot.onrender.com'
```

**Done!** Your chatbot is now powered by AI! 🎉

---

## 📊 What You Get

### Without AI Backend (Current)
- ✓ Rule-based responses
- ✓ Pattern matching
- ✓ Basic context
- ✗ Limited understanding
- ✗ Repetitive responses
- ✗ Can't handle variations

### With AI Backend (New!)
- ✓ Human-like understanding
- ✓ Natural conversations
- ✓ Emotional intelligence
- ✓ Learns from context
- ✓ Handles typos/variations
- ✓ Multi-language support
- ✓ Intent detection
- ✓ Sentiment analysis
- ✓ Proactive suggestions

---

## 💰 Cost Breakdown

### Development (Local Testing)
- **Free!** Test unlimited on localhost

### Production (Live Website)
Assuming 1000 conversations/month:

**OpenAI GPT-3.5:**
- Cost: ~$1-3/month
- Speed: Very fast
- Quality: Excellent

**OpenAI GPT-4:**
- Cost: ~$15-30/month
- Speed: Fast
- Quality: Outstanding

**Anthropic Claude:**
- Cost: ~$5-10/month
- Speed: Fast
- Quality: Excellent

**Hosting (Render Free Tier):**
- Cost: $0/month
- Limitations: Sleeps after inactivity, 750 hours/month

**Hosting (Render Paid):**
- Cost: $7/month
- Always active, faster

**Total Monthly Cost:**
- **Budget**: $1-3 (GPT-3.5 + Free hosting)
- **Recommended**: $10-15 (GPT-3.5 + Paid hosting)
- **Premium**: $40-50 (GPT-4 + Paid hosting)

---

## 🔧 Troubleshooting

### "Import errors" when starting
```powershell
pip install -r requirements.txt
```

### "OpenAI API key not set"
Check your .env file has:
```env
OPENAI_API_KEY=sk-...
```

### "Connection refused"
Make sure server is running:
```powershell
python main.py
```

### "CORS error" in browser
Add your website domain to `.env`:
```env
ALLOWED_ORIGINS=http://localhost,https://www.triventatech.com
```

### Backend works but chatbot doesn't use it
Check `frontend-integration.js`:
```javascript
enableBackend: true  // Make sure this is true
backendURL: 'http://localhost:8000'  // Correct URL
```

---

## 📞 Need Help?

**Email**: bilfordderek917@gmail.com  
**WhatsApp**: +254722206805  
**Website**: https://www.triventatech.com

---

## 🎯 Next Steps

1. ✅ Get API key
2. ✅ Run `setup.ps1`
3. ✅ Edit `.env`
4. ✅ Run `python main.py`
5. ✅ Test at http://localhost:8000/health
6. ✅ Integrate with website
7. ✅ Deploy to Render/Railway
8. ✅ Update website with live URL

**You're ready to have the most intelligent chatbot!** 🚀
