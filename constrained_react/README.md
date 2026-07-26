# Constrained ReAct Delivery Agent

An intelligent, rule-governed ReAct (Reasoning and Acting) agent built with Python and the Google Gemini API. The agent processes material delivery requests for a construction company while enforcing strict operational constraints, schema validation, and tool-access boundaries.

---

## Features

* **Strict Action Rules:** Enforces adherence to allowed operational tools (`check_inventory`, `check_vehicle`, `dispatch_material`, `schedule_delivery`).
* **Schema Validation:** Validates all final decisions against JSON schemas ensuring required keys (`thought`, `action`, `status`) and status limits (`APPROVED`, `PENDING`, `REJECTED`, `SCHEDULED`, `ESCALATE`).
* **Self-Correction Mechanism:** Feeds validation errors back to the model during execution to prompt self-correction without hard-crashing.
* **Rate-Limit Resilience:** Handles Gemini API quota limits (`429 Rate Limits`) with exponential backoff retries.

---

## Repository Structure

```text
material-delivery-agent/
│
├── constrained_react/
│   ├── agent.py          # ConstrainedReActAgent implementation
│   ├── tools.py          # Available tools & allowed actions definition
│   ├── schema.py         # Decision validation & schema rules
│   └── main.py           # Test execution script
│
├── test_cases.py         # Pre-defined request datasets
└── README.md             # Project documentation
