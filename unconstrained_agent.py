import os
import sys
from dotenv import load_dotenv
from google import genai

from agent import GeminiReActAgent
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
agent = GeminiReActAgent(
    client,
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test_cases import requests

for i, request in enumerate(requests,1):

    print("\n================")
    print("Request", i)
    print(request)
    result = agent.solve(request)
    
    print("\nFinal Result:")
    print(result)