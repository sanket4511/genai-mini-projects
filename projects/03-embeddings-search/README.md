# Semantic Search

Roadmap topic: Embeddings.

Rank the included documents with an offline TF-IDF baseline. Run python main.py. TF-IDF is a lexical vector method, not a neural embedding.

For dense local embeddings, install requirements-embeddings.txt and run python main.py --dense. This option downloads a model on first use. Compare the rankings and notice how paraphrases affect each approach. Run python main.py --smoke for the offline baseline check.
