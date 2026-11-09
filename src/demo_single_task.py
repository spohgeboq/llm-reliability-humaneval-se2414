import os
import sys
import warnings

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
import argparse
import yaml
from src.evaluate_models import load_env_file, extract_code, extract_explanation, extract_reasoning
from src.execution_sandbox import execute_in_sandbox


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=str, default="HumanEval/0")
    parser.add_argument("--condition", type=str, choices=["proposed", "baseline1", "baseline2", "both"], default="both")
    parser.add_argument("--config", type=str, default="config/experiment_config.yaml")
    return parser.parse_args()


def main():
    load_env_file()
    args = parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env or environment!")
        sys.exit(1)

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    task_id = args.task_id
    if not task_id.startswith("HumanEval/"):
        task_id = f"HumanEval/{task_id}"

    target_task = None
    with open("data/humaneval_test.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if item["task_id"] == task_id:
                target_task = item
                break

    if not target_task:
        print(f"ERROR: Task '{task_id}' not found.")
        sys.exit(1)

    print("\n" + "=" * 80)
    print(f"LIVE DEFENCE DEMONSTRATION: {target_task['task_id']} ({target_task['entry_point']})")
    print(f"Complexity Tier: {target_task['complexity_tier']} | Cyclomatic Complexity (CC): {target_task['cyclomatic_complexity']}")
    print("=" * 80)
    print("\n[PROBLEM SPECIFICATION]:")
    print(target_task["prompt"].strip())
    print("\n" + "-" * 80)

    from google import genai
    client = genai.Client(api_key=api_key)

    conditions_to_run = []
    if args.condition in ["baseline1", "both"]:
        conditions_to_run.append(("baseline1", config["models"]["baseline1"]["id"], "Zero-Shot (gemini-3.1-flash-lite)", config["prompts"]["zero_shot"]))
    if args.condition in ["proposed", "both"]:
        conditions_to_run.append(("proposed", config["models"]["proposed"]["id"], "Proposed CoT (gemini-3.5-flash-lite)", config["prompts"]["cot"]))

    for cond_name, model_id, desc, prompt_tmpl in conditions_to_run:
        print(f"\n>>> QUERYING GOOGLE GEMINI API: {desc}...")
        formatted_prompt = prompt_tmpl.format(prompt=target_task["prompt"])

        t0 = time.time()
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=formatted_prompt
            )
            elapsed = time.time() - t0

            resp_parts = []
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for p in response.candidates[0].content.parts:
                    if getattr(p, "text", None):
                        resp_parts.append(p.text)
            resp_text = "".join(resp_parts) if resp_parts else ""

            code = extract_code(resp_text)
            explanation = extract_explanation(resp_text)
            reasoning = extract_reasoning(resp_text)

            print(f"API Generation Time: {elapsed:.2f} seconds")

            if reasoning:
                print("\n[CHAIN-OF-THOUGHT REASONING]:")
                print(reasoning[:400] + ("..." if len(reasoning) > 400 else ""))

            print("\n[EXTRACTED PYTHON CODE]:")
            print(code)

            print("\n[EXTRACTED EXPLANATION]:")
            print(explanation[:250] + ("..." if len(explanation) > 250 else ""))

            print("\n>>> EXECUTING UNIT TESTS IN MULTIPROCESSING SANDBOX (3.0s WATCHDOG)...")
            exec_res = execute_in_sandbox(code, target_task["test"], target_task["entry_point"], timeout=3.0)

            if exec_res["passed"]:
                print(f"VERIFICATION STATUS:  PASSED  100% of hidden unit tests passed successfully!")
            else:
                print(f"VERIFICATION STATUS:  FAILED ({exec_res['status']}) - {exec_res['details']}")

            print("-" * 80)

        except Exception as e:
            print(f"Live API error: {e}")

    print("\nDEMONSTRATION COMPLETED.\n")


if __name__ == "__main__":
    main()
