import argparse
import json
from pathlib import Path


def build_prompt(task, requirements):
    numbered = "\n".join(f"{i}. {item}" for i, item in enumerate(requirements, 1))
    return f"You are a careful assistant.\nTask: {task}\nConstraints:\n{numbered}\nReturn valid JSON with keys: summary, evidence."


def evaluate(case, response):
    keys = set(response) if isinstance(response, dict) else set()
    return {
        "valid_json_object": isinstance(response, dict),
        "missing_keys": sorted(set(case["expected_keys"]) - keys),
    }


def run():
    cases = json.loads(Path("data/eval_cases.json").read_text(encoding="utf-8"))
    for case in cases:
        print("Prompt:\n" + build_prompt(case["task"], case["requirements"]))
        print("Fixed offline fixture:", json.dumps(case["mock_result"]))
        print("Checks:", evaluate(case, case["mock_result"]))
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    cases = run()
    if args.smoke:
        assert all(not evaluate(case, case["mock_result"])["missing_keys"] for case in cases)
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
