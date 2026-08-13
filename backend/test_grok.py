import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Key chahe GROQ_API_KEY ho ya XAI_API_KEY
api_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY")

print("----------------------------------------")
if api_key:
    print(f"🔑 API Key Found: {api_key[:8]}...****")
else:
    print("❌ ERROR: API Key nahi mili!")
    exit()

print("🛰️ Groq API connect kar rahe hain...")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"  # Groq ka URL
)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Groq ka powerful free model
        messages=[{"role": "user", "content": "Hi, reply with 'Groq is working!'"}]
    )
    print("✅ SUCCESS! Aapki Groq API key bilkul sahi kaam kar rahi hai.")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("\n❌ API CALL FAILED! Error Details:")
    print(e)
print("----------------------------------------")