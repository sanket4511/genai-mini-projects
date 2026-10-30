import argparse
import hashlib
import json
import math
import sqlite3
from pathlib import Path

DIMENSIONS = 96


def embed(text):
    vector = [0.0] * DIMENSIONS
    for token in text.lower().split():
        digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
        index = int.from_bytes(digest[:4], "little") % DIMENSIONS
        vector[index] += 1 if digest[4] % 2 else -1
    norm = math.sqrt(sum(x * x for x in vector)) or 1
    return [x / norm for x in vector]


def add_docs(db, docs):
    db.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, text TEXT, vector TEXT)")
    db.executemany(
        "INSERT INTO documents(text,vector) VALUES (?,?)",
        [(text, json.dumps(embed(text))) for text in docs],
    )
    db.commit()


def search(db, query):
    query_vector = embed(query)
    rows = db.execute("SELECT text,vector FROM documents")
    return sorted(
        ((sum(a * b for a, b in zip(query_vector, json.loads(vector))), text) for text, vector in rows),
        reverse=True,
    )[:3]


def run(path):
    docs = [x.strip() for x in Path("data/documents.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    db = sqlite3.connect(path)
    try:
        db.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, text TEXT, vector TEXT)")
        if db.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 0:
            add_docs(db, docs)
        results = search(db, "solar power from sunlight")
    finally:
        db.close()
    for score, text in results:
        print(f"{score:.3f} {text}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--db", default="data/vector_store.sqlite3")
    args = parser.parse_args()
    if args.smoke:
        smoke_path = Path("data/smoke-vector.sqlite3")
        if smoke_path.exists():
            smoke_path.unlink()
        results = run(smoke_path)
        smoke_path.unlink()
    else:
        results = run(args.db)
    if args.smoke:
        assert results
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
