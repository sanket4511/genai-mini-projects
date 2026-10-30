import argparse
import hashlib
import math
import re
from pathlib import Path

WORD = re.compile(r"[a-z0-9]+")


def terms(text):
    return WORD.findall(text.lower())


def chunks(path, size=55, overlap=10):
    words = path.read_text(encoding="utf-8").split()
    result, start = [], 0
    while start < len(words):
        result.append({"source": path.name, "text": " ".join(words[start:start + size])})
        if start + size >= len(words):
            break
        start += size - overlap
    return result


def vector(text, dimensions=128):
    values = [0.0] * dimensions
    for term in terms(text):
        digest = hashlib.blake2b(term.encode(), digest_size=8).digest()
        index = int.from_bytes(digest[:4], "little") % dimensions
        values[index] += 1 if digest[4] % 2 else -1
    norm = math.sqrt(sum(x * x for x in values)) or 1
    return [x / norm for x in values]


def cosine(left, right):
    return sum(x * y for x, y in zip(left, right))


def lexical(query, text):
    left, right = set(terms(query)), set(terms(text))
    return len(left & right) / math.sqrt(max(1, len(left)) * max(1, len(right)))


def retrieve(query, documents, limit=3):
    synonyms = {"solar": "sunlight photovoltaic", "electricity": "power current", "battery": "storage"}
    expanded = query + " " + " ".join(synonyms.get(term, "") for term in terms(query))
    lexical_rank = sorted(range(len(documents)), key=lambda i: lexical(expanded, documents[i]["text"]), reverse=True)
    query_vector = vector(expanded)
    dense_rank = sorted(range(len(documents)), key=lambda i: cosine(query_vector, vector(documents[i]["text"])), reverse=True)
    fused = {}
    for ranking in (lexical_rank, dense_rank):
        for rank, index in enumerate(ranking, 1):
            fused[index] = fused.get(index, 0) + 1 / (60 + rank)
    pool = sorted(fused, key=fused.get, reverse=True)[:max(limit * 3, limit)]
    selected = []
    while pool and len(selected) < limit:
        best = max(pool, key=lambda i: lexical(query, documents[i]["text"]) + fused[i] - 0.15 * max(
            (cosine(vector(documents[i]["text"]), vector(documents[j]["text"])) for j in selected),
            default=0,
        ))
        selected.append(best)
        pool.remove(best)
    return [(fused[index], documents[index]) for index in selected]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    paths = sorted(Path("data/docs").glob("*.txt"))
    documents = [part for path in paths for part in chunks(path)]
    results = retrieve("How do solar cells create electrical power?", documents)
    for score, item in results:
        print(f"{item['source']} ({score:.4f}): {item['text']}")
    if args.smoke:
        assert results and "solar" in results[0][1]["source"]
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
