from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import faiss
import json
import os

# 文件路径
PROJECT_PATH = 'F:/Law_llm/rag'
MODEL_PATH = './FlagEmbedding'
TEXT_PATH = "F:/Law_llm/法律领域语料库.json"


model = HuggingFaceEmbeddings(model_name=MODEL_PATH)
# 读取json文件
# 2. 读取 JSONL 文件（每行一个 JSON）
data = []
with open(TEXT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"跳过一行解析失败：{e}")

print(f"共读取 {len(data)} 条记录")
# documents = [line["text"] for line in data["lines"]]
documents = []
for item in data:
    text = item.get("text") or item.get("content") or item.get("contentText")
    if text:
        documents.append(Document(page_content=text))
    else:
        print(f"跳过一条没有文本字段的数据：{item}")

print(f"成功解析 {len(documents)} 条文本")

# 初始化FAISS索引
vector_store = FAISS.from_documents(documents, model)



# 保存索引
faiss_path = os.path.join(PROJECT_PATH, "server", "db")
vector_store.save_local(faiss_path)



