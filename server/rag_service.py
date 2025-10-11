# rag_service.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "./FlagEmbedding"  # 嵌入模型
VECTOR_STORE_PATH = "./rag/server/db"

# 全局缓存向量库
_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        print("🔹 正在加载向量数据库...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ 向量数据库加载完成！")
    return _vector_store

def rag_answer(query: str) -> str:
    """仅检索相关文档，返回拼接后的上下文（由外部 LLM 生成答案）"""
    db = get_vector_store()
    docs = db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    # 返回提示词模板，供外部 LLM 使用
    prompt = (
        f"请根据以下法律资料回答问题。如果资料中没有相关信息，请回答“根据现有资料无法回答”。\n\n"
        f"资料：\n{context}\n\n"
        f"问题：{query}\n\n"
        f"回答："
    )
    return prompt