import os
from dotenv import load_dotenv
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def query_together(prompt, model="llama-3.3-70b-versatile", max_tokens=2048):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Determine if this is a JSON request based on prompt content
    is_json_request = "JSON" in prompt and "{" in prompt and "}" in prompt
    
    # Create a system message that emphasizes JSON formatting if needed
    system_message = (
        "You are a helpful AI assistant that provides concise, accurate responses. " +
        ("When asked to return JSON, you MUST return ONLY valid, properly formatted JSON with no additional text, " +
         "markdown formatting, or explanations outside the JSON object." if is_json_request else "")
    )
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if "choices" not in result or not result["choices"]:
            raise ValueError("Invalid response format from API")
            
        return result["choices"][0]["message"]["content"].strip()
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise RuntimeError(f"LLM API error: {str(e)}")
    except (KeyError, ValueError) as e:
        print(f"Error processing API response: {e}")
        raise RuntimeError(f"Invalid API response: {str(e)}")

if __name__ == "__main__":
    test_prompt = "Classify this slide content: 'Our team has 10 years of experience in fintech product development.' Return only one category from: Problem, Solution, Market, Business Model, Competition, Team, Financials, Traction, Funding Ask."
    try:
        result = query_together(test_prompt)
        print("LLM Response:", result)
    except Exception as e:
        print("Error:", e)