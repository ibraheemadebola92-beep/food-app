
app_code = '''
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# Initialize client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]

# Multiple models with fallback
MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "poolside/laguna-xs.2:free",
    "baidu/cobuddy:free"
]

def ask_ai(messages):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except:
            continue
    return "I apologize, all models are currently unavailable. Please try again shortly."

def is_ingredient_list(text):
    food_keywords = ["rice", "beans", "tomato", "onion", "chicken", "beef", "fish", 
                    "egg", "milk", "flour", "sugar", "salt", "pepper", "garlic",
                    "potato", "carrot", "cabbage", "spinach", "yam", "plantain",
                    "pasta", "bread", "butter", "oil", "water", "corn", "wheat"]
    text_lower = text.lower()
    comma_count = text.count(",")
    keyword_found = any(keyword in text_lower for keyword in food_keywords)
    return comma_count >= 1 or keyword_found

# Hide Streamlit branding
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {visibility: hidden;}

* {
    font-family: "Segoe UI", sans-serif;
}

body {
    background-color: #0a0a0a;
}

/* Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000000;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 15%;
    font-weight: 500;
    box-shadow: 0 2px 10px rgba(255,215,0,0.3);
}

.ai-bubble {
    background: linear-gradient(135deg, #1a1500, #0a0a00);
    border: 1px solid #FFD700;
    color: #ffffff;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 15% 8px 0;
    box-shadow: 0 2px 10px rgba(255,215,0,0.1);
}

.ai-name {
    color: #FFD700;
    font-weight: bold;
    font-size: 0.85em;
    margin-bottom: 5px;
}

.user-name {
    color: #000000;
    font-weight: bold;
    font-size: 0.85em;
    margin-bottom: 5px;
}

/* Hero */
.hero {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #0a0a0a, #1a1500);
    border: 1px solid #FFD700;
    border-radius: 20px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 2.5em;
    color: #FFD700;
    font-weight: bold;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.hero p {
    color: #cccccc;
    font-size: 1em;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000000;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
    width: 100%;
}

/* Input */
.stTextInput > div > div > input {
    background: #1a1a1a;
    color: #ffffff;
    border: 1px solid #FFD700;
    border-radius: 10px;
}

/* Sidebar */
.stSidebar {
    background: #0a0a0a;
    border-right: 1px solid #FFD700;
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    color: #FFD700;
    border-top: 1px solid #FFD700;
    margin-top: 30px;
    font-size: 0.8em;
}

/* Welcome card */
.welcome-card {
    background: #1a1500;
    border: 1px solid #FFD700;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>👑 ScyIntelligence</h1>
    <p>AI-Powered Food Analysis & Nutrition Insights</p>
    <p style="color:#FFD700; font-size:0.85em;">Powered by SCY Intelligence AI Studio</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 👑 ScyIntelligence")
    st.markdown("---")
    
    user_name = st.text_input("Your Name:", placeholder="Enter your name")
    language = st.selectbox("🌍 Language", 
        ["English", "French", "Spanish", "Arabic", "Hausa", "Yoruba", "Igbo"])
    dietary = st.multiselect("🥗 Dietary Preferences",
        ["Halal", "Vegan", "Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Keto"])
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Type **hello** to start
    - List ingredients to analyze
    - Ask any food question
    - Type **clear** to reset chat
    """)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("*SCY Intelligence AI Studio*")
    st.markdown("*© 2026 All rights reserved*")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        name = user_name if user_name else "You"
        st.markdown(f"""
        <div class="user-bubble">
            <div class="user-name">{name}</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"""
        <div class="ai-bubble">
            <div class="ai-name">👑 ScyIntelligence</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input(
    "Message ScyIntelligence:",
    placeholder="Say hello or enter ingredients...",
    key="user_input"
)

col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    send_btn = st.button("Send 📨")
with col3:
    download_btn = st.button("📥 Save")

# Handle send
if send_btn and user_input:
    name = user_name if user_name else "User"
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Build system prompt
    system_prompt = f"""You are ScyIntelligence, a world-class AI food engineering expert created by SCY Intelligence AI Studio.

You speak professionally but warmly like a PhD food engineer.
Always address the user as {name}.
Respond in {language}.
Consider these dietary preferences: {dietary}.

When given ingredients:
- Provide a detailed recipe
- Full nutritional table with calories per ingredient
- Total calorie count
- Health score out of 10 with explanation
- Food safety tips
- Allergen warnings
- Shelf life information
- Food engineering insights (Maillard reaction, starch gelatinization etc.)
- Suitability for dietary preferences

When asked questions:
- Answer as a professional food engineering expert
- Be detailed but clear
- Use food science terminology appropriately

When greeted:
- Greet back warmly and professionally
- Introduce yourself briefly
- Ask how you can help

Only discuss food-related topics. If asked about non-food topics, politely redirect.
"""
    
    # Prepare messages for AI
    ai_messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in st.session_state.messages:
        if msg["role"] in ["user", "assistant"]:
            ai_messages.append(msg)
    
    # Get AI response
    with st.spinner("👑 ScyIntelligence is thinking..."):
        if is_ingredient_list(user_input):
            ai_messages[-1]["content"] = f"Please analyze these ingredients: {user_input}"
        
        reply = ask_ai(ai_messages)
    
    # Add AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    
    st.rerun()

# Handle download
if download_btn:
    if st.session_state.messages:
        chat_text = f"ScyIntelligence Chat Report\\n"
        chat_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n"
        chat_text += f"User: {user_name}\\n"
        chat_text += "="*50 + "\\n\\n"
        
        for msg in st.session_state.messages:
            role = user_name if msg["role"] == "user" else "ScyIntelligence"
            chat_text += f"{role}:\\n{msg['content']}\\n\\n"
        
        st.download_button(
            "📥 Download Chat",
            chat_text,
            file_name=f"scyintelligence_report_{datetime.now().strftime('%Y%m%d')}.txt"
        )
    else:
        st.warning("No chat to download yet!")

# Footer
st.markdown("""
<div class="footer">
    👑 ScyIntelligence AI Food System | 
    Powered by SCY Intelligence AI Studio | 
    Built with AI 🤖 | © 2026
</div>
""", unsafe_allow_html=True)
'''

with open("food_app.py", "w") as f:
    f.write(app_code)

print("ScyIntelligence Premium launched!")
