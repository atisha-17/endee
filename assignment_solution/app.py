import streamlit as st
from engine import EndeeEngine

st.set_page_config(page_title="Endee Semantic Search", page_icon="⚡")

# Initialize Engine
if 'engine' not in st.session_state:
    st.session_state.engine = EndeeEngine()
    st.session_state.engine.ensure_index()

st.title("⚡ Endee High-Performance AI Agent")
st.markdown("This project demonstrates **Semantic Search** using the Endee Vector Database.")

# Sidebar for Ingestion
with st.sidebar:
    st.header("📥 Data Ingestion")
    doc_text = st.text_area("Paste text to index:", height=150)
    if st.button("Index to Endee"):
        if doc_text:
            with st.spinner("Vectorizing..."):
                lat = st.session_state.engine.add_document(doc_text)
                st.success(f"Indexed in {lat*1000:.2f}ms")
        else:
            st.warning("Please enter some text.")

# Main Search UI
st.header("🔍 Intelligent Search")
query = st.text_input("Ask a question about your data:")

if query:
    results, latency = st.session_state.engine.search(query)
    
    st.info(f"Endee Search Latency: {latency:.2f} ms")
    
    if not results:
        st.write("No matches found. Try indexing some data first!")
    else:
        for i, res in enumerate(results):
            with st.expander(f"Result #{i+1} (Score: {res.get('score', 'N/A')})"):
                st.write(res.get('metadata', {}).get('text', 'No text found'))

st.divider()
st.caption("Built for Endee.io Internship-cum-Placement Opportunity 2026")
