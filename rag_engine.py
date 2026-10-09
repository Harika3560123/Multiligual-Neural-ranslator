try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# =====================================================
# EMBEDDING MODEL
# =====================================================

try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # =====================================================
    # KNOWLEDGE BASE
    # =====================================================

    documents = [
        Document(page_content="Break a leg means good luck."),
        Document(page_content="Kick the bucket means someone died."),
        Document(page_content="Piece of cake means very easy."),
        Document(page_content="Spill the beans means reveal secret."),
        Document(page_content="Bite the bullet means face a difficult situation with courage."),
        Document(page_content="Under the weather means feeling sick or unwell."),
        Document(page_content="Once in a blue moon means very rarely."),
        Document(page_content="Cost an arm and a leg means very expensive.")
    ]

    # =====================================================
    # VECTOR DATABASE
    # =====================================================

    vector_db = FAISS.from_documents(
        documents,
        embedding_model
    )
except Exception as e:
    print(f"RAG Engine Initialization Warning: {e}")
    vector_db = None


# =====================================================
# RETRIEVE CONTEXT
# =====================================================

def retrieve_context(query):
    if not query or not query.strip() or vector_db is None:
        return ""

    try:
        docs = vector_db.similarity_search(
            query,
            k=2
        )
        context = "\n".join(
            [doc.page_content for doc in docs]
        )
        return context
    except Exception as e:
        print(f"Context Retrieval Error: {e}")
        return ""