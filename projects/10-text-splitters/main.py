import argparse
import re
from pathlib import Path


def split_words(text, chunk_size=24, overlap=5):
    if chunk_size <= overlap or overlap < 0:
        raise ValueError("Require chunk_size > overlap >= 0")
    words = re.findall(r"\S+", text)
    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    text = Path("data/long_note.txt").read_text(encoding="utf-8")
    chunks = split_words(text)
    for index, chunk in enumerate(chunks, 1):
        print(f"Chunk {index} ({len(chunk.split())} words): {chunk}")
    if args.smoke:
        assert len(chunks) > 1 and chunks[0].split()[-5:] == chunks[1].split()[:5]
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
