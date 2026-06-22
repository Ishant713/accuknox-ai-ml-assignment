# Question 5: Most Complex Database Code

**File:** `src/rag/retriever_setup.py`
**Repo:** `Ishant713/AgenticRAG`

---

## Why This Is My Most Complex Database File

This file handles the document retrieval side of the RAG system. When a user uploads documents, this is what converts them into vectors, stores them, and makes them searchable by the AI agent. It looks simple on the surface, but it's doing quite a few things at once — processing documents, generating embeddings, managing vector storage, and exposing all of that as a tool the agent can actually use.

---

## 1. Turning Text Into Vectors

Before anything can be stored or searched, the document chunks need to be converted into numbers. I used the `sentence-transformers/all-MiniLM-L6-v2` model from Hugging Face for this.

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

The reason this matters is that these embeddings capture *meaning*, not just words. So if a user asks something in different phrasing than what's in the document, the system can still find the right content.

---

## 2. Building the Vector Store

When documents are uploaded, `retriever_chain()` takes the chunks and builds a FAISS index from them.

```python
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)
```

Each chunk gets embedded and stored in the index. From there, FAISS can do fast similarity searches across all of them.

---

## 3. Keeping One Shared Index

To avoid rebuilding the vector store on every query, it gets saved to a global variable.

```python
_faiss_vectorstore = vectorstore
```

This way, every part of the app reads from the same index without recreating it each time. Simple but important for performance.

---

## 4. Setting Up the Retriever

`get_retriever()` takes the stored index and turns it into a retriever object.

```python
retriever = _faiss_vectorstore.as_retriever(
    search_kwargs={"k": 3}
)
```

The `k=3` means it pulls the 3 most relevant chunks for any given query. That's usually enough context for the model to generate a good answer without flooding it with too much information.

---

## 5. Wrapping It as an Agent Tool

The retriever gets wrapped into a LangChain tool so the agent knows it exists and can call it when needed.

```python
retriever_tool = create_retriever_tool(
    retriever,
    "retriever_customer_uploaded_documents",
    description
)
```

This is what connects the document search to the actual agent workflow. Without this step, the agent wouldn't know how or when to search the uploaded files.

---

## 6. Dynamic Tool Description

The tool's description — which tells the agent when to use it — gets loaded from a text file at runtime.

```python
with open("description.txt", "r", encoding="utf-8") as f:
    description = f.read()
```

This means you can change how the retriever behaves for different document types without touching the code. Just update the description file.

---

## Why This File Matters

This is the bridge between uploaded documents and the AI agent. Take it out and the agent has no way to access or reason over anything the user uploads. It handles embedding, storage, search, and tool registration — all in one place. That's why I'd point to this as my most complex database-related code.
