# Question 5: Most Complex Database Code

**File:** `src/rag/retriever_setup.py`  
**Repo:** Ishant713/AgenticRAG  
**Link:** [retriever_setup.py on GitHub](https://github.com/Ishant713/AgenticRAG/blob/main/src/rag/retriever_setup.py)

---

## Why This Is My Most Complex Database File

`graph_builder.py` handles the thinking, but this file is where data actually lives. It controls the vector database — the thing that finds and returns relevant documents when a question comes in. Looks simple from the outside, but there's more to it than it seems.

---

## Breakdown

### 1. One Shared Vector Store for the Whole App

I used a global `_vectorstore` variable to hold the Qdrant index. Keeping it global means every part of the app talks to the same index — no duplicates, no inconsistency. It's a straightforward decision but an important one.

---

### 2. Lazy Initialization

`get_retriever()` doesn't build the vector store on startup. It waits until something actually needs it. If no files have been uploaded yet, it quietly creates a placeholder document just so the store has something to initialize with. That way the app stays up and running even before any real data exists.

```python
def get_retriever():
    global _vectorstore
    if _vectorstore is None:
        dummy_doc = Document(page_content="Placeholder", metadata={"source": "init"})
        _vectorstore = Qdrant.from_documents([dummy_doc], embeddings)
    return _vectorstore.as_retriever(search_kwargs={"k": 4})
```

---

### 3. Adding New Documents on the Fly

Early on I noticed that every upload was resetting the whole index, which meant previously added documents would vanish. Not great. So I tweaked `retriever_chain()` — now it checks if an index is already there before doing anything. New chunks get added to whatever exists. If nothing's there yet, it starts fresh. Small change, but it fixed a real problem.

```python
def retriever_chain(chunks):
    global _vectorstore
    if _vectorstore is not None:
        _vectorstore.add_documents(chunks)
    else:
        _vectorstore = Qdrant.from_documents(chunks, embeddings)
    return True
```

---

### 4. Embeddings

Each document chunk gets converted into a vector — specifically 1536 dimensions — using OpenAI's `text-embedding-3-small`. This is what powers semantic search. The system stops caring about exact words and starts finding content that actually matches the meaning of the question.

---

### 5. Why Qdrant

Qdrant is persistent and production-ready, which is exactly what this system needs. Unlike in-memory options, data survives server restarts and the index scales well as more documents get added. It was the right choice from the start given that the app is meant to handle real document uploads over time, not just quick demos.
