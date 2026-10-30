# SQLite Vector Search

Roadmap topic: Vector Databases.

Persist hashed text vectors in SQLite and retrieve nearby documents. Run python main.py; the local database is created under data. Use --db PATH to choose another location.

The feature-hashing encoder is an inspectable lexical baseline, not a learned embedding model or production vector database. The smoke check uses a temporary database.
