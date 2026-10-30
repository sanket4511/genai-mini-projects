# Multi-Model API Comparison

Roadmap topic: LLM APIs.

Compare two configurable OpenAI-compatible chat-completions endpoints by response and latency. Copy .env.example to .env, replace both model names and API keys, then run python main.py. The example values are placeholders and must be replaced before a live call.

The adapter reads secrets from environment variables and never prints them. Do not commit .env or send private data to a provider without permission. Run python main.py --smoke for a no-network check.
