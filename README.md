# 13 Mini Projects: LLM and RAG Engineering Roadmap

A hands-on Python portfolio moving from Transformer fundamentals to conversational RAG. Every project has its own source, setup notes, requirements, and synthetic sample data.

## Roadmap

| # | Topic | Mini-project |
|---|---|---|
| 1 | Transformer | [Mini Transformer](projects/01-mini-transformer/README.md) |
| 2 | Tokenization | [Byte Pair Tokenizer Explorer](projects/02-tokenizer-explorer/README.md) |
| 3 | Embeddings | [Semantic Search](projects/03-embeddings-search/README.md) |
| 4 | LLM | [Local Text Generation Playground](projects/04-llm-playground/README.md) |
| 5 | Prompt Engineering | [Prompt Evaluation Lab](projects/05-prompt-engineering/README.md) |
| 6 | LLM APIs | [Multi-Model API Comparison](projects/06-llm-api-comparison/README.md) |
| 7 | Vector Databases | [SQLite Vector Search](projects/07-vector-database/README.md) |
| 8 | LangChain | [LCEL Workflow](projects/08-langchain-lcel/README.md) |
| 9 | Document Loaders | [Document Intelligence](projects/09-document-loaders/README.md) |
| 10 | Text Splitters | [Intelligent Chunking](projects/10-text-splitters/README.md) |
| 11 | Basic RAG | [Grounded Document Q&A](projects/11-basic-rag/README.md) |
| 12 | Advanced RAG | [Hybrid Retrieval and Reranking](projects/12-advanced-rag/README.md) |
| 13 | Conversational RAG | [Memory-Based Knowledge Assistant](projects/13-conversational-rag/README.md) |

## Quick start

Use Python 3.10 or newer. Open a project folder, install its requirements with **python -m pip install -r requirements.txt**, then run **python main.py**. For example, begin in **projects/02-tokenizer-explorer**.

Most projects use only the standard library. Project 1 requires NumPy; project 3 offers optional dense embeddings; project 8 uses LangChain Core; project 9 lists optional PDF and DOCX packages.

## Offline checks

Run **python check_all.py** from this repository folder. Smoke checks do not call paid APIs or download models. Missing optional dependencies are reported as skips.

## Safety and learning notes

Sample content is synthetic. The API comparison reads keys from environment variables or a local .env file; copy its example file and replace placeholders. Never commit .env or real credentials. Retrieval examples print evidence and source identifiers. The tiny generator and prompt fixture are learning aids, not pretrained LLMs. Optional dense embeddings download weights only when explicitly selected.
