from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
genai_api_key = os.getenv('OPENAI_API_KEY')
# Initialize OpenAI client
client = OpenAI(api_key=genai_api_key)

def generate_response(query, context=None):
    # Create a chat completion using the client
    completion = client.chat.completions.create(
        model="babbage-002",  # Change model if needed
        messages=[
            {"role": "system", "content": "You are an assistant knowledgeable about GitLab."},
            {"role": "user", "content": query}
        ],
        max_tokens=500  # Adjust as needed
    )
    return completion.choices[0].message['content']

# Example usage
relevant_context = "Information about GitLab's remote work policy."
print(generate_response("What is GitLab's remote work policy?", relevant_context))
