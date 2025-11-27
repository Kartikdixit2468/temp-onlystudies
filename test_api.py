import os
from dotenv import load_dotenv
import google.generativeai as genai
from backend import Director

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

genai.configure(api_key=api_key)

try:
    print("Testing simple generation...")
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Say hello")
    print(f"Simple response: {response.text}")
except Exception as e:
    print(f"Simple generation failed: {e}")

print("\nTesting Director.plan_video...")
try:
    plan = Director.plan_video("Gravity")
    print(f"Plan result: {plan}")
except Exception as e:
    print(f"Director failed: {e}")
