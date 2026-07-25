import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

print("My Key is:", repr(api_key))

client = genai.Client(api_key=api_key)


class GeminiReActAgent:

    def __init__(self, inventory_db):
        self.inventory = inventory_db

    def think_and_act(self, request):
        material = request.get("material")
        quantity = request.get("quantity", 0)
        current_inv = self.inventory.get(material, 0)

        prompt = f"""
You are an Unconstrained ReAct Agent responsible for coordinating material deliveries
for a construction company.

Current Request:
- Material Requested: {material}
- Quantity Requested: {quantity}
- Current Inventory Available: {current_inv}
- Request Priority: {request.get("priority", "Low")}
- Vehicle Available: {request.get("vehicle", False)}

Analyze the request freely.

You may reason in any way you think is appropriate and decide on the best action based
on the available information.

At the end, summarize your decision in the following JSON format:

{{
    "thought": "Explain your reasoning",
    "action": "Recommended action",
    "status": "APPROVED | PENDING | REJECTED | SCHEDULED"
}}
"""

        max_retries = 5
        response = None

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                )
                break

            except ClientError as e:
                if "429" in str(e):
                    wait_time = (attempt + 1) * 10
                    print(
                        f"Rate limit hit. Waiting {wait_time}s before retrying "
                        f"(Attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(wait_time)
                else:
                    raise e

        if not response:
            return {"error": "Failed to get response after multiple retries"}

        try:
            cleaned_text = (
                response.text.strip()
                .replace("```json", "")
                .replace("```", "")
            )

            decision = json.loads(cleaned_text)

        except Exception:
            decision = {
                "thought": response.text,
                "action": "Review System Logs",
                "status": "PENDING",
            }

        if (
            decision.get("status") == "APPROVED"
            and current_inv >= quantity
        ):
            self.inventory[material] -= quantity

        decision["remaining_inventory"] = self.inventory.get(
            material,
            current_inv,
        )

        time.sleep(3)

        return decision


if __name__ == "__main__":

    initial_inventory = {
        "cement": 100,
        "steel": 50,
        "bricks": 5000,
    }

    agent = GeminiReActAgent(
        inventory_db=initial_inventory
    )

    requests_list = [
        {
            "material": "cement",
            "quantity": 70,
            "priority": "High",
            "vehicle": True,
        },
        {
            "material": "steel",
            "quantity": 120,
            "priority": "High",
            "vehicle": True,
        },
        {
            "material": "bricks",
            "quantity": 3000,
            "priority": "Low",
            "vehicle": False,
        },
    ]

    print("\nProcessing Unconstrained ReAct Agent Decisions\n")

    for idx, req in enumerate(requests_list, 1):

        print(f"Request {idx}: {req}")

        result = agent.think_and_act(req)

        print(f"Thought : {result.get('thought')}")
        print(f"Action  : {result.get('action')}")
        print(f"Status  : {result.get('status')}")
        print(f"Remaining Inventory: {result.get('remaining_inventory')}")

        print("=" * 60)