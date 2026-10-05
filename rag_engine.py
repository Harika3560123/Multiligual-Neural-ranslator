from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document


# =====================================================
# EMBEDDING MODEL
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =====================================================
# KNOWLEDGE BASE
# =====================================================

documents = [

    Document(
        page_content="Break a leg means good luck."
    ),

    Document(
        page_content="Kick the bucket means someone died."
    ),

    Document(
        page_content="Piece of cake means very easy."
    ),

    Document(
        page_content="Spill the beans means reveal secret."
    )

]


# =====================================================
# VECTOR DATABASE
# =====================================================

vector_db = FAISS.from_documents(
    documents,
    embedding_model
)


# =====================================================
# RETRIEVE CONTEXT
# =====================================================

def retrieve_context(query):

    docs = vector_db.similarity_search(
        query,
        k=2
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    return context