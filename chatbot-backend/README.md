# Bwire Global Tech AI Chatbot Backend

## 🚀 Complete Human-Like AI Chatbot System

A production-ready, intelligent chatbot backend with advanced NLP, emotion detection, context awareness, and multi-LLM support.

### ✨ Features

#### 🧠 Advanced AI Capabilities
- **Multi-LLM Support**: OpenAI GPT-4, Anthropic Claude, HuggingFace models
- **Context Memory**: Short-term (current conversation) and long-term (user profiles)
- **Emotion Detection**: Detects joy, sadness, anger, fear, surprise, trust
- **Intent Classification**: Automatically understands user intentions
- **Sentiment Analysis**: Real-time positive/negative/neutral detection
- **Entity Extraction**: Extracts budget, timeline, contact info, URLs
- **Multi-language**: English + Swahili support

#### 💬 Natural Conversation
- **Human-like Responses**: Empathetic, contextual, and personality-driven
- **Fuzzy Matching**: Understands typos and variations
- **Conversation Tracking**: Remembers context across messages
- **Proactive Suggestions**: Provides relevant follow-up questions
- **Urgency Detection**: Prioritizes urgent requests

#### 🛠️ Technical Features
- **FastAPI Backend**: High-performance async Python framework
- **Vector Database**: ChromaDB/FAISS for semantic search
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate answers
- **Session Management**: Persistent conversations
- **Rate Limiting**: Prevents abuse
- **Safety Filters**: Content moderation and toxicity detection

### 📋 Requirements

- Python 3.10+
- API Key from OpenAI, Anthropic, or HuggingFace
- 2GB RAM minimum
- Optional: PostgreSQL, Redis

### 🔧 Installation

#### 1. Install Dependencies

```bash
cd chatbot-backend
pip install -r requirements.txt
```

#### 2. Download NLP Models

```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt vader_lexicon
```

#### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Required Configuration:**
```env
# Choose your LLM provider
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

# LLM Settings
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

#### 4. Run the Server

```bash
# Development
python main.py

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will start at: `http://localhost:8000`

### 🌐 API Endpoints

#### Health Check
```http
GET /health
```

#### Chat (Main Endpoint)
```http
POST /api/chat
Content-Type: application/json

{
  "message": "I need a website for my business",
  "session_id": "optional-session-id",
  "user_name": "John",
  "context": {}
}
```

**Response:**
```json
{
  "response": "Great! I'd love to help you with your website...",
  "session_id": "uuid-here",
  "intent": "web_development",
  "sentiment": "positive",
  "confidence": 0.85,
  "suggestions": [
    "What's the pricing?",
    "How long does it take?",
    "Show me your portfolio"
  ],
  "context": {
    "user_name": "John",
    "interested_services": ["Web Development"],
    "message_count": 2
  }
}
```

#### Get Conversation History
```http
GET /api/conversation/{session_id}
```

#### Delete Conversation
```http
DELETE /api/conversation/{session_id}
```

#### Submit Feedback
```http
POST /api/feedback?session_id=xxx&rating=5
```

### 🔗 Frontend Integration

Update your website's chatbot to call the backend API:

```javascript
async function sendMessageToAI(message, sessionId) {
    const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            session_id: sessionId,
            user_name: conversationContext.userName
        })
    });
    
    const data = await response.json();
    return data.response;
}
```

### 🚀 Deployment Options

#### Option 1: Render (Free Tier)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Add environment variables
5. Deploy

#### Option 2: Railway
```bash
railway login
railway init
railway up
```

#### Option 3: DigitalOcean App Platform
1. Create new app
2. Connect GitHub repo
3. Configure environment
4. Deploy

#### Option 4: AWS/Azure/GCP
Use Docker for containerized deployment:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 💰 Cost Estimates

#### API Costs (per 1000 conversations)
- **GPT-3.5-Turbo**: ~$0.50 - $2.00
- **GPT-4**: ~$10.00 - $30.00
- **Claude-3**: ~$5.00 - $15.00

#### Hosting Costs (monthly)
- **Render Free Tier**: $0 (limited)
- **Railway Hobby**: $5
- **DigitalOcean**: $12-25
- **AWS/Azure**: $20-100+

### 🧪 Testing

```bash
# Run tests
pytest

# Test API
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### 📊 Monitoring

Logs are stored in `logs/chatbot_{timestamp}.log`

View real-time logs:
```bash
tail -f logs/chatbot_*.log
```

### 🔒 Security

- API keys stored in environment variables
- CORS configured for your domains
- Rate limiting enabled
- Content filtering active
- Input validation on all endpoints

### 🎯 Customization

#### Change Personality
Edit `.env`:
```env
CHATBOT_PERSONALITY=professional  # or friendly, empathetic, technical
```

#### Add Custom Knowledge
Add to `data/knowledge_base.json` or populate database with company info.

#### Adjust Response Style
Modify system prompt in `app/services/llm_service.py`

### 📞 Support

- Email: bilfordderek917@gmail.com
- WhatsApp: +254722206805
- Website: https://www.triventatech.com

### 📄 License

© 2025 Bwire Global Tech. All rights reserved.

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Add your API key to `.env`
3. ✅ Run the server: `python main.py`
4. ✅ Test the API: Visit `http://localhost:8000/health`
5. ✅ Integrate with your website
6. ✅ Deploy to production

**You're ready to go!** 🚀
