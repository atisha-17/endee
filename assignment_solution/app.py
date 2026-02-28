import streamlit as st
from engine import EndeeEngine

st.set_page_config(page_title="Endee AI Agent", page_icon="⚡")
st.title("⚡ Endee High-Performance Research Agent")

engine = EndeeEngine()
engine.prepare_index()

# Sidebar for Ingestion
with st.sidebar:
    st.header("Ingest Data")
    doc_input = st.text_area("Paste Research Text here:")
    if st.button("Index Document"):
        latency = engine.add_document(doc_input, {"source": "manual_entry"})
        st.success(f"Indexed in {latency*1000:.2f}ms")

# Main Search Area
query = st.text_input("Ask the Research Agent:")
if query:
    results, latency = engine.search(query)
    st.info(f"Endee Search Latency: {latency:.2f} ms")
    
    for res in results:
        st.write(f"📄 **Match:** {res['metadata']['text'][:200]}...")
        st.write(f"Score: `{res['score']}`")
        st.divider()
