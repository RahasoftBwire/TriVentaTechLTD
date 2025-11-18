/**
 * TriVenta Tech AI Chatbot - Frontend Integration
 * Replace the existing chatbot code in index.html with this enhanced version
 * 
 * Features:
 * - Connects to AI backend for human-like responses
 * - Maintains session across page refreshes
 * - Shows typing indicators
 * - Displays suggestions
 * - Handles errors gracefully
 * - Falls back to rule-based if backend unavailable
 */

// Configuration
const CHATBOT_CONFIG = {
    backendURL: 'http://localhost:8000',  // Change to your deployed URL
    enableBackend: true,  // Set to false to use rule-based fallback
    sessionStorageKey: 'triventatech_chat_session',
    typingDelay: 1000
};

// Get or create session ID
function getSessionId() {
    let sessionId = localStorage.getItem(CHATBOT_CONFIG.sessionStorageKey);
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem(CHATBOT_CONFIG.sessionStorageKey, sessionId);
    }
    return sessionId;
}

// Send message to AI backend
async function sendToAIBackend(message, userName) {
    const sessionId = getSessionId();
    
    try {
        const response = await fetch(`${CHATBOT_CONFIG.backendURL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                user_name: userName || null,
                context: {}
            }),
            timeout: 30000  // 30 second timeout
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        return {
            response: data.response,
            intent: data.intent,
            sentiment: data.sentiment,
            suggestions: data.suggestions || [],
            context: data.context || {}
        };
        
    } catch (error) {
        console.error('AI Backend Error:', error);
        return null;  // Will fallback to rule-based
    }
}

// Enhanced message handler with AI integration
async function handleChatMessageEnhanced(message) {
    const chatDisplay = document.getElementById('chatDisplay');
    const sessionId = getSessionId();
    
    // Add user message to chat
    chatDisplay.innerHTML += `
        <div class="chat-message user-message">
            <div class="message-content">${escapeHtml(message)}</div>
            <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
        </div>
    `;
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'chat-message bot-message typing-indicator';
    typingIndicator.innerHTML = `
        <div class="message-content">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
    `;
    chatDisplay.appendChild(typingIndicator);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
    
    let botResponse = null;
    let suggestions = [];
    
    // Try AI backend first
    if (CHATBOT_CONFIG.enableBackend) {
        const aiResponse = await sendToAIBackend(message, conversationContext.userName);
        if (aiResponse) {
            botResponse = aiResponse.response;
            suggestions = aiResponse.suggestions;
            
            // Update context with AI insights
            if (aiResponse.context) {
                conversationContext.sentiment = aiResponse.sentiment;
                conversationContext.lastIntent = aiResponse.intent;
            }
        }
    }
    
    // Fallback to rule-based if backend fails
    if (!botResponse) {
        botResponse = analyzeAndRespond(message);  // Your existing function
    }
    
    // Remove typing indicator
    typingIndicator.remove();
    
    // Add bot response
    let responseHTML = `
        <div class="chat-message bot-message">
            <div class="message-content">${botResponse}</div>
            <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
    `;
    
    // Add suggestions if available
    if (suggestions.length > 0) {
        responseHTML += `
            <div class="message-suggestions">
                ${suggestions.map(s => `
                    <button class="suggestion-btn" onclick="sendSuggestion('${escapeHtml(s)}')">
                        ${escapeHtml(s)}
                    </button>
                `).join('')}
            </div>
        `;
    }
    
    responseHTML += `</div>`;
    
    chatDisplay.innerHTML += responseHTML;
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
    
    // Save to conversation history
    conversationContext.conversationHistory.push(
        { role: 'user', content: message, timestamp: new Date() },
        { role: 'bot', content: botResponse, timestamp: new Date() }
    );
}

// Send suggestion when clicked
function sendSuggestion(text) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = text;
    sendMessage();  // Your existing send function
}

// HTML escape utility
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add CSS for new features
const enhancedStyles = `
    <style>
        /* Typing indicator */
        .typing-indicator {
            opacity: 0.7;
        }
        
        .typing-indicator .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        /* Suggestions */
        .message-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        
        .suggestion-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .suggestion-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Message timestamp */
        .message-timestamp {
            font-size: 11px;
            opacity: 0.6;
            margin-top: 5px;
        }
    </style>
`;

// Inject enhanced styles
document.head.insertAdjacentHTML('beforeend', enhancedStyles);

// Replace the existing sendMessage function
// Comment out the old one and use this:
/*
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (message) {
        handleChatMessageEnhanced(message);
        chatInput.value = '';
    }
}
*/

// Health check on page load
async function checkBackendHealth() {
    if (!CHATBOT_CONFIG.enableBackend) return;
    
    try {
        const response = await fetch(`${CHATBOT_CONFIG.backendURL}/health`, {
            method: 'GET',
            timeout: 5000
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✓ AI Chatbot Backend Connected:', data);
            console.log('  Provider:', data.llm_provider);
            console.log('  Version:', data.version);
        } else {
            console.warn('⚠ AI Backend health check failed, using fallback');
            CHATBOT_CONFIG.enableBackend = false;
        }
    } catch (error) {
        console.warn('⚠ AI Backend unavailable, using fallback:', error.message);
        CHATBOT_CONFIG.enableBackend = false;
    }
}

// Run health check on page load
document.addEventListener('DOMContentLoaded', () => {
    checkBackendHealth();
});
