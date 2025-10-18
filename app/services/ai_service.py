
import json
import requests
import os
from fastapi.encoders import jsonable_encoder
from typing import List
from ..schemas import ai_schema

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-70b-8192"


def get_subtasks(task_title):
    prompt = f"""
    You are a project planning assistant.
    A user will provide a high-level task. Break it down into actionable subtasks.
    
    Rules:
    1. Each subtask must have:
    - "priority" : rank based on priority
    - "title": short clear subtask name
    - "description": brief guidance or ideas to complete it
    - "created_at": ISO 8601 timestamp in UTC (e.g., "2025-08-10T14:30:00Z")
    2. Return ONLY a valid JSON array of objects — no markdown, no extra text, no explanations.
    3. Exactly five keys per object: "title", "description", "priority", "created_at".
    4. Do not include numbering in the titles.
    5. The JSON must be parseable without modification.
    
    User task: {task_title}
"""
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )
    content = resp.json()["choices"][0]["message"]["content"].strip()
    return json.loads(content)


def get_priority_tasks(task_list: list) -> list[dict]:
    tasks_payload = jsonable_encoder(task_list)  # handles datetime -> ISO
    tasks_json = json.dumps(tasks_payload, ensure_ascii=False)

    # 2) Prompt
    prompt = f"""
    You are a scheduling assistant. Re-prioritize the given tasks.
    Rules:
    - Return ONLY valid JSON as an array of objects.
    - Keep the SAME objects (no additions/deletions).
    - Keep the SAME values for all fields EXCEPT "priority".
    - Go through all the task ad decide the field "priority" and change the numbers.
    - Dont return the field "priority" with same values
    - The ONLY field you may change is "priority".
    - Set "priority" as integers starting at 1 (1 = highest), no ties, no gaps.
    - Preserve original text exactly (no rewording).
    - Output must be parseable JSON with no extra text.
    Tasks:
{tasks_json}
"""

    # 3) Call Groq
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0
        },
        timeout=60
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"].strip()
    updated = json.loads(content)  # list[dict] from the model

    # 4) Merge: only update 'priority' onto original items by stable key (title here)
    originals_by_title = {t["title"]: t for t in tasks_payload}
    result = []
    for item in updated:
        title = item.get("title")
        if title in originals_by_title and "priority" in item:
            originals_by_title[title]["priority"] = int(item["priority"])
            result.append(originals_by_title[title])

    # Fallback: if model messed up, return originals
    if len(result) != len(tasks_payload):
        return tasks_payload
    return result
