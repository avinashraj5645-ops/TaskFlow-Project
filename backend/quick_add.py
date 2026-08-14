import re
from typing import Tuple, Optional

def parse_quick_add_description(description: str) -> Tuple[str, str, Optional[str]]:
    if not description or not description.strip():
        return "Untitled task", "medium", None

    orig_text = description.strip()
    lower_text = orig_text.lower()

    # Priority Keywords
    high_keywords = ["urgent", "asap", "high priority", "p1"]
    low_keywords = ["whenever", "low priority", "p3"]

    has_high = any(re.search(r'\b' + re.escape(k) + r'\b', lower_text) for k in high_keywords)
    has_low = any(re.search(r'\b' + re.escape(k) + r'\b', lower_text) for k in low_keywords)

    if has_high:
        priority = "high"
    elif has_low:
        priority = "low"
    else:
        priority = "medium"

    # Date Keywords (Longer phrases first)
    date_keywords = [
        "next monday", "next tuesday", "next wednesday", "next thursday", 
        "next friday", "next saturday", "next sunday", "next week",
        "monday", "tuesday", "wednesday", "thursday", 
        "friday", "saturday", "sunday", "today", "tomorrow"
    ]

    due_date_hint: Optional[str] = None
    for phrase in date_keywords:
        if re.search(r'\b' + re.escape(phrase) + r'\b', lower_text):
            due_date_hint = phrase
            break

    # All phrases to strip (Sorted by length DESC to prevent partial substring overlaps)
    all_strip_keywords = sorted(high_keywords + low_keywords + date_keywords, key=len, reverse=True)

    spans_to_remove = []
    for kw in all_strip_keywords:
        for match in re.finditer(r'\b' + re.escape(kw) + r'\b', orig_text, flags=re.IGNORECASE):
            spans_to_remove.append(match.span())

    # Sort & Merge overlapping spans
    spans_to_remove.sort(key=lambda x: x[0])

    merged_spans = []
    for start, end in spans_to_remove:
        if not merged_spans:
            merged_spans.append((start, end))
        else:
            prev_start, prev_end = merged_spans[-1]
            if start <= prev_end:
                merged_spans[-1] = (prev_start, max(prev_end, end))
            else:
                merged_spans.append((start, end))

    # Slice text outside removed spans
    title_chars = []
    last_idx = 0
    for start, end in merged_spans:
        if start > last_idx:
            title_chars.append(orig_text[last_idx:start])
        last_idx = max(last_idx, end)
    if last_idx < len(orig_text):
        title_chars.append(orig_text[last_idx:])

    title = "".join(title_chars)

    # Clean-up formatting, double spaces, and orphan commas
    title = re.sub(r'\s+,', ',', title)           # Remove space before comma (' ,' -> ',')
    title = re.sub(r',\s*,', ',', title)           # Remove duplicate commas (',,')
    title = re.sub(r'\s+', ' ', title)            # Normalize spaces
    title = re.sub(r'^[,\s\.-]+|[,\s\.-]+$', '', title).strip() # Remove leading/trailing commas, dots, dashes

    if not title:
        title = "Untitled task"

    return title, priority, due_date_hint