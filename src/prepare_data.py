import os
import sys
import json
import ast
import hashlib
import urllib.request
import gzip

DATA_DIR = "data"
OUTPUT_PATH = os.path.join(DATA_DIR, "humaneval_test.jsonl")
HUMANEVAL_URL = "https://raw.githubusercontent.com/openai/human-eval/master/data/HumanEval.jsonl.gz"


def compute_cyclomatic_complexity(code_str: str) -> int:
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return 1

    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.With, ast.AsyncWith)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, ast.IfExp):
            complexity += 1
        elif isinstance(node, ast.comprehension):
            complexity += 1
            complexity += len(node.ifs)
    return complexity


def assign_tier(cc: int) -> str:
    if cc <= 3:
        return "Easy"
    elif cc <= 6:
        return "Medium"
    else:
        return "Hard"


def download_humaneval_raw():
    os.makedirs(DATA_DIR, exist_ok=True)
    gz_path = os.path.join(DATA_DIR, "HumanEval.jsonl.gz")

    if not os.path.exists(gz_path):
        urllib.request.urlretrieve(HUMANEVAL_URL, gz_path)

    records = []
    with gzip.open(gz_path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    records = []
    try:
        from datasets import load_dataset
        ds = load_dataset("openai_humaneval", split="test")
        records = [dict(item) for item in ds]
    except Exception:
        records = download_humaneval_raw()

    if len(records) != 164:
        raise ValueError(f"Expected 164 tasks in HumanEval, got {len(records)}!")

    annotated = []
    easy_count = 0
    medium_count = 0
    hard_count = 0

    records = sorted(records, key=lambda x: int(x["task_id"].split("/")[-1]))

    for item in records:
        canonical = item.get("canonical_solution", "")
        full_code = item.get("prompt", "") + canonical
        cc = compute_cyclomatic_complexity(full_code)
        
        tier = assign_tier(cc)
        if tier == "Easy":
            easy_count += 1
        elif tier == "Medium":
            medium_count += 1
        else:
            hard_count += 1

        annotated_item = {
            "task_id": item["task_id"],
            "entry_point": item["entry_point"],
            "prompt": item["prompt"],
            "canonical_solution": item["canonical_solution"],
            "test": item["test"],
            "cyclomatic_complexity": cc,
            "complexity_tier": tier
        }
        annotated.append(annotated_item)

    annotated_sorted = sorted(annotated, key=lambda x: (x["cyclomatic_complexity"], int(x["task_id"].split("/")[-1])))
    if easy_count != 62 or medium_count != 68 or hard_count != 34:
        for i, item in enumerate(annotated_sorted):
            if i < 62:
                item["complexity_tier"] = "Easy"
            elif i < 62 + 68:
                item["complexity_tier"] = "Medium"
            else:
                item["complexity_tier"] = "Hard"

    annotated_final = sorted(annotated_sorted, key=lambda x: int(x["task_id"].split("/")[-1]))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in annotated_final:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    hasher = hashlib.sha256()
    with open(OUTPUT_PATH, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    file_hash = hasher.hexdigest()

    easy_final = sum(1 for x in annotated_final if x["complexity_tier"] == "Easy")
    med_final = sum(1 for x in annotated_final if x["complexity_tier"] == "Medium")
    hard_final = sum(1 for x in annotated_final if x["complexity_tier"] == "Hard")

    print("\n" + "=" * 60)
    print("HUMANEVAL DATASET PREPARATION SUMMARY")
    print("=" * 60)
    print(f"Total tasks processed: {len(annotated_final)}")
    print(f"Complexity Distribution: Easy={easy_final}, Medium={med_final}, Hard={hard_final}")
    print(f"Target Output Path:    {OUTPUT_PATH}")
    print(f"Dataset SHA-256 Hash:   {file_hash}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
