import os
import re
import uuid
import streamlit as st
import urllib.request
from bs4 import BeautifulSoup
from pypdf import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# 1. Advanced High-Scale UI Styling Layout
st.set_page_config(page_title="OmniStream Industrial RAG Platform", layout="wide", page_icon="🔮")
st.title("🔮 OmniStream: Multi-Source Industrial RAG Platform")
st.caption("Advanced data pipeline for enterprise PDFs, live website links, and YouTube video knowledge grids.")

# Initialize global cache directories
if "global_knowledge_cache" not in st.session_state:
    st.session_state.global_knowledge_cache = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "tenant_id" not in st.session_state:
    st.session_state.tenant_id = str(uuid.uuid4())

tenant_key = st.session_state.tenant_id

# 2. Unified Omni-Channel Ingestion Controller (Sidebar)
with st.sidebar:
    st.header("🔑 Control Tower")
    groq_api_key = st.text_input("Enter Groq Cloud Token:", type="password")
    
    st.markdown("---")
    st.header("📥 Ingestion Channel")
    source_type = st.radio("Select Knowledge Source:", ["Corporate PDF", "Live Web URL", "YouTube Video Transcript"])
    
    paragraphs = []
    
    if source_type == "Corporate PDF":
        uploaded_file = st.file_uploader("Ingest Large Document (600+ Pages Supported):", type=["pdf"])
        if uploaded_file and st.button("Compile Document Index"):
            with st.spinner("Streaming page elements to data buffers..."):
                reader = PdfReader(uploaded_file)
                current_block = []
                words = 0
                
                for page_idx, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        for line in text.split("\n"):
                            if line.strip():
                                current_block.append(line.strip())
                                words += len(line.split())
                                if words >= 150:
                                    paragraphs.append(" ".join(current_block))
                                    current_block = []
                                    words = 0
                if current_block:
                    paragraphs.append(" ".join(current_block))

    elif source_type == "Live Web URL":
        web_url = st.text_input("Enter Web Site URL (e.g., https://example.com):")
        if web_url and st.button("Scrape Web Knowledge Base"):
            with st.spinner("Extracting semantic elements from HTML DOM trees..."):
                try:
                    req = urllib.request.Request(web_url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req).read()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    for s in soup(['script', 'style', 'nav', 'footer', 'header']):
                        s.decompose()
                    raw_lines = [p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])]
                    paragraphs = [line for line in raw_lines if len(line) > 50]
                except Exception as e:
                    st.error(f"Scraping Failure: {str(e)}")

    elif source_type == "YouTube Video Transcript":
        yt_url = st.text_input("Enter Public YouTube Video URL:")
        if yt_url and st.button("Extract Video Transcripts"):
            with st.spinner("Connecting to YouTube Cloud Layers..."):
                try:
                    # Target the Langchain loader directly
                    from langchain_community.document_loaders import YoutubeLoader
                    loader = YoutubeLoader.from_youtube_url(yt_url, add_video_info=False)
                    video_docs = loader.load()
                    if video_docs:
                        full_transcript = video_docs.page_content
                        words = full_transcript.split()
                        paragraphs = [" ".join(words[i:i+150]) for i in range(0, len(words), 150)]
                    else:
                        raise ValueError("Subtitles restricted.")
                except Exception as e:
                    # ENTERPRISE FALLBACK LAYER: If cloud IP is banned by YouTube transcripts, scrape DOM layout directly
                    st.warning("🔄 YouTube Subtitle API restricted by cloud IP. Executing deep HTML metadata fallback...")
                    try:
                        req = urllib.request.Request(yt_url, headers={'User-Agent': 'Mozilla/5.0'})
                        html = urllib.request.urlopen(req).read()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract title and video description elements from meta tags (Unblockable by IP bans)
                        title = soup.find("meta", name="title")
                        desc = soup.find("meta", name="description")
                        
                        extracted_meta = []
                        if title: extracted_meta.append(f"Video Title: {title['content']}")
                        if desc: extracted_meta.append(f"Video Context Summary: {desc['content']}")
                        
                        if extracted_meta:
                            paragraphs = extracted_meta
                        else:
                            st.error("Extraction Failure: This specific video has structural scrap constraints.")
                    except Exception as fallback_err:
                        st.error(f"Ultimate System Block: {str(fallback_err)}")

    st.markdown("---")
    if paragraphs:
        st.session_state.global_knowledge_cache[tenant_key] = {
            "paragraphs": paragraphs
        }
        st.sidebar.success(f"🔥 Live Ingestion Complete! Cached {len(paragraphs)} data nodes.")

# 3. Dynamic Conversation Rendering Interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Multi-Lingual Structural Search Engine Loop
if user_query := st.chat_input("Ask a question in any language..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("Scanning structural database layers..."):
            
            db = st.session_state.global_knowledge_cache.get(tenant_key)
            if db:
                clean_query = user_query.lower().strip()
                query_words = [re.sub(r'[^\w]', '', w) for w in clean_query.split() if len(w) > 2]
                matched_segments = []
                
                for p in db["paragraphs"]:
                    p_lower = p.lower()
                    match_count = sum(1 for word in query_words if word in p_lower)
                    if match_count > 0:
                        matched_segments.append((match_count, p))
                
                matched_segments.sort(key=lambda x: x, reverse=True)
                retrieved_chunks = [item for item in matched_segments[:4]]
                context_str = "\n---\n".join(retrieved_chunks) if retrieved_chunks else "\n---\n".join(db["paragraphs"][:2])
            else:
                context_str = "Zero operational context indices loaded into memory."

            if groq_api_key:
                os.environ["GROQ_API_KEY"] = groq_api_key
                llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.1)
                
                system_prompt = (
                    "You are a global-grade Omni-Channel Enterprise Knowledge Architect.\n"
                    "CORE MULTI-LINGUAL CAPABILITY: Respond fluently in the exact same language used by the user in their prompt query.\n\n"
                    "OPERATIONAL PRINCIPLES:\n"
                    "1. Analyze the provided context carefully to answer the question, including headings, chapter names, or text content.\n"
                    "2. If the context contains video metadata descriptions, expand upon that structural layout using your core intelligence to answer the query deeply.\n"
                    "3. If the user asks general engineering system designs or computer science concepts, use your master training weights to provide an exhaustive response.\n\n"
                    "Extracted Knowledge Context:\n{context}"
                )
                prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{question}")])
                
                chain = prompt | llm
                response = chain.invoke({"context": context_str, "question": user_query})
                st.markdown(response.content)
            else:
                st.error("Access Forbidden: Enter your valid Groq API token in the control sidebar to execute neural passes.")
                response = type('', (), {'content': 'System Access Token Deficit.'})()
                
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})


