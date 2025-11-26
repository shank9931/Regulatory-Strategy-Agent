import json
import os
from typing import List, Dict, Any, Optional

# 1. Get the directory where tools.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Join it with the filename
JSON_PATH = os.path.join(BASE_DIR, "guidelines.json")

# 3. Open using the absolute path
try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        GUIDELINES: List[Dict[str, Any]] = json.load(f)
except FileNotFoundError:
    print(f"ERROR: Could not find guidelines.json at {JSON_PATH}")
    # Fallback to empty list so the agent doesn't crash immediately on load
    GUIDELINES = []


def search_guidelines(
    product_description: str,
    Markets: Optional[str] = None,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Simple keyword-based search over the guidelines DB.
    """
    text = product_description.lower()
    scored = []

    for g in GUIDELINES:
        score = 0

        # keyword hits
        for kw in g.get("Keywords", []):
            if kw.lower() in text:
                score += 2  # keyword hit
        # product type hints
        for t in g.get("Product Types", []):
            if t.lower() in text:
                score += 1

        # Markets filter (mild)
        if Markets:
            if g.get("Markets") == Markets or str(g.get("Markets")).lower() == "global":
                score += 0.5
            else:
                score -= 0.5

        if score > 0:
            scored.append((score, g))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [g for score, g in scored[:max_results]]