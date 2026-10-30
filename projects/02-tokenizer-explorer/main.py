import argparse
from collections import Counter
from pathlib import Path


class BytePairTokenizer:
    def __init__(self, merges, alphabet):
        self.merges = merges
        self.unknown = "<UNK>"
        self.vocabulary = sorted(set(alphabet) | {left + right for left, right in merges})
        self.token_to_id = {token: index for index, token in enumerate(self.vocabulary)}
        self.id_to_token = self.vocabulary + [self.unknown]
        self.unknown_id = len(self.vocabulary)

    @classmethod
    def train(cls, text, max_merges=40):
        symbols, merges = list(text), []
        alphabet = set(symbols)
        for _ in range(max_merges):
            counts = Counter(zip(symbols, symbols[1:]))
            if not counts:
                break
            pair, count = max(counts.items(), key=lambda item: (item[1], item[0]))
            if count < 2:
                break
            merged, output, i = pair[0] + pair[1], [], 0
            while i < len(symbols):
                if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == pair:
                    output.append(merged)
                    i += 2
                else:
                    output.append(symbols[i])
                    i += 1
            symbols, merges = output, merges + [pair]
        return cls(merges, alphabet)

    def encode(self, text):
        symbols = list(text)
        for left, right in self.merges:
            output, i = [], 0
            while i < len(symbols):
                if i + 1 < len(symbols) and symbols[i] == left and symbols[i + 1] == right:
                    output.append(left + right)
                    i += 2
                else:
                    output.append(symbols[i])
                    i += 1
            symbols = output
        return symbols

    def decode(self, tokens):
        return "".join(tokens)

    def encode_ids(self, text):
        return [self.token_to_id.get(token, self.unknown_id) for token in self.encode(text)]

    def decode_ids(self, token_ids):
        return "".join(self.id_to_token[index] for index in token_ids)


def run():
    corpus = Path("data/sample_corpus.txt").read_text(encoding="utf-8")
    tokenizer = BytePairTokenizer.train(corpus)
    sample = "tokenization turns text into reusable pieces."
    pieces = tokenizer.encode(sample)
    print("Learned merges:", len(tokenizer.merges), "| pieces:", pieces)
    print("Vocabulary size:", len(tokenizer.vocabulary))
    print("Token IDs:", tokenizer.encode_ids(sample))
    return tokenizer, sample, pieces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    tokenizer, sample, pieces = run()
    if args.smoke:
        assert tokenizer.decode(pieces) == sample and tokenizer.merges
        assert tokenizer.decode_ids(tokenizer.encode_ids(sample)) == sample
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
