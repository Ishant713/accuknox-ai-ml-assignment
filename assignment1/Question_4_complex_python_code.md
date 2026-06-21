# Question 4: Most Complex Python Code

## File Path: `src/rag/graph_builder.py`

**GitHub Repository:** [Ishant713/AgenticRAG](https://github.com/Ishant713/AgenticRAG)

**Full URL:**  
[https://github.com/Ishant713/AgenticRAG/blob/main/src/rag/graph_builder.py](https://github.com/Ishant713/AgenticRAG/blob/main/src/rag/graph_builder.py)

---

## Why I consider this my most complex file

This file is the core of my AgenticRAG project. It's not a simple script that runs top to bottom — it builds a workflow using LangGraph where the system can make decisions, check its own output, and retry if something goes wrong.
Most basic chatbots just take a question and return an answer. This one actually thinks through the problem — it figures out what kind of question is being asked, fetches relevant information, checks whether that information is actually useful, and if it's not, it rephrases the question and tries again.

---

## Shared state across the whole workflow

There's a GraphState object that every part of the system reads from and writes to. It holds the user's question, retrieved documents, the final answer, and the session ID for chat history. Keeping this consistent across multiple nodes that all run at different points was honestly one of the trickier parts to get right.

---

## Seven separate nodes, each doing one job

I broke the whole process into seven nodes:
* query_analysis- Figures out if the question needs document search, web search, or just the LLM
* retriever - Pulls relevant chunks from the vector store.
* grade_documents- Checks if what was retrieved is actually relevant.
* rewrite_query - Rephrases the question if the retrieval didn't work well
* generate - Builds the final answer using the LLM and retrieved context
* web_search - Fetches live results via Tavily for current events
* general_llm - Answers directly from the model's own knowledge when no retrieval is needed
---

## The routing logic

After query_analysis, the system decides which path to take — retrieval, web search, or direct answer. After grading the documents, it either moves forward to generate an answer or loops back to rewrite the query. None of this is hardcoded; the data drives the decision.

---

## The retry loop

This is the part I'm most proud of. If the retrieved documents aren't relevant, the system doesn't just give a bad answer — it rewrites the query and searches again. It's a simple loop on paper, but getting it to work reliably took a lot of tuning

---

## Everything working together

The file ties together LangGraph, LangChain, OpenAI/Groq, FAISS/Qdrant, Tavily, and MongoDB in one place. Getting all of these to work together without things breaking was a challenge in itself.

---

