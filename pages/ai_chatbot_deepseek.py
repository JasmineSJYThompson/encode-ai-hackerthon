import streamlit as st
import requests
import openai

# -----------------------------
# Configure OpenRouter via the OpenAI client.
# -----------------------------
# Replace with your OpenRouter API key.
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = OPENROUTER_API_KEY

# -----------------------------
# Function to fetch news from NewsAPI.
# -----------------------------
def get_news_data(query):
    """
    Retrieves recent cryptocurrency/DeFi news using NewsAPI.
    Change the 'q' parameter as needed for broader or more focused queries.
    """
    # Replace with your actual NewsAPI key (or add it to your Streamlit secrets).
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "cryptocurrency OR DeFi",  # Query for crypto or DeFi articles.
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,   # Retrieve top 5 articles.
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract headlines from the articles.
            headlines = [article.get("title", "No Title") for article in data.get("articles", [])]
            # In this example, we set sentiment to "Neutral".
            sentiment = "Neutral"
            return {"news": headlines, "sentiment": sentiment}
        else:
            st.error(f"NewsAPI error: {response.status_code} - {response.text}")
            return {"news": ["No news available."], "sentiment": "Neutral"}
    except Exception as e:
        st.error(f"NewsAPI request failed: {e}")
        return {"news": [f"Error: {e}"], "sentiment": "Neutral"}

# -----------------------------
# Function to generate AI response using OpenRouter (via OpenAI client).
# -----------------------------
def generate_ai_response(user_query, news_data):
    # Combine the news headlines into a simple context string.
    news_context = "\n".join(news_data.get("news", []))
    prompt = f"""
You are a knowledgeable AI assistant specializing in DeFi and cryptocurrency.
Based on these news headlines:
{news_context}
Overall sentiment: {news_data.get("sentiment")}

Answer the following question briefly:
Q: {user_query}
A:"""
    
    #st.write("**Prompt sent to OpenRouter:**", prompt)  # Optional debug output
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        # Removed extra_headers so that the default authorization is used.
        completion = openai.ChatCompletion.create(
            model="openai/gpt-4o",  # as per OpenRouter docs
            messages=messages,
            max_tokens=150  # Adjust as necessary
        )
        #st.write("**Raw API Response:**", completion)  # Optional debug output
        
        if "choices" in completion and len(completion["choices"]) > 0:
            answer = completion["choices"][0]["message"]["content"].strip()
            return answer
        else:
            return f"Error: Unexpected API response structure. Full response: {completion}"
    except Exception as e:
        return f"Error communicating with OpenRouter API: {e}"


# -----------------------------
# Streamlit UI for the chatbot.
# -----------------------------
def run_chatbot():
    st.title("🧠 AI Chatbot Deepseek")
    st.markdown(
        "Ask any question about the cryptocurrency or DeFi market. "
        "The AI assistant fetches real-time news from NewsAPI and uses DeepSeek to generate its response."
    )
    
    user_query = st.text_input("Enter your question:")
    if st.button("Send") and user_query:
        st.info("Fetching news data from NewsAPI...")
        news_data = get_news_data(user_query)
        st.info("Generating AI response from DeepSeek (via OpenRouter)...")
        answer = generate_ai_response(user_query, news_data)
        st.markdown("### AI Response:")
        st.write(answer)
        
        with st.expander("View Raw News Data"):
            st.json(news_data)

if __name__ == "__main__":
    run_chatbot()
