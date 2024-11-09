from dotenv import load_dotenv
import google.generativeai as genai
import os

# Configure the API key for Gemini from the environment variable
load_dotenv()
genai_api_key = os.getenv('GEMINI_API_KEY')
if genai_api_key:
    genai.configure(api_key=genai_api_key)
else:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Create a Generative Model instance
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"}
    ]
)

def generate_response(query, context=None):
    # Send the user's query and get the response
    response = chat.send_message(query)
    return response.text

# Example usage
print(generate_response("I have 2 dogs in my house."))
