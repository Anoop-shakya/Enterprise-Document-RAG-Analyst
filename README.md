# OmniStream: Multi-Source Industrial RAG Platform 🔮

A production-grade Retrieval-Augmented Generation (RAG) platform built with Python, Streamlit, and LangChain Core. This application is engineered to ingest, chunk, index, and securely query massive 600+ page PDFs, live website links, and YouTube multimedia video transcripts using state-of-the-art open-weight models via the Groq Cloud API.

## 🚀 Key Features
- **Omni-Channel Ingestion:** Supports automated text streaming from multi-page local PDFs, live HTML DOM web scraping, and real-time YouTube subtitle extraction.
- **Advanced Structural Scanner:** Implements a customized punctuation-stripping token intersection array that maps exact keyword density, solving semantic dilution for textbook headers and small layout indexes.
- **Stateless Tenant Isolation:** Dynamically handles concurrent browser sessions via unique `uuid4` memory sandboxes to prevent cross-user data leakage.
- **Native Multi-Lingual Architecture:** Leverages model context vector alignments to accept prompt queries and return accurate synthesised answers in any native global language fluently.
- **Dual-Engine Hybrid Generation Routing:** Features active instruction guardrails that switch smoothly between text-base document extractions and high-level training data parameters for code structure blueprints.

## 🛠️ Industrial Tech Stack
- **Language Layer:** Python 3.10+
- **Orchestration Network:** LangChain Core
- **Inference Infrastructure:** Groq Cloud API Engine
- **AI Core Reasoning Model:** Llama 3.3 70B / OpenAI GPT-OSS (120B parameter capacity)
- **Data Scraping Utilities:** BeautifulSoup4 & YouTube Transcript API
- **Document Stream Parser:** PyPDF (PdfReader Iteration Blocks)
- **User Interface Framework:** Streamlit Dashboard Nodes

## 📦 Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd Enterprise-Document-RAG-Analyst
   ```

2. **Install Core System Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Live Application Server:**
   ```bash
   streamlit run app.py
   ```

## ⚙️ How It Works (System Architecture)
1. **Data Streaming:** Unstructured assets are systematically split page-by-page or block-by-block into clean, standardized 150-word semantic packet arrays to secure local server RAM boundaries.
2. **Context Filtering:** A keyword intersection loop scans text arrays against normalized user query strings, isolating and ranking high-relevance paragraphs.
3. **API Routing:** The isolated contextual paragraphs are combined with strict boundary system rules and dispatched securely over the network grid to the Groq inference engine to generate a hallucination-free output frame.

