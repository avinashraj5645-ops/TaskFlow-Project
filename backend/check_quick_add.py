import sys
import os

# Project directory ko path me add karein
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Quick-Add parser function import karein
from quick_add import parse_quick_add_description


def run_tests():
    examples = [
        {
            "input": "This is urgent, mark it ASAP please",
            "expected": {
                "title": "This is, mark it please",
                "priority": "high",
                "due_date_hint": None
            }
        },
        {
            "input": " ",
            "expected": {
                "title": "Untitled task",
                "priority": "medium",
                "due_date_hint": None
            }
        },
        {
            "input": "Finish the report next Friday, it's urgent",
            "expected": {
                "title": "Finish the report, it's",
                "priority": "high",
                "due_date_hint": "next friday"
            }
        },
        {
            "input": "tomorrow review tomorrow",
            "expected": {
                "title": "review",
                "priority": "medium",
                "due_date_hint": "tomorrow"
            }
        },
        {
            "input": "Submit tax files whenever possible on tuesday",
            "expected": {
                "title": "Submit tax files possible on",
                "priority": "low",
                "due_date_hint": "tuesday"
            }
        }
    ]

    print("\n--- RUNNING QUICK-ADD PARSER TESTS ---")
    all_passed = True

    for idx, ex in enumerate(examples, 1):
        title, priority, due_hint = parse_quick_add_description(ex["input"])
        actual = {
            "title": title,
            "priority": priority,
            "due_date_hint": due_hint
        }

        if actual == ex["expected"]:
            print(f"✅ PASS: Example {idx}")
        else:
            all_passed = False
            print(f"❌ FAIL: Example {idx}")
            print(f"   Input    : '{ex['input']}'")
            print(f"   Expected : {ex['expected']}")
            print(f"   Got      : {actual}\n")

    if all_passed:
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()