# check_algorithms.py — Automated verification script
from algorithms import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)

def run_checks():
    # Case 1: insertion_sort on empty list
    empty_list = []
    insertion_sort(empty_list, "key")
    case_name = "insertion_sort on empty list leaves it empty and completes without error"
    if empty_list == []:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected [], got {empty_list}")

    # Case 2: insertion_sort on single-element list
    single_list = [{"title": "Task 1"}]
    insertion_sort(single_list, "title")
    case_name = "insertion_sort on single-element list leaves that element unchanged"
    if single_list == [{"title": "Task 1"}]:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected single element unchanged, got {single_list}")

    # Case 3: binary_search finds value at first, last, and middle index
    sorted_list = [
        {"title": "A"},
        {"title": "B"},
        {"title": "C"},
        {"title": "D"},
        {"title": "E"},
    ]
    idx_first = binary_search(sorted_list, "A", "title")
    idx_mid = binary_search(sorted_list, "C", "title")
    idx_last = binary_search(sorted_list, "E", "title")
    
    case_name = "binary_search correctly finds value at first, last, and middle index"
    if idx_first == 0 and idx_mid == 2 and idx_last == 4:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected (0, 2, 4), got ({idx_first}, {idx_mid}, {idx_last})")

    # Case 4: binary_search returns -1 when target is absent
    case_name = "binary_search correctly returns not-found result (-1) when target is absent"
    idx_absent = binary_search(sorted_list, "Z", "title")
    if idx_absent == -1:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected -1, got {idx_absent}")

    # Case 5: insertion_sort_count on small list
    small_list = [{"val": 3}, {"val": 1}, {"val": 2}]
    count = insertion_sort_count(small_list, "val")
    case_name = "insertion_sort_count leaves list sorted and returns plain int > 0"
    is_sorted = small_list == [{"val": 1}, {"val": 2}, {"val": 3}]
    if is_sorted and type(count) == int and count > 0:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected sorted list and int > 0, got sorted={is_sorted}, count={count}")

    # Case 6: binary_search_count on sorted list
    bs_res = binary_search_count(sorted_list, "C", "title")
    case_name = "binary_search_count returns expected index and comparison_count int > 0"
    if bs_res.get("index") == 2 and type(bs_res.get("comparison_count")) == int and bs_res.get("comparison_count") > 0:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected index=2, count > 0, got {bs_res}")

    # Case 7: linear_search_count for absent value
    ls_res = linear_search_count(sorted_list, "Z", "title")
    case_name = "linear_search_count for absent value returns index=-1 and comparison_count == len(list)"
    if ls_res.get("index") == -1 and ls_res.get("comparison_count") == len(sorted_list):
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected index=-1, count={len(sorted_list)}, got {ls_res}")

if __name__ == "__main__":
    run_checks()