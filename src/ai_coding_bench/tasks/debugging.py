"""Debugging task — measures ability to locate and fix code errors."""

from .base import BaseTask

DEBUG_CASES = [
    {
        "code": (
            "def binary_search(arr, target):\n"
            "    left, right = 0, len(arr)\n"
            "    while left < right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            left = mid\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n"
        ),
        "fix": ["infinite loop", "left = mid + 1", "right = mid"],
    },
    {
        "code": (
            "class Singleton:\n"
            "    _instance = None\n"
            "    def __new__(cls, *args, **kwargs):\n"
            "        if not cls._instance:\n"
            "            cls._instance = super().__new__(cls)\n"
            "        return cls._instance\n"
        ),
        "fix": ["thread", "lock", "race condition", "not thread-safe"],
    },
    {
        "code": (
            "def memoize(fn):\n"
            "    cache = {}\n"
            "    def wrapper(*args):\n"
            "        if args in cache:\n"
            "            return cache[args]\n"
            "        result = fn(*args)\n"
            "        cache[args] = result\n"
            "        return result\n"
            "    return wrapper\n"
        ),
        "fix": ["unhashable", "mutable", "isinstance", "hash"],
    },
]


class DebuggingTask(BaseTask):
    name = "Debugging"

    async def evaluate(self, model) -> float:
        passed = 0
        for case in DEBUG_CASES:
            prompt = (
                "Find and explain the bugs in this code. "
                "Describe how to fix each one:\n\n" + case["code"]
            )
            output = await model.generate(prompt, max_tokens=1024)
            if any(fix in output.lower() for fix in case["fix"]):
                passed += 1
        return (passed / len(DEBUG_CASES)) * 100
