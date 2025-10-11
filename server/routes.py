from fastapi import APIRouter, UploadFile, HTTPException,Query 
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
import mimetypes
import os
from uuid import uuid4

from database import get_db_connection
from llm_utils import llm_stream, llm

router = APIRouter()


# 内部工具：保存上传文件并返回 URL
async def _save_upload(img1: UploadFile) -> JSONResponse:
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    allowed = {"image/png", "image/jpeg", "image/webp", "application/pdf", "application/zip",
               "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
    if img1.content_type and img1.content_type not in allowed:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    suffix = Path(img1.filename).suffix or ""
    safe_name = f"{uuid4().hex}{suffix}"
    dst = static_dir / safe_name
    content = await img1.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件过大，超过10MB")
    with open(dst, "wb") as f:
        f.write(content)
    return JSONResponse({"img": f"/static/{safe_name}"}, status_code=200, headers={"Cache-Control": "no-store"})


# 测试路由
@router.get("/test1")
def test1():
    return {"message": "Hello, World!"}


# 测试路由，测试参数
@router.get("/test2")
def test2(count: int, chat_text: str):
    return {"count": count, "chat_text": chat_text}


# 定义模型
class Mydata(BaseModel):
    count: str
    chat_text: str


# 测试路由，测试参数
@router.post("/test3")
def test3(data: Mydata):
    return {"data": data}


# 上传文件
@router.post("/upload")
async def upload_lower(img1: UploadFile):
    try:
        return await _save_upload(img1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {e}")


# 简单聊天
@router.get("/chat")
def chat(text: str):
    try:
        ai_content = llm(text)
        return {"code": 2000, "content": ai_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")


# 提取主题（去除非文本字符）
def extract_clean_title(raw_title: str) -> str:
    """清理 LLM 返回的主题，只保留纯文本"""
    return raw_title.strip().strip('\"\'').replace('\n', '').replace('\r', '')[:100]


# 流式对话
@router.get("/stream")
def stream(text: str, subjectid: int):
    try:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # 如果是新对话，创建主题
                    if subjectid == 0:
                        raw_title = llm(f"用户的对话内容是:{text},请帮我生成一个对话主题,只返回主题文字")
                        title = extract_clean_title(raw_title)

                        # 插入主题
                        insert_subject_sql = "INSERT INTO subject (title) VALUES (%s)"
                        cursor.execute(insert_subject_sql, (title,))
                        subjectid = cursor.lastrowid

                        # 保存用户消息（事务内）
                        insert_chat_sql = "INSERT INTO chatcontent (subjectid, content, role) VALUES (%s, %s, %s)"
                        cursor.execute(insert_chat_sql, (subjectid, text, "user"))

                        conn.commit()  # 提交事务

                    else:
                        # 已有主题，仅保存用户消息
                        insert_chat_sql = "INSERT INTO chatcontent (subjectid, content, role) VALUES (%s, %s, %s)"
                        cursor.execute(insert_chat_sql, (subjectid, text, "user"))
                        conn.commit()
        except Exception as db_err:
            # 不中断流式对话，记录错误并继续
            print(f"用户消息入库失败: {db_err}")

        # 流式返回 AI 回复（llm_stream 内部会保存 AI 回复）
        return StreamingResponse(
            llm_stream(text, subjectid),
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流式对话失败: {e}")


# 获取主题
@router.get("/get_subject")
def get_subject():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, title, created_at FROM subject ORDER BY created_at DESC"
                cursor.execute(sql)
                return cursor.fetchall()
    except Exception as e:
        # 回退逻辑：兼容历史表结构缺少 created_at 的情况
        print(f"获取主题失败（将启用回退查询）：{e}")
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, title FROM subject ORDER BY id DESC")
                    rows = cursor.fetchall()
                    # 补齐 created_at 字段，避免前端取值报错
                    for r in rows:
                        if "created_at" not in r:
                            r["created_at"] = None
                    return rows
        except Exception as e2:
            raise HTTPException(status_code=500, detail=f"获取主题失败: {e2}")


# 获取主题下的聊天记录
@router.get("/get_chatcontent_at_subjectid")
def get_chatcontent_at_subjectid(subjectid: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # 使用参数化查询防止注入
                sql = "SELECT * FROM chatcontent WHERE subjectid = %s ORDER BY id LIMIT 20"
                cursor.execute(sql, (subjectid,))
                return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天记录失败: {e}")


# 删除主题（兼容未启用 ON DELETE CASCADE 的环境）
@router.delete("/subject/{subject_id}")
def delete_subject(subject_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # 先删除子表，避免 1451 外键约束错误
                cursor.execute("DELETE FROM chatcontent WHERE subjectid = %s", (subject_id,))
                # 再删除父表
                cursor.execute("DELETE FROM subject WHERE id = %s", (subject_id,))
                conn.commit()
                return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除主题失败: {e}")
    
@router.get("/rag_query")
def rag_query_route(question: str = Query(..., description="用户问题")):
    """
    RAG问答接口
    前端调用示例: /rag_query?question=合同无效的情形有哪些
    """
    try:
        answer = rag_answer(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}