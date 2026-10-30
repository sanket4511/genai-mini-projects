# Grounded Document Q&A

Roadmap topic: Basic RAG.

Follow the retrieval-augmented generation flow: split a document, rank relevant chunks, and return supporting evidence with chunk references. Run python main.py and edit data/faq.txt or the example question.

The response is extractive rather than generated, keeping grounding visible and the project offline. A full RAG system would add a generation model after retrieval and require citations. This lexical baseline can miss paraphrases. To query a PDF, install requirements-optional.txt and pass its path with the --document option.
