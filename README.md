# Unconstrained ReAct Agent

# Overview

This project implements an Unconstrained ReAct agent for a construction company.
The agent helps decide how to handle material delivery requests.
It can check inventory, dispatch vehicles, create supplier orders, and notify managers.

# Architecture
The model follows a ReAct style loop:
Thought → Action → Observation → Final Answer
The LLM decides which tool to use and when the task is completed.

This version does not use:
. fixed output schemas
. tool restrictions
. maximum step limits

# Model
Google Gemini 2.0 Flash

# Running
Install dependencies:
pip install -r requirements.txt
Create a '.env' file:
GEMINI_API_KEY=your_key
Run:
python main.py