import argparse
import math

try:
    import numpy as np
except ImportError:
    np = None


def positional_encoding(length, width):
    pos = np.arange(length)[:, None]
    dim = np.arange(width)[None, :]
    angle = pos / np.power(10000.0, (2 * (dim // 2)) / width)
    result = np.zeros((length, width))
    result[:, 0::2] = np.sin(angle[:, 0::2])
    result[:, 1::2] = np.cos(angle[:, 1::2])
    return result


def self_attention(x):
    rng = np.random.default_rng(7)
    width = x.shape[-1]
    q, k, v = (x @ rng.normal(0, 0.3, (width, width)) for _ in range(3))
    scores = q @ k.T / math.sqrt(width)
    scores = np.where(np.triu(np.ones_like(scores, dtype=bool), 1), -1e9, scores)
    scores -= scores.max(axis=-1, keepdims=True)
    weights = np.exp(scores)
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights @ v, weights


def run():
    words = ["A", "small", "model", "learns"]
    x = np.random.default_rng(3).normal(0, 0.2, (len(words), 8))
    x += positional_encoding(len(words), 8)
    output, weights = self_attention(x)
    print("Tokens:", words, "| output shape:", output.shape)
    print("Causal attention weights:")
    print(np.round(weights, 2))
    return weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if np is None:
        print("SMOKE_SKIPPED install requirements.txt (NumPy required)")
        return 0
    weights = run()
    if args.smoke:
        assert weights.shape == (4, 4) and np.allclose(np.triu(weights, 1), 0)
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
