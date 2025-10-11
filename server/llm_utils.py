from langchain_openai import ChatOpenAI
import os

# ✅ 新增导入 RAG
RAG_AVAILABLE = False
try:
    from rag_service import rag_answer
    RAG_AVAILABLE = True
except Exception as e:
    print(f"⚠️ RAG 模块加载失败，将使用普通 LLM：{e}")


def get_chat_model():
    """统一创建 LLM 实例"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("缺少环境变量 DEEPSEEK_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
    model = os.getenv("OPENAI_MODEL", "deepseek-chat")
    return ChatOpenAI(api_key=api_key, base_url=base_url, model=model)


def llm(text: str):
    """同步调用：根据问题类型决定是否使用RAG"""
    chat_model = get_chat_model()
    
    # 先判断是否是需要使用RAG的知识库问题
    if RAG_AVAILABLE and _is_knowledge_question(text):
        try:
            prompt = rag_answer(text)  # 获取带上下文的prompt
            result = chat_model.invoke(prompt)
            return result.content
        except Exception as e:
            print(f"⚠️ RAG调用失败，回退到普通LLM：{e}")
    
    # 普通问题直接调用LLM
    result = chat_model.invoke(text)
    return result.content

def _is_knowledge_question(text: str) -> bool:
    """判断问题是否属于知识库范畴"""
    # 这里可以添加更复杂的逻辑，比如：
    # 1. 使用分类模型判断
    # 2. 检查问题中是否包含特定关键词
    # 3. 简单实现：检查问题是否包含"知识库"等关键词
    knowledge_keywords = ["知识库", "文档", "资料", "说明书"]
    return any(keyword in text for keyword in knowledge_keywords)

def llm_stream(text: str, subjectid: int):
    """流式调用：RAG 不支持流式（因需先检索完整上下文），故非流式返回"""
    if RAG_AVAILABLE:
        try:
            prompt = rag_answer(text)
            chat_model = get_chat_model()
            answer = chat_model.invoke(prompt).content

            yield str(subjectid)
            yield answer

            _save_to_db(subjectid, answer)
            return
        except Exception as e:
            print(f"⚠️ RAG 流式调用失败，回退到普通流式：{e}")

    # 回退到普通流式
    chat_model = get_chat_model()
    yield str(subjectid)
    content = ""
    for chunk in chat_model.stream(text):
        if chunk.content:
            content += chunk.content
            yield chunk.content

    _save_to_db(subjectid, content)


def _save_to_db(subjectid: int, content: str):
    try:
        from database import get_db_connection
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chatcontent (subjectid, content, role) VALUES (%s, %s, %s)",
                    (subjectid, content, "assistant")
                )
                conn.commit()
    except Exception as e:
        print(f"保存 AI 回复失败: {e}")