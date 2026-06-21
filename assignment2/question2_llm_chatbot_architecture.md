# What Goes Into Building an LLM Chatbot

A working LLM chatbot has more layers than most people realize. You can't just wrap an API call in a text box and call it done. Every piece has a job, and if one breaks, the whole thing falls apart.

---

## 1. Frontend

This is the part users see and type into. It handles the chat UI, displays responses, and can support things like file uploads or login. Streamlit works well for quick projects, while React or Next.js makes more sense for something you'd actually ship. The frontend sends messages to the backend — through a regular API call or WebSockets when you need the response to come in as it's being generated.

---

## 2. Backend API

The backend sits between the frontend and everything else. It receives incoming requests, validates them, deals with auth, and sends them where they need to go. FastAPI is a popular pick here because it handles multiple requests at once without blocking. It also holds onto session data so the conversation stays coherent across multiple messages.

---

## 3. Orchestration Layer

This is where decisions get made. After a message comes in, something has to figure out what to do with it — pull from documents, call a tool, or go straight to the model. LangGraph and LangChain are built for building these kinds of multi-step flows. Without this layer, the chatbot just blindly forwards every message to the LLM. With it, the system can actually reason about what the right move is.

---

## 4. LLM Integration

The model is what reads the input and writes the response. This layer manages the connection to providers like OpenAI, Groq, or Gemini — it builds the prompt, keeps track of token usage, and parses whatever comes back. Bigger systems sometimes use separate models for different steps, like one for classifying the query and another for writing the final answer.

---

## 5. Vector Database and Retrieval

When the chatbot needs to answer questions about uploaded documents, you need a vector database. The documents get split into chunks, each chunk gets turned into an embedding, and everything gets stored in something like Qdrant, Pinecone, or Weaviate. At query time, the system finds chunks that are semantically close to the question — meaning it understands intent, not just matching words. `text-embedding-3-small` is a go-to embedding model for this.

---

## 6. Conversation Memory

Without memory, every message feels like the first one. Chat history gets saved in a database — MongoDB or Redis are common — so the model has context from earlier in the conversation. LangChain handles this with memory classes that feed the right amount of history into each request without going over the token limit.

---

## 7. Tools and Integrations

Not every question can be answered from stored documents. Sometimes the chatbot needs to look something up online, call an API, or query a database. These get registered as tools the model can choose to use when it decides they're needed. Tavily is a solid option for live web search.

---

## 8. Monitoring

When things go wrong in production, you need data to figure out why. That means tracking response times, token usage, error rates, and failed requests. For monitoring this kind of system, Prometheus covers metrics, ELK Stack takes care of logs, and OpenTelemetry handles tracing. Setting this up early saves a lot of pain later.

---

## How a Request Flows

1. User sends a message → frontend hands it to the backend
2. Backend validates it and loads the session history
3. Orchestration layer reads the message and classifies what kind of question it is
4. Based on that, it searches the vector DB, fires a tool, or goes to the LLM directly
5. Retrieved documents get checked — if they're not relevant, the query gets rewritten and search runs again
6. LLM writes the answer using the context and chat history
7. Response goes back to the user, conversation gets saved
8. Logs get collected to tune things over time

---

## Design Choices Worth Knowing

| Decision | Why It Matters |
|---|---|
| **Async** | FastAPI with async doesn't get stuck when multiple users send messages at once |
| **Streaming** | Users see tokens arriving as the model writes, which feels much faster |
| **Caching** | Repeated questions can be served from Redis instead of calling the model each time |
| **Fallbacks** | External services go down sometimes; the system should handle that without crashing |
| **Security** | Keys in env variables, rate limits on endpoints, and input sanitization before anything hits the model |