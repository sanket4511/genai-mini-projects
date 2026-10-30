import argparse
import math
import re
from pathlib import Path

WORD = re.compile(r"[a-z0-9]+")


def tokens(text):
    return WORD.findall(text.lower())


def tfidf(documents):
    rows = [tokens(text) for text in documents]
    vocab = {term for row in rows for term in row}
    idf = {t: math.log((1 + len(rows)) / (1 + sum(t in row for row in rows))) + 1 for t in vocab}
    vectors = []
    for row in rows:
        raw = {t: row.count(t) * idf[t] for t in set(row)}
        norm = math.sqrt(sum(x * x for x in raw.values())) or 1
        vectors.append({t: v / norm for t, v in raw.items()})
    return vectors


def search(query, documents, vectors):
    q = tfidf([query] + documents)[0]
    return sorted(
        ((sum(v * vector.get(t, 0) for t, v in q.items()), i) for i, vector in enumerate(vectors)),
        reverse=True,
    )


def dense_search(query, documents, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    vectors = model.encode([query] + documents, normalize_embeddings=True)
    return sorted(((float(s), i) for i, s in enumerate(vectors[1:] @ vectors[0])), reverse=True)


def run(dense=False):
    docs = [x.strip() for x in Path("data/documents.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    query = "How do solar panels produce electricity?"
    results = dense_search(query, docs) if dense else search(query, docs, tfidf(docs))
    print("Backend:", "sentence-transformers" if dense else "offline TF-IDF lexical baseline")
    for score, i in results[:3]:
        print(f"{score:.3f} {docs[i]}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dense", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    try:
        results = run(args.dense)
    except ImportError:
        print("Install requirements-embeddings.txt for dense embeddings.")
        return 1
    if args.smoke:
        assert results and results[0][1] == 0
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
