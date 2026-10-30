import argparse
import math
import re
from pathlib import Path

WORD = re.compile(r"[a-z0-9]+")


def chunk(text, size=70, overlap=12):
    words = text.split()
    result, start = [], 0
    while start < len(words):
        result.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return result


def rank(query, chunks):
    q = set(WORD.findall(query.lower()))
    scored = []
    for index, text in enumerate(chunks):
        terms = set(WORD.findall(text.lower()))
        score = len(q & terms) / math.sqrt(max(1, len(q)) * max(1, len(terms)))
        scored.append((score, index, text))
    return sorted(scored, reverse=True)


def answer(query, chunks):
    found = [item for item in rank(query, chunks) if item[0] > 0][:3]
    if not found:
        return "No evidence found in supplied document.", []
    evidence = "\n".join(f"[chunk {index + 1}] {text}" for _, index, text in found)
    return "Relevant evidence:\n" + evidence, [index + 1 for _, index, _ in found]


def load_document(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--document", default="data/faq.txt")
    args = parser.parse_args()
    chunks = chunk(load_document(args.document))
    question = "What converts sunlight into electricity?"
    response, sources = answer(question, chunks)
    print("Question:", question)
    print(response)
    print("Sources:", sources)
    if args.smoke:
        assert "photovoltaic" in response.lower() and sources
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
