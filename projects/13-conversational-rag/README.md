# Memory-Based Knowledge Assistant

Roadmap topic: Conversational RAG.

Ask questions about the sample knowledge file in a multi-turn CLI session. A short conversational signal uses the previous question to resolve simple references; retrieved sentences are shown with source numbers. Run python main.py and type /quit to save.

Conversation history is stored locally as JSON. This is a retrieval and memory demo, not a generated answer from a pretrained model. Avoid placing sensitive content in its history file. Run python main.py --smoke for a temporary-file check.
