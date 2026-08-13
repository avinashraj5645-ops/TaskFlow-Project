from quick_add import mock_parse_task

def run_tests():
    examples = [
        {
            "input": "This is urgent, mark it ASAP please",
            "expected": {"title": "This is , mark it please", "priority": "high", "due_date_hint": None}
        },
        {
            "input": " ",
            "expected": {"title": "Untitled task", "priority": "medium", "due_date_hint": None}
        },
        {
            "input": "Finish the report next Friday, it's urgent",
            "expected": {"title": "Finish the report , it's", "priority": "high", "due_date_hint": "next friday"}
        },
        {
            "input": "tomorrow review tomorrow",
            "expected": {"title": "review", "priority": "medium", "due_date_hint": "tomorrow"}
        },
        {
            "input": "Submit tax files whenever possible on tuesday",
            "expected": {"title": "Submit tax files  possible on", "priority": "low", "due_date_hint": "tuesday"}
        }
    ]

    for idx, ex in enumerate(examples, 1):
        title, priority, due_hint = mock_parse_task(ex["input"])
        actual = {"title": title, "priority": priority, "due_date_hint": due_hint}
        if actual == ex["expected"]:
            print(f"PASS: Worked Example {idx}")
        else:
            print(f"FAIL: Worked Example {idx} — expected {ex['expected']}, got {actual}")

if __name__ == "__main__":
    run_tests()


# for example
# {
#   "title": "review",
#   "priority": "medium",
#   "due_date_hint": "tomorrow"
# }
# {
#   "title": "Finish the report , it's",
#   "priority": "high",
#   "due_date_hint": "next friday"
# }