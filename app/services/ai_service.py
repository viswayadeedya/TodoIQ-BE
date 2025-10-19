import json
import os
from openai import OpenAI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime

# Load environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"


def get_subtasks(task_title: str):
    """
    Generates subtasks for a given high-level task using OpenAI GPT-4o-mini.
    """

    prompt = f"""
    You are MindfulCoach, a calm but decisive planning expert. Internally consider energy, dependencies, and “minimum next steps,” but OUTPUT ONLY JSON.

    GOAL
    Turn the user's high-level task into 6–9 concrete subtasks that a real person can execute today.

    PLANNING HEURISTICS (think silently; do NOT explain in output)
    • Start with a quick setup/clarify step if needed, then sequence from easiest win → hardest focus → admin/wrap-up.
    • Make each subtask independent, small (<60 min), and start with a strong verb.
    • Respect natural flow: plan → prep → do → review. Batch similar actions.
    • Prefer momentum over perfection; avoid duplicate or overlapping steps.

    OUTPUT RULES (must follow exactly)
    1) Return ONLY a JSON array of objects (no markdown, no commentary).
    2) Each object has EXACTLY these keys:
       - "title"        : short, 3–6 words, action-verb first (e.g., “Draft outline V1”)
       - "description"  : one sentence with specifics (what + how)
       - "priority"     : integer rank starting at 1 (1 = highest), no ties, no gaps
       - "created_at"   : ISO 8601 UTC timestamp like "2025-10-19T14:30:00Z"
    3) Create 6–9 items. Keep titles unique. No numbering inside titles.
    4) JSON must be valid and parseable without edits. No trailing commas.

    USER TASK
    {task_title}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        subtasks = json.loads(content)

        # ✅ Optional: ensure all have created_at if model missed it
        for subtask in subtasks:
            if "created_at" not in subtask:
                subtask["created_at"] = datetime.utcnow().isoformat() + "Z"

        return subtasks

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


def get_priority_tasks(task_list: list[dict]) -> list[dict]:
    """
    Re-prioritize a list of tasks based on context using GPT-4o-mini.
    """
    tasks_payload = jsonable_encoder(task_list)
    tasks_json = json.dumps(tasks_payload, ensure_ascii=False)

    prompt = f"""
    You are MindfulCoach, an empathetic but structured scheduling expert.
    Your goal is to re-prioritize the user’s existing tasks so the day flows naturally, balancing energy, focus, and well-being.

    INTERNAL REASONING (do not include in output):
    • Group similar or dependent tasks together.
    • Place high-impact or time-sensitive tasks first.
    • Keep deep-focus work before admin or errands.
    • Schedule recovery or light tasks near the end.
    • Think like a human who wants momentum, not burnout.

    OUTPUT RULES (must follow exactly):
    1) Return ONLY a valid JSON array of objects (no markdown, no commentary).
    2) Use the SAME objects given — do not add, remove, or rename anything.
    3) Keep every field exactly the same EXCEPT "priority".
    4) Reassign "priority" values as integers starting at 1 (1 = highest), with no ties or gaps.
    5) Output must be valid JSON and parseable without modification.

    Tasks to re-prioritize:
    {tasks_json}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()
        updated_tasks = json.loads(content)

        return updated_tasks

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
