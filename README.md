

**RAG Document Chatbot (OpenRouter + FAISS + Streamlit)**

A **free, modern, lightweight Retrieval-Augmented Generation (RAG) chatbot** built using:

✔ **LangChain**
✔ **HuggingFace Embeddings**
✔ **FAISS vector store (fully offline & free)**
✔ **OpenRouter LLM models (free tier models)**
✔ **Streamlit ChatGPT-style UI**

This app allows users to **upload a document (PDF / DOCX / TXT)** and chat with it.
The chatbot retrieves relevant chunks using FAISS & answers using an OpenRouter LLM.

---

## 🚀 **Features**

### 🔍 Document Processing

* Upload **PDF, DOCX, or TXT**
* Automatic text extraction
* Smart chunking: `1000 tokens` with `200 overlap`
* Metadata preserved (source filename)

### 🧠 RAG Pipeline

* Free **sentence-transformers/all-MiniLM-L6-v2** embeddings
* **FAISS** vector database (fast, fully local)
* **Conversational Retrieval Chain** from LangChain
* Supports **multi-turn chat history**

### 🤖 LLM Integration (Free)

Uses **OpenRouter** with models like:

* `meta-llama/llama-3.1-8b-instruct:free`
* `google/gemini-flash-1.5:free`
* `qwen/qwen-2.5-72b-instruct:free`

### 💬 UI (Streamlit)

* ChatGPT-style chat bubbles
* Fixed chat input at bottom
* “View Sources” expander for transparency
* Upload file from sidebar
* Clear chat button
* Auto-scroll conversation

### 🛠️ Tech Stack

| Component    | Technology          |
| ------------ | ------------------- |
| UI           | Streamlit           |
| LLM          | OpenRouter API      |
| Embeddings   | HuggingFace         |
| Vector Store | FAISS               |
| RAG          | LangChain           |
| File Parsing | PyPDF2, python-docx |

---

## 📦 **Installation**

### 1️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` file

Inside your project folder:

```
OPENROUTER_API_KEY=your_key_here
```

---

## ▶️ **Run the App**

```bash
streamlit run rag_chat.py
```

Then open the link from the terminal (usually [http://localhost:8501](http://localhost:8501)).

---

## 🧩 **How it Works (Architecture)**

```
          ┌──────────────┐
          │   User Upload │
          └───────┬──────┘
                  ▼
     ┌────────────────────────┐
     │ Text Extraction (PDF,  │
     │ DOCX, TXT)             │
     └─────────┬──────────────┘
               ▼
 ┌───────────────────────────┐
 │ Recursive Text Splitter   │
 │ 1000 size, 200 overlap    │
 └────────────┬──────────────┘
              ▼
     ┌──────────────────┐
     │ HuggingFace       │
     │ Embeddings        │
     └─────────┬────────┘
               ▼
      ┌─────────────────┐
      │   FAISS Index   │
      │ (local vectorDB)│
      └─────────┬───────┘
                ▼
   ┌────────────────────────────┐
   │ ConversationalRetriever    │
   │ + Chat Model (OpenRouter)  │
   └──────────────┬─────────────┘
                  ▼
            ┌──────────┐
            │  Answer   │
            │ + Sources │
            └──────────┘
```

---

## 📚 **Supported Models (Free Options)**

You can switch LLMs in the sidebar.

| Model                 | Type             | Cost |
| --------------------- | ---------------- | ---- |
| llama-3.1-8b-instruct | General QA       | Free |
| gemini-flash-1.5      | Fast reasoning   | Free |
| qwen-2.5-72b          | Strong responses | Free |

All served through **OpenRouter**, so no paid tokens needed.

---

## 📁 **Project Structure**

```
rag-chat/
│
├── rag_chat.py          # Main RAG chatbot app (your file)
├── requirements.txt
├── README.md
└── .env                 # Contains OPENROUTER_API_KEY
```

---

## 🧠 **Why FAISS Instead of Chroma?**

| Feature    | FAISS     | Chroma   |
| ---------- | --------- | -------- |
| Speed      | ⚡ Fastest | Good     |
| Offline    | ✔ Yes     | ✔ Yes    |
| Disk usage | Low       | High     |
| Latency    | Ultra low | Moderate |
| Complexity | Simple    | Medium   |

FAISS is best for **lightweight local RAG systems**.

---

## 🔒 **Security**

* Your API key is loaded from `.env` (never hard-coded)
* No data is sent anywhere except to OpenRouter for LLM inference
* Vectorstore runs **completely local**

---

## 🌟 **Future Enhancements (Free)**

* PDF page number tracking
* Support for multiple file uploads
* Better chunking using Document Transformers
* Reranking with free BGE model
* Offline LLM (llama.cpp)
* Add citations with page numbers


---

## 🙌 **Author**

Built by **Santhiya G** using only free, open technologies.

---


Just tell me!
