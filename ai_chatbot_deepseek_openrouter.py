import streamlit as st
import openai

# -----------------------------
# Set up the API key and OpenRouter base URL.
# -----------------------------
# Retrieve the API key from Streamlit secrets (or replace with your key)
OPENROUTER_API_KEY = "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"

# Configure the OpenAI client to use OpenRouter’s API base.
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = OPENROUTER_API_KEY

# -----------------------------
# Function to retrieve (or simulate) news data.
# -----------------------------
def get_news_data(query):
    """
    For demonstration purposes, this function returns simulated news data.
    Replace this with a real API call (e.g., Sentifi) if desired.
    """
    simulated_news = {
        "news": [
            "Crypto adoption surges as global markets show mixed signals."
            # "Institutional interest in DeFi grows despite volatility concerns.",
            # "Regulatory debates spark uncertainty across the crypto ecosystem."
        ],
        "sentiment": "Neutral"
    }
    return simulated_news

# -----------------------------
# Function to generate AI chatbot responses using OpenRouter via OpenAI's API.
# -----------------------------
def generate_ai_response(user_query, news_data):
    # Limit the news headlines to reduce overall token count.
    news_headlines = news_data.get("news", [])[:2]
    news_context = "\n".join(news_headlines)
    prompt = f"""
You are a knowledgeable AI assistant specializing in DeFi and cryptocurrency.
Based on these news headlines:
{news_context}
Overall sentiment: {news_data.get("sentiment")}

Answer the following question briefly:
Q: {user_query}
A:"""
    
    st.write("**Prompt sent to OpenRouter:**", prompt)  # Debug output
    
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=messages,
            extra_headers={
                "HTTP-Referer": "https://your-site.example.com",
                "X-Title": "YourSiteName"
            },
            max_tokens=150  # Lower max_tokens to fit your credit limit
        )
        
        st.write("**Raw API Response:**", completion)
        
        if "choices" in completion and len(completion["choices"]) > 0:
            answer = completion["choices"][0]["message"]["content"].strip()
            return answer
        else:
            return f"Error: Unexpected API response structure. Full response: {completion}"
    except Exception as e:
        return f"Error communicating with OpenRouter DeepSeek API: {e}"



# -----------------------------
# Streamlit UI for the chatbot.
# -----------------------------
def run_chatbot():
    st.title("🧠 DeFi Chatbot Powered by DeepSeek (via OpenRouter)")
    st.markdown(
        "Ask any question about the cryptocurrency or DeFi market. The AI assistant uses recent news with DeepSeek "
        "to generate its response."
    )
    
    user_query = st.text_input("Enter your question:")
    if st.button("Send") and user_query:
        st.info("Fetching news data...")
        news_data = get_news_data(user_query)
        st.info("Generating AI response from DeepSeek (via OpenRouter)...")
        answer = generate_ai_response(user_query, news_data)
        st.markdown("### AI Response:")
        st.write(answer)
        
        with st.expander("View Raw News Data"):
            st.json(news_data)

if __name__ == "__main__":
    run_chatbot()
