import argparse
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


def train(text, order=3):
    model = defaultdict(Counter)
    padded = "^" * order + text
    for i in range(order, len(padded)):
        model[padded[i - order:i]][padded[i]] += 1
    return model, order


def generate(model, seed_text="The", length=160, temperature=0.8, seed=4):
    counts, order = model
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    rng, output = random.Random(seed), seed_text
    for _ in range(length):
        options = counts.get(output[-order:])
        if not options:
            break
        chars = list(options)
        logits = [math.log(options[c]) / temperature for c in chars]
        peak = max(logits)
        output += rng.choices(chars, weights=[math.exp(x - peak) for x in logits], k=1)[0]
    return output


def run(temp):
    model = train(Path("data/tiny_corpus.txt").read_text(encoding="utf-8"))
    result = generate(model, temperature=temp)
    print(f"Character n-gram toy generator, temperature={temp}:\n{result}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    result = run(args.temperature)
    if args.smoke:
        assert result.startswith("The")
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
