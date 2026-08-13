# algorithms.py — Hand-rolled algorithms engine

def insertion_sort(records: list, key: str):
    """Sorts a list of dicts in place by record[key]. Mutates list directly."""
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1
        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = current
    return None

def binary_search(sorted_records: list, target_value, key: str) -> int:
    """Standard low/high/mid binary search. Returns index or -1 if not found."""
    low = 0
    high = len(sorted_records) - 1
    
    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_records[mid][key]
        
        if mid_val == target_value:
            return mid
        elif mid_val < target_value:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1

def linear_search(records: list, target_value, key: str) -> int:
    """Baseline linear search. Returns index of first match or -1."""
    for idx, record in enumerate(records):
        if record[key] == target_value:
            return idx
    return -1


# =========================================================
# COMPARISON-COUNTING BENCHMARK WRAPPERS
# =========================================================

def insertion_sort_count(records: list, key: str) -> int:
    """Sorts records in place and returns total comparison count."""
    comparisons = 0
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if records[j][key] > current[key]:
                records[j + 1] = records[j]
                j -= 1
            else:
                break
        records[j + 1] = current
    return comparisons

def binary_search_count(sorted_records: list, target_value, key: str) -> dict:
    """Returns {"index": int, "comparison_count": int}."""
    comparisons = 0
    low = 0
    high = len(sorted_records) - 1
    found_idx = -1

    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_records[mid][key]
        comparisons += 1
        
        if mid_val == target_value:
            found_idx = mid
            break
        elif mid_val < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {"index": found_idx, "comparison_count": comparisons}

def linear_search_count(records: list, target_value, key: str) -> dict:
    """Returns {"index": int, "comparison_count": int}."""
    comparisons = 0
    found_idx = -1
    
    for idx, record in enumerate(records):
        comparisons += 1
        if record[key] == target_value:
            found_idx = idx
            break

    return {"index": found_idx, "comparison_count": comparisons}