import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from agent import ConstrainedReActAgent
from google import genai
from test_cases import requests

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

agent = ConstrainedReActAgent(client=client)


def run_pipeline():
    print("=" * 60)
    print("STARTING TEST SUITE FOR CONSTRAINED REACT AGENT")
    print("=" * 60)

    for i, req in enumerate(requests, 1):
        print(f"\n---> Running Test Case [{i}/{len(requests)}]")
        print(
            f"Input: Material={req['material']}, Qty={req['quantity']}, "
            f"Inv={req['inventory']}, Veh={req['vehicle']}, Priority={req['priority']}"
        )

        decision = agent.solve(req)

        print("\nValidated Agent Decision:")
        print(decision)
        print("-" * 60)


if __name__ == "__main__":
    run_pipeline()