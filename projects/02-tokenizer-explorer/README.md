# Byte Pair Tokenizer Explorer

Roadmap topic: Tokenization.

Train byte-pair merges from a sample corpus and inspect the vocabulary, token IDs, and reversible token pieces. Run python main.py; edit the corpus in data/sample_corpus.txt to see how learned merges change.

This character-level BPE implementation is a small educational example, not a production tokenizer. Run python main.py --smoke to check that pieces decode back to the original sample.
