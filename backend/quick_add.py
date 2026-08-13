import re
import os
import json
from typing import Tuple, Optional, Dict, Any

# Step 1: Terminal me 'pip install openai' zaroor run karein
from openai import OpenAI

def mock_parse_task(description: str) -> Tuple[str, str, Optional[str]]:
    """
    Deterministic rule-based mock parser (Fallback ke liye)
    """
    orig_text = description
    lower_text = description.lower()

    high_keywords = ["urgent", "asap"]
    low_keywords = ["whenever", "low priority"]
    
    has_high = any(k in lower_text for k in high_keywords)
    has_low = any(k in lower_text for k in low_keywords)

    if has_high:
        priority = "high"
    elif has_low:
        priority = "low"
    else:
        priority = "medium"

    priority_strip_keywords = high_keywords + low_keywords

    date_keywords = [
        "today", "tomorrow", "next week",
        "next monday", "next tuesday", "next wednesday", "next thursday", 
        "next friday", "next saturday", "next sunday",
        "monday", "tuesday", "wednesday", "thursday", 
        "friday", "saturday", "sunday"
    ]

    due_date_hint: Optional[str] = None
    matched_date_phrase: Optional[str] = None

    for phrase in date_keywords:
        if phrase in lower_text:
            due_date_hint = phrase
            matched_date_phrase = phrase
            break

    spans_to_remove = []

    for kw in priority_strip_keywords:
        for match in re.finditer(re.escape(kw), orig_text, flags=re.IGNORECASE):
            spans_to_remove.append(match.span())

    if matched_date_phrase:
        for match in re.finditer(re.escape(matched_date_phrase), orig_text, flags=re.IGNORECASE):
            spans_to_remove.append(match.span())

    spans_to_remove.sort(key=lambda x: x[0])

    title_chars = []
    last_idx = 0
    for start, end in spans_to_remove:
        if start > last_idx:
            title_chars.append(orig_text[last_idx:start])
        last_idx = max(last_idx, end)
    if last_idx < len(orig_text):
        title_chars.append(orig_text[last_idx:])

    title = "".join(title_chars).strip()

    if not title:
        title = "Untitled task"

    return title, priority, due_date_hint


def build_llm_prompt(description: str) -> list[Dict[str, str]]:
    system_prompt = (
        "You are an AI assistant that extracts task attributes from free-text user input.\n"
        "Respond ONLY with a valid JSON object matching this schema:\n"
        "{\n"
        '  "title": string,\n'
        '  "priority": "low" | "medium" | "high",\n'
        '  "due_date_hint": string | null\n'
        "}\n"
        "1. title: The task summary with priority and date keywords removed. Never empty (use 'Untitled task').\n"
        "2. priority: Must be one of 'low', 'medium', 'high'. Default is 'medium'. 'urgent'/'asap' means 'high'.\n"
        "3. due_date_hint: Extracted raw date phrase (e.g., 'today', 'tomorrow', 'next friday') or null."
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": description}
    ]


def parse_quick_add_description(description: str) -> Tuple[str, str, Optional[str]]:
    """
    Parse task using Groq API
    """
    use_real_llm = os.getenv("USE_REAL_LLM", "false").lower() == "true"
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY")

    if use_real_llm and api_key:
        try:
            # Groq API endpoint
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            messages = build_llm_prompt(description)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)
            
            title = result.get("title") or "Untitled task"
            priority = result.get("priority") or "medium"
            due_date_hint = result.get("due_date_hint")

            return title, priority, due_date_hint

        except Exception as e:
            print(f"Groq API Call Failed, falling back to mock: {e}")
            return mock_parse_task(description)
    
    return mock_parse_task(description)