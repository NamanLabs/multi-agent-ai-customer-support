# TechMart Multi-Agent AI Customer Support Assistant

A multi-agent AI customer support system using RAG and LLMs. Built for a fictional
company, **TechMart Electronics**. Queries are classified by intent, routed to one
or more specialized agents (Billing, Technical, Product, Complaint, FAQ), each of
which retrieves relevant company-document context via RAG before generating a
grounded response. Unresolved or low-confidence queries are automatically flagged
for human escalation.

## Architecture

```
Customer -> Chat UI -> FastAPI Backend
                            |
                    Intent Detection Agent
                            |
                       Agent Router  ----------> (multi-agent dispatch)
                    /    |     |     \      \
              Billing  Tech  Product  Complaint  FAQ
                    \    |     |     /      /
                     Retrieval (FAISS + MiniLM embeddings)
                            |
                    Response Aggregator
                            |
                     Final Response  ----> saved to MongoDB (Conversation Memory)
```

## Setup

### 1. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
```
Edit `.env`:
- `GROQ_API_KEY` — get a free key at https://console.groq.com/keys
- `MONGO_URI` — local MongoDB, or a free MongoDB Atlas cluster connection string

### 3. Generate the knowledge base (already generated, re-run if you edit content)
```bash
python knowledge_base/generate_kb.py
```

### 4. Build the RAG index
```bash
python -m backend.rag.ingest
```
First run downloads the `all-MiniLM-L6-v2` embedding model (~90MB) — needs internet.

### 5. Run the backend
```bash
uvicorn backend.main:app --reload --port 8000
```
API docs available at `http://localhost:8000/docs`.

### 6. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/chat` | Send a message, get routed multi-agent response |
| GET | `/sessions/{session_id}/history` | Get conversation history |
| GET | `/analytics/summary` | Conversation + agent usage stats |
| GET | `/health` | Health check |

## Project Structure

```
customer-support-ai/
├── frontend/              # Next.js + Tailwind chat UI
├── backend/
│   ├── agents/             # Intent detection, router, 5 specialized agents
│   ├── rag/                 # Chunking, embedding, FAISS ingestion & retrieval
│   ├── vectorstore/       # Generated FAISS index (gitignored)
│   ├── database/           # MongoDB connection, auth, conversation memory
│   ├── models/               # Pydantic schemas
│   └── main.py               # FastAPI app
├── knowledge_base/     # TechMart Electronics company PDFs
├── requirements.txt
└── README.md
```

## Testing the multi-agent routing

Try this query to see multi-agent dispatch in action (matches the spec's example):
```
"I paid yesterday but Premium is still locked."
```
This should invoke both the Billing Agent and Technical Support Agent.

## Notes

- Escalation triggers on: low intent-classification confidence (<0.45), detected
  Complaint intent, or strong negative-sentiment keywords in the query.
- Chat works for guest users too; login is optional but enables session
  history tied to a real account.
