import streamlit as st
from pathlib import Path

from src.document_processor import load_documents
from src.retrieval import DocumentRetriever
from src.rag import generate_answer


st.set_page_config(
    page_title="CampusSathi",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CampusSathi")
st.subheader("AI Student Support & Opportunity Navigator")

# -------------------------
# FILE UPLOAD SECTION
# -------------------------

uploaded_files = st.file_uploader(
    "📄 Upload Scholarship / Policy Documents",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:

    save_folder = Path("data/documents")
    save_folder.mkdir(parents=True, exist_ok=True)

    for uploaded_file in uploaded_files:

        file_path = save_folder / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success("✅ Files uploaded successfully!")

# -------------------------
# APP DESCRIPTION
# -------------------------

st.write(
    "Ask questions about scholarships, university policies, "
    "eligibility, deadlines, and required documents."
)

# -------------------------
# LOAD DOCUMENTS
# -------------------------

documents = load_documents()

if documents:

    retriever = DocumentRetriever(documents)

    question = st.text_input(
        "Ask CampusSathi anything:"
    )

    if question:

        with st.spinner(
            "🔎 Searching documents and generating answer..."
        ):

            results = retriever.search(
                question,
                top_k=3
            )

            answer = generate_answer(
                question,
                results
            )

        # -------------------------
        # ANSWER
        # -------------------------

        st.subheader("🤖 CampusSathi Answer")
        st.write(answer)

        # -------------------------
        # CHECKLIST
        # -------------------------

        st.subheader("📋 Application Checklist")

        checklist_items = [
            "CNIC/B-Form",
            "Transcript",
            "Enrollment Certificate",
            "Income Certificate",
            "Recommendation Letter"
        ]

        for item in checklist_items:
            st.checkbox(item, key=item)

        # -------------------------
        # EVIDENCE
        # -------------------------

        st.subheader("📚 Sources & Evidence")

        for result in results:

            st.write(
                f"**Source:** {result['source']}"
            )

            st.write(
                f"**Relevance Score:** {result['score']:.2f}"
            )

            with st.expander("View evidence used"):

                st.write(
                    result["text"]
                )

else:

    st.warning(
        "No documents found. Please upload documents or add them to "
        "data/documents."
    )