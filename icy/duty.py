import json
import time
import functools
import sys
import tracemalloc
from typing import Any, Callable, List, Dict

# ------------------------------------------------------------
# ฟังก์ชันจัดการ JSON
def save_to_json(data: Any, filename: str):
    """บันทึกข้อมูลลงไฟล์ JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_from_json(filename: str) -> Any:
    """อ่านข้อมูลจากไฟล์ JSON"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# ------------------------------------------------------------
# guests = [
#     {"channel_id": 1, "seq_in_channel": 1, "room_number": 1},
#     {"channel_id": 1, "seq_in_channel": 2, "room_number": 2},
#     {"channel_id": 2, "seq_in_channel": 1, "room_number": 3},
# ]

# json_filename = "roomData.json"

# save_to_json(guests, json_filename)
# loaded_guests = load_from_json(json_filename)

# print("---- ข้อมูลจาก JSON ----")
# for g in loaded_guests:
#     print(g)

# ------------------------------------------------------------
# time, memory
# timing_records: List[Dict[str, Any]] = []

# def timed(func: Callable = None, *, record_args: bool = True):
#     if func is None:
#         return lambda f: timed(f, record_args=record_args)

#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         tracemalloc_started = tracemalloc.is_tracing()
#         if not tracemalloc_started:
#             tracemalloc.start()

#         wall_start = time.perf_counter()
#         cpu_start = time.process_time()
#         try:
#             result = func(*args, **kwargs)
#             return result
#         finally:
#             wall_end = time.perf_counter()
#             cpu_end = time.process_time()
#             current, peak = tracemalloc.get_traced_memory()
#             if not tracemalloc_started:
#                 tracemalloc.stop()

#             rec = {
#                 "function": func.__name__,
#                 "wall_seconds": wall_end - wall_start,
#                 "mem_current_bytes": current,
#             }
#             timing_records.append(rec)
#     return wrapper

# def deep_getsizeof(obj: Any, ids: set = None) -> int:
#     if ids is None:
#         ids = set()
#     obj_id = id(obj)
#     if obj_id in ids:
#         return 0
#     ids.add(obj_id)
#     size = sys.getsizeof(obj)
#     if isinstance(obj, dict):
#         for k, v in obj.items():
#             size += deep_getsizeof(k, ids)
#             size += deep_getsizeof(v, ids)
#     elif isinstance(obj, (list, tuple, set, frozenset)):
#         for item in obj:
#             size += deep_getsizeof(item, ids)
#     return size

# ------------------------------------------------------------
#  test time and memory
# @timed
# def make_numbers(n: int) -> List[int]:
#     return list(range(n))

# @timed
# def sum_numbers(lst: List[int]) -> int:
#     return sum(lst)

# ------------------------------------------------------------
# if __name__ == "__main__":
#     nums = make_numbers(1_000_000)
#     total = sum_numbers(nums)

#     print("Total:", total)
#     print("\nTiming records:")
#     for rec in timing_records:
#         print(rec)

#     print("\nApprox memory usage of nums:", deep_getsizeof(nums), "bytes")
