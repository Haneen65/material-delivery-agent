import json
import re
import time

from google.genai.errors import ClientError

from tools import (
    check_inventory,
    dispatch_vehicle,
    order_from_supplier,
    inform_manager
)



class GeminiReActAgent:


    def __init__(self, client):

        self.client = client



    def run_tool(self, action):


        if "check_inventory" in action:

            material = re.findall(
                r'"(.*?)"',
                action
            )[0]

            return check_inventory(self.request)

        elif "dispatch_vehicle" in action:

            values = re.findall(
                r'"(.*?)"',
                action
            )

            return dispatch_vehicle(
                values[0],
                values[1]
            )



        elif "order_from_supplier" in action:

            values = re.findall(
                r'"(.*?)"',
                action
            )

            return order_from_supplier(
                values[0],
                values[1]
            )



        elif "inform_manager" in action:

            return inform_manager(
                "Delivery request finished"
            )


        return {
            "error":"Unknown action"
        }



    def solve(self, request):
        self.request = request

        prompt = f"""

You are an Unconstrained ReAct Agent for a construction company.

Your goal is to decide how to handle a material delivery request.

Available tools (use ONLY these tools):

check_inventory("material")

dispatch_vehicle("material","quantity")

order_from_supplier("material","quantity")

inform_manager("message")


Request:

Material: {request["material"]}
Quantity: {request["quantity"]}
Available Inventory: {request["inventory"]}
Priority: {request["priority"]}
Vehicle Available: {request["vehicle"]}


Guidelines:

1. First, always check the inventory before making any decision.

2. Use the inventory returned by the tool to determine availability.

3. If inventory is enough:
   - If a vehicle is available, dispatch the vehicle.
   - If no vehicle is available, do NOT dispatch a vehicle. Inform the manager or wait for vehicle availability.

4. If inventory is not enough:
   - Calculate the missing quantity.
   - Order ONLY the missing quantity from the supplier.

5. Consider the priority:
   - High: handle immediately.
   - Medium: normal handling.
   - Low: delivery can be scheduled if needed.

6. Do not invent tools.
   Use only the available tools listed above.

7. After every Action, wait for the Observation before deciding the next Action.

Use this format exactly:

Thought:
...

Action:
...

Observation:
...

When the task is complete return only:

FINAL:
{{
"action":"",
"status":"APPROVED/PENDING/SCHEDULED/REJECTED"
}}

"""
        conversation = prompt
        max_retries = 5



        # small ReAct loop
        for step in range(3):


            response = None


            for attempt in range(max_retries):

                try:

                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=conversation
                    )

                    break


                except ClientError as e:
                    if "429" in str(e):

                        wait_time = (attempt + 1) * 10

                        print(
                            f"Rate limit reached. Waiting {wait_time}s..."
                        )

                        time.sleep(wait_time)


                    else:

                        raise e

            if response is None:

                return {
                    "status":"FAILED",
                    "action":"Gemini quota exceeded"
                }



            text = response.text.strip()


            print("\nAgent:")
            print(text)



            if "FINAL:" in text:


                result = text.split("FINAL:")[1]


                result = (
                    result
                    .replace("```json","")
                    .replace("```","")
                    .strip()
                )


                try:

                    return json.loads(result)

                except:


                    return {
                        "status":"PENDING",
                        "action":result
                    }



            action = re.search(
                r"Action:\s*(.*)",
                text
            )



            if action:


                observation = self.run_tool(
                    action.group(1)
                )


                conversation += f"""

{text}


Observation:

{observation}


Continue.
"""



        return {
            "status":"PENDING",
            "action":"Agent stopped"
        }