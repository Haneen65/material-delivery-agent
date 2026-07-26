                              


Main Readme


Company :
Ironbridge Construction B


the problem :
Material Delivery Coordination
Construction sites frequently request building materials with different priorities. The company must decide whether to deliver immediately, delay  the request, or escalate it based on inventory availability, request priority, and vehicle availability


why it genuinely needs an agent rather than a simple script?
A simple script can only follow fixed rules. An agent can evaluate the current situation, reason about the request, and make decisions using different architectures such as Reactive, Routing, and ReAct agents.



Comparison

| Architecture                    | LLM Calls per Request                  | Approximate Cost | Latency  | Limitation / What Broke on Tricky Input                                                                                                                  |
| ------------------------------- | -------------------------------------- | ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Reactive Agent**              | 0                                      | None             | Very Low | Cannot handle unexpected or complex situations. Only follows predefined rules.                                                                           |
| **Unconstrained ReAct Agent**   | 1+ (may make multiple reasoning steps) | High             | High     | May generate inconsistent actions or unexpected outputs because it has no strict constraints.                                                            |
| **Deterministic Routing Agent** | 1                                      | Medium           | Medium   | Limited to predefined routing categories (DELIVER, QUEUE, ESCALATE). Cannot adapt beyond those categories.                                               |
| **Constrained ReAct Agent**     | 1                                      | Medium           | Medium   | More reliable due to schema validation, tool allow-list, and reasoning limits, but less flexible when facing situations outside its defined constraints. |


