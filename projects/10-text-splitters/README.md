# Intelligent Document Chunking

Roadmap topic: Text Splitters.

Split text into overlapping word windows and inspect the effect of chunk size and overlap. Run python main.py, then adjust chunk_size and overlap in split_words.

This starter uses word windows. Production chunking may split by pages, paragraphs, tokens, or semantic boundaries and should retain source metadata with each chunk. Run python main.py --smoke for the offline overlap check.
