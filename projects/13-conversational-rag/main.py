import argparse
import json
import re
import tempfile
from pathlib import Path

WORD = re.compile(r"[a-z0-9]+")


def retrieve(question, history, document):
    query = question
    if history and any(term in question.lower().split() for term in ("it", "they", "that", "those", "them")):
        query = history[-1].get("user", "") + " " + question
    query_terms = set(WORD.findall(query.lower()))
    paragraphs = [part.strip() for part in re.split(r"(?<=[.!?])\s+", document) if part.strip()]
    ranked = sorted(
        ((len(query_terms & set(WORD.findall(text.lower()))), index, text) for index, text in enumerate(paragraphs)),
        reverse=True,
    )
    matches = [(index, text) for score, index, text in ranked[:3] if score]
    if not matches:
        return "I couldn't find support in the documents.", []
    return " ".join(text for _, text in matches), [index + 1 for index, _ in matches]


def respond(question, history, document):
    answer, citations = retrieve(question, history, document)
    if citations:
        answer += " [sources: " + ", ".join(map(str, citations)) + "]"
    history.append({"user": question, "assistant": answer})
    return answer


def run(history_path, interactive=True):
    document = Path("data/knowledge.txt").read_text(encoding="utf-8")
    history_path = Path(history_path)
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    if interactive:
        print("Ask about the sample knowledge base; type /quit to save.")
        while True:
            question = input("You: ").strip()
            if question.lower() in {"/quit", "quit", "exit"}:
                break
            if question:
                print("Assistant:", respond(question, history, document))
    else:
        answer = respond("How does it store energy?", history, document)
        history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
        print("Assistant:", answer)
        return answer, history
    history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
    return None, history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--history", default="chat_history.json")
    args = parser.parse_args()
    if args.smoke:
        smoke_path = Path("smoke_history.json")
        if smoke_path.exists():
            smoke_path.unlink()
        answer, history = run(smoke_path, interactive=False)
        smoke_path.unlink()
        assert "battery" in answer.lower() and len(history) == 1
        print("SMOKE_OK")
    else:
        run(args.history)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
