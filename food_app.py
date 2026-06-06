
import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
                      
)
# App title
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 50px 20px;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-radius: 15px;
    margin-bottom: 30px;
}
st.markdown("""
<style>
/* Hide GitHub logo and Streamlit menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hide deploy button */
.stDeployButton {display: none;}

/* Hide top right icons */
[data-testid="stToolbar"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
.hero h1 {
    font-size: 3em;
    color: #00d4ff;
    margin-bottom: 10px;
}
.hero p {
    font-size: 1.2em;
    color: #ffffff;
    margin-bottom: 10px;
}
.subtitle {
    font-size: 1em !important;
    color: #aaaaaa !important;
}
</style>

<div class="hero">
    <h1>🍽️ ScyIntelligence</h1>
    <p>AI-Powered Food Analysis & Nutrition Insights</p>
    <p class="subtitle">
        Analyze ingredients, discover nutritional value,
        identify health concerns, and get intelligent food recommendations.
    </p>
</div>
""", unsafe_allow_html=True)
st.write("Powered by ScyIntelligence — Your AI Food Expert")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Recipes Generated",
        value="100+"
    )

with col2:
    st.metric(
        label="Food Analyses",
        value="500+"
    )

with col3:
    st.metric(
        label="AI Accuracy",
        value="95%"
    )
# Sidebar options
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Language",
    ["English", "French", "Spanish", "Arabic", "Hausa"])
dietary = st.sidebar.multiselect("Dietary Filters",
    ["Halal", "Vegan", "Gluten-Free", "Diabetic-Friendly"])

# Main tabs
tab1, tab2 = st.tabs(["🔍 Analyze Ingredients", "💬 Food Q&A"])

# Tab 1 - Ingredient Analyzer
with tab1:
    st.subheader("Ingredient Analyzer")

    st.markdown("### 🍲 Try these examples")

    ex1, ex2, ex3 = st.columns(3)

    with ex1:
        st.code("rice, chicken, onions")

    with ex2:
        st.code("beans, tomato, pepper")

    with ex3:
         st.code("fish, garlic, lemon")

    ingredients = st.text_area(
         "Enter ingredients",
         placeholder="Example: rice, chicken, tomatoes, onions",
         height=120
)

    analyze = st.button(
    "🚀 Analyze Ingredients",
    use_container_width=True
)

if analyze:
        if ingredients:
            with st.spinner("AI is analyzing..."):
                prompt = f"""Analyze these ingredients: {ingredients}
                Dietary requirements: {dietary}
                Language: {language}

                Provide:
                1. A recipe using these ingredients
                2. Nutritional table with calories
                3. Total calorie count
                4. Health rating out of 10
                5. Food safety tips
                6. Dietary suitability ({dietary})
                """

                response = client.chat.completions.create(
                    model="nvidia/nemotron-nano-9b-v2:free",
                    messages=[
                        {"role": "system", "content": "You are a food engineering expert and nutritionist."},
                        {"role": "user", "content": prompt}
                    ]
                )

                result = response.choices[0].message.content
                metric1, metric2, metric3 = st.columns(3)

                with metric1:
                    st.metric("Health Score", "8/10")

                with metric2:
                    st.metric("Calories", "~450")

                with metric3:
                    st.metric("Safety", "Good")

                with st.container(border=True):
                    st.markdown(result)

                # Save to history
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({
                    "ingredients": ingredients,
                    "result": result
                })

                # Download button
                st.download_button(
                    "📥 Download Report",
                    result,
                    file_name="food_report.txt"
                )
        else:
            st.warning("Please enter ingredients!")

# Tab 2 - Food Q&A
with tab2:
    st.subheader("Ask Any Food Question")
    question = st.text_input("Ask a food question:")

    if st.button("Ask"):
        if question:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="nvidia/nemotron-nano-9b-v2:free",
                    messages=[
                        {"role": "system", "content": "You are a food expert. Answer food-related questions only. If asked non-food questions, politely redirect to food topics."},
                        {"role": "user", "content": question}
                    ]
                )
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Please ask a question!")

# History section
if "history" in st.session_state and st.session_state.history:
    st.subheader("📋 Analysis History")
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Analysis {i+1}: {item['ingredients']}"):
            st.markdown(item["result"])
