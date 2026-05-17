"""Code review task — measures ability to spot bugs and suggest improvements."""

from .base import BaseTask

REVIEW_CASES = [
    {
        "code": (
            "def process_orders(orders):\n"
            "    results = []\n"
            "    for o in orders:\n"
            "        total = o.price * o.qty\n"
            "        results.append(total)\n"
            "    return sum(results) / len(results)\n"
        ),
        "bugs": ["ZeroDivisionError", "division by zero", "empty list"],
    },
    {
        "code": (
            "@app.route('/user/<int:user_id>')\n"
            "def get_user(user_id):\n"
            "    query = f'SELECT * FROM users WHERE id = {user_id}'\n"
            "    return db.execute(query).fetchone()\n"
        ),
        "bugs": ["sql injection", "parameterized", "prepared statement"],
    },
    {
        "code": (
            "async def fetch_all(urls):\n"
            "    tasks = []\n"
            "    for url in urls:\n"
            "        data = await fetch(url)\n"
            "        tasks.append(data)\n"
            "    return tasks\n"
        ),
        "bugs": ["concurrent", "asyncio.gather", "sequential", "not parallel"],
    },
]


class CodeReviewTask(BaseTask):
    name = "Code Review"

    async def evaluate(self, model) -> float:
        passed = 0
        for case in REVIEW_CASES:
            prompt = (
                "Review the following code for bugs and security issues. "
                "List all problems found:\n\n" + case["code"]
            )
            output = await model.generate(prompt, max_tokens=1024)
            if any(bug in output.lower() for bug in case["bugs"]):
                passed += 1
        return (passed / len(REVIEW_CASES)) * 100
