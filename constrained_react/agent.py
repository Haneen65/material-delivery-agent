import json
import re
import time
from google.genai.errors import ClientError

from schema import validate_schema
from tools import (
    ALLOWED_ACTIONS,
    VALID_TOOLS,
    check_inventory,
    check_vehicle,
    dispatch_material,
    schedule_delivery,
)

MAX_STEPS = 5


class ConstrainedReActAgent:

    def __init__(self, client):
        self.client = client
        self.request = None

    def run_tool(self, action_str: str):
        match = re.search(r"^\s*([a-zA-Z0-9_]+)", action_str)
        if not match:
            return {"error": "Invalid action format."}

        tool_name = match.group(1).strip()

        if tool_name not in VALID_TOOLS:
            return {"error": f"Tool '{tool_name}' is not allowed."}

        try:
            if tool_name == "check_inventory":
                qty = self.request.get("quantity", 0)
                inv = self.request.get("inventory", 0)
                return check_inventory(qty, inv)

            elif tool_name == "check_vehicle":
                veh = self.request.get("vehicle", False)
                return check_vehicle(veh)

            elif tool_name == "dispatch_material":
                return dispatch_material()

            elif tool_name == "schedule_delivery":
                return schedule_delivery()

        except Exception as e:
            return {"error": f"Execution error in '{tool_name}': {str(e)}"}

        return {"error": "Unknown tool action"}

    def solve(self, request):
        self.request = request

        allowed_actions_formatted = ", ".join(f'"{a}"' for a in ALLOWED_ACTIONS)

        prompt = f"""
You are a Constrained ReAct Agent for a construction company.

Your task is to decide how to handle a material delivery request based on strict constraints.

You MUST follow these rules strictly:

1. Use ONLY these valid tools:
   - check_inventory()
   - check_vehicle()
   - dispatch_material()
   - schedule_delivery()

2. Never invent a new tool.

3. Always check inventory and vehicle availability before making decisions.

4. Allowed status values in FINAL answer MUST be one of:
   - APPROVED
   - PENDING
   - REJECTED
   - SCHEDULED
   - ESCALATE

5. Allowed action values in FINAL answer MUST be one of:
   [{allowed_actions_formatted}]

6. Wait for the Observation after every Action before making another decision.

7. Stop after at most {MAX_STEPS} reasoning steps.

Request details:
- Material: {request.get("material")}
- Quantity: {request.get("quantity")}
- Priority: {request.get("priority")}

Use this format exactly:

Thought: ...
Action: tool_name(...)
Observation: ...

When finished, return ONLY the JSON block after 'FINAL:':

FINAL:
{{
    "thought": "...",
    "action": "<must be one of ALLOWED_ACTIONS>",
    "status": "<must be one of VALID_STATUS>"
}}
"""
        conversation = prompt
        max_retries = 5

        for step in range(MAX_STEPS):
            response = None

            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash", contents=conversation
                    )
                    break
                except ClientError as e:
                    if "429" in str(e):
                        wait_time = (attempt + 1) * 10
                        print(
                            f"Rate limit reached. Waiting {wait_time} seconds..."
                        )
                        time.sleep(wait_time)
                    else:
                        raise e

            if response is None:
                return {
                    "thought": "Quota limit reached after maximum retries.",
                    "action": "Review System Logs",
                    "status": "ESCALATE",
                }

            text = response.text.strip()
            print(f"\n[Step {step + 1}] Agent:")
            print(text)

            if "FINAL:" in text:
                raw_json = text.split("FINAL:")[1]
                raw_json = (
                    raw_json.replace("```json", "").replace("```", "").strip()
                )

                try:
                    decision = json.loads(raw_json)

                    if validate_schema(decision):
                        return decision
                    else:
                        error_msg = f"Error: Output failed validation. Ensure required keys exist, status is valid, and action is strictly one of {ALLOWED_ACTIONS}."
                        print(f"\n[Validation Error] {error_msg}")
                        conversation += f"\n\n{text}\n\nObservation: {error_msg}\nContinue."
                        continue

                except json.JSONDecodeError:
                    error_msg = "Error: Invalid JSON format after FINAL:. Return strict JSON format only."
                    print(f"\n[JSON Parse Error] {error_msg}")
                    conversation += f"\n\n{text}\n\nObservation: {error_msg}\nContinue."
                    continue

            action_match = re.search(r"Action:\s*(.*)", text)

            if action_match:
                action_str = action_match.group(1).strip()
                observation = self.run_tool(action_str)
                conversation += (
                    f"\n\n{text}\n\nObservation:\n{observation}\n\nContinue."
                )
            else:
                feedback = "Observation: No valid Action or FINAL output detected. Follow the format: Thought -> Action -> Observation."
                conversation += f"\n\n{text}\n\n{feedback}\nContinue."

        return {
            "thought": "Reached maximum reasoning steps without conclusive decision.",
            "action": "Review System Logs",
            "status": "PENDING",
        }