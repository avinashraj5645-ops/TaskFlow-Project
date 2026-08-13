# benchmark.py — Performance benchmarking across data sizes
import random
from algorithms import (
    insertion_sort,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)

def generate_synthetic_tasks(size: int):
    priorities = ["low", "medium", "high"]
    tasks = []
    for i in range(size):
        tasks.append({
            "id": f"task-{i}",
            "title": f"Task Title {i:04d}",
            "priority": random.choice(priorities),
            "due_date": "2026-08-20"
        })
    return tasks

def run_benchmark():
    sizes = [10, 500, 3000]
    print("=" * 65)
    print(f"{'Size':<10} | {'Algo':<22} | {'Comparisons':<15} | {'Target'}")
    print("=" * 65)

    for size in sizes:
        tasks = generate_synthetic_tasks(size)
        random.shuffle(tasks)
        
        # 1. Insertion Sort Count
        tasks_copy = [t.copy() for t in tasks]
        sort_comps = insertion_sort_count(tasks_copy, "title")
        print(f"{size:<10} | {'Insertion Sort':<22} | {sort_comps:<15} | N/A")

        # Prepare sorted copy for Binary Search
        sorted_tasks = [t.copy() for t in tasks]
        insertion_sort(sorted_tasks, "title")

        # 2. Linear Search Count (Existing Target)
        target_title = f"Task Title {size // 2:04d}"
        ls_res = linear_search_count(tasks, target_title, "title")
        print(f"{size:<10} | {'Linear Search (Found)':<22} | {ls_res['comparison_count']:<15} | Mid Item")

        # 3. Binary Search Count (Existing Target)
        bs_res = binary_search_count(sorted_tasks, target_title, "title")
        print(f"{size:<10} | {'Binary Search (Found)':<22} | {bs_res['comparison_count']:<15} | Mid Item")

        # 4. Linear Search Count (Absent Target)
        ls_absent = linear_search_count(tasks, "Task Title ABSENT", "title")
        print(f"{size:<10} | {'Linear Search (Absent)':<22} | {ls_absent['comparison_count']:<15} | Absent")

        # 5. Binary Search Count (Absent Target)
        bs_absent = binary_search_count(sorted_tasks, "Task Title ABSENT", "title")
        print(f"{size:<10} | {'Binary Search (Absent)':<22} | {bs_absent['comparison_count']:<15} | Absent")
        print("-" * 65)

if __name__ == "__main__":
    run_benchmark()