"""
TriVenta Tech AI Chatbot - NLP Processing Service
Handles intent classification, sentiment analysis, entity recognition, and context tracking
"""

from typing import Dict, List, Optional, Tuple
from textblob import TextBlob
import re
from loguru import logger


class NLPService:
    """Natural Language Processing Service"""
    
    def __init__(self):
        """Initialize NLP components"""
        self.intent_keywords = self._load_intent_keywords()
        logger.info("NLP Service initialized")
    
    def _load_intent_keywords(self) -> Dict[str, List[str]]:
        """Load intent classification keywords"""
        return {
            "greeting": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening",
                        "habari", "mambo", "jambo", "sasa", "vipi"],
            "goodbye": ["bye", "goodbye", "see you", "talk later", "gotta go", "kwaheri"],
            "thanks": ["thank", "thanks", "appreciate", "grateful", "asante"],
            
            # Service intents
            "web_development": ["website", "web", "site", "landing page", "web app", "web design"],
            "ai_ml": ["ai", "artificial intelligence", "machine learning", "ml", "data science",
                     "chatbot", "automation", "predict"],
            "cybersecurity": ["security", "cyber", "hack", "protect", "secure", "firewall",
                            "vulnerability", "penetration test"],
            "cloud": ["cloud", "aws", "azure", "hosting", "server", "infrastructure"],
            "mobile": ["mobile", "app", "android", "ios", "mobile app"],
            "training": ["train", "course", "learn", "teach", "workshop", "education"],
            
            # Business intents
            "pricing": ["price", "cost", "how much", "quote", "quotation", "budget", "fee"],
            "timeline": ["when", "how long", "duration", "timeline", "deadline", "time frame"],
            "contact": ["contact", "reach", "call", "email", "phone", "whatsapp", "location"],
            "portfolio": ["portfolio", "projects", "work", "examples", "past work", "case study"],
            "team": ["team", "who", "founders", "staff", "people", "about"],
            
            # Emotional intents
            "complaint": ["problem", "issue", "wrong", "not working", "disappointed", "frustrated"],
            "urgent": ["urgent", "asap", "immediately", "emergency", "quick", "fast", "now"],
            "help": ["help", "assist", "support", "stuck", "confused", "don't understand"]
        }
    
    def analyze_message(self, message: str) -> Dict:
        """Comprehensive message analysis"""
        
        message_lower = message.lower().strip()
        
        return {
            "intent": self.detect_intent(message_lower),
            "sentiment": self.analyze_sentiment(message),
            "emotions": self.detect_emotions(message_lower),
            "entities": self.extract_entities(message),
            "urgency": self.detect_urgency(message_lower),
            "language": self.detect_language(message_lower)
        }
    
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect user intent with confidence score"""
        
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in message:
                    # Exact word boundary match scores higher
                    if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                        score += 2
                    else:
                        score += 1
            
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return ("unknown", 0.0)
        
        # Get top intent
        top_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[top_intent]
        confidence = min(max_score / 10.0, 1.0)  # Normalize to 0-1
        
        return (top_intent, confidence)
    
    def analyze_sentiment(self, message: str) -> Dict:
        """Analyze sentiment using TextBlob"""
        
        try:
            blob = TextBlob(message)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
            
            if polarity > 0.1:
                sentiment_label = "positive"
            elif polarity < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return {
                "label": sentiment_label,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": abs(polarity)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {"label": "neutral", "polarity": 0.0, "subjectivity": 0.5, "confidence": 0.0}
    
    def detect_emotions(self, message: str) -> List[str]:
        """Detect emotional content"""
        
        emotions = []
        
        emotion_patterns = {
            "joy": ["happy", "excited", "great", "awesome", "wonderful", "fantastic", "love"],
            "sadness": ["sad", "disappointed", "unhappy", "regret", "sorry"],
            "anger": ["angry", "frustrated", "annoyed", "mad", "upset"],
            "fear": ["worried", "concerned", "afraid", "anxious", "nervous"],
            "surprise": ["wow", "amazing", "incredible", "surprising", "unexpected"],
            "trust": ["reliable", "trustworthy", "confident", "sure", "believe"]
        }
        
        for emotion, keywords in emotion_patterns.items():
            if any(keyword in message for keyword in keywords):
                emotions.append(emotion)
        
        return emotions if emotions else ["neutral"]
    
    def extract_entities(self, message: str) -> Dict:
        """Extract entities (budget, timeline, contact info, etc.)"""
        
        entities = {}
        
        # Extract budget
        budget_patterns = [
            r'(?:ksh|kes|shillings?)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*)\s*(?:ksh|kes|shillings?)',
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*)\s*dollars?',
            r'(\d+)k\b'  # e.g., "50k"
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities["budget"] = match.group(0)
                break
        
        # Extract timeline
        timeline_patterns = [
            r'(\d+)\s*(?:days?|weeks?|months?|years?)',
            r'(?:within|in)\s+(\d+\s+(?:days?|weeks?|months?))',
            r'(?:by|before)\s+(\w+\s+\d{1,2})'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities["timeline"] = match.group(0)
                break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        if email_match:
            entities["email"] = email_match.group(0)
        
        # Extract phone (Kenyan format)
        phone_patterns = [
            r'\+254\s*\d{9}',
            r'0\d{9}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, message)
            if match:
                entities["phone"] = match.group(0)
                break
        
        # Extract URLs
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        urls = re.findall(url_pattern, message)
        if urls:
            entities["urls"] = urls
        
        return entities
    
    def detect_urgency(self, message: str) -> str:
        """Detect urgency level"""
        
        urgent_keywords = ["urgent", "asap", "immediately", "emergency", "quickly", 
                          "right now", "right away", "fast", "soon as possible"]
        
        urgent_count = sum(1 for keyword in urgent_keywords if keyword in message)
        
        # Check for punctuation emphasis
        exclamation_count = message.count("!")
        
        if urgent_count >= 2 or exclamation_count >= 2:
            return "high"
        elif urgent_count >= 1 or exclamation_count >= 1:
            return "medium"
        else:
            return "normal"
    
    def detect_language(self, message: str) -> str:
        """Detect message language (simple heuristic)"""
        
        swahili_words = ["habari", "mambo", "jambo", "sasa", "vipi", "sijambo",
                        "nzuri", "poa", "asante", "karibu", "kwaheri"]
        
        swahili_count = sum(1 for word in swahili_words if word in message)
        
        if swahili_count >= 1:
            return "sw"  # Swahili
        else:
            return "en"  # English (default)
    
    def fuzzy_match(self, text: str, patterns: List[str], threshold: int = 3) -> bool:
        """Fuzzy string matching with Levenshtein distance"""
        
        text_lower = text.lower()
        
        for pattern in patterns:
            pattern_lower = pattern.lower()
            
            # Exact match
            if pattern_lower in text_lower:
                return True
            
            # Fuzzy match with simple edit distance
            distance = self._levenshtein_distance(text_lower, pattern_lower)
            if distance <= threshold and len(pattern_lower) > 3:
                return True
        
        return False
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


# Global NLP service instance
nlp_service = None

def get_nlp_service() -> NLPService:
    """Get or create NLP service instance"""
    global nlp_service
    if nlp_service is None:
        nlp_service = NLPService()
    return nlp_service
