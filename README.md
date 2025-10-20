# LawMind - 您的智能法律咨询助手 ⚖️🤖

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-purple.svg)](https://www.langchain.com/)
[![UI](https://img.shields.io/badge/UI-Streamlit-orange.svg)](https://streamlit.io/)

`LawMind` 是一个基于大语言模型（LLM）和本地法律知识库的垂直领域智能问答项目。它旨在为用户提供专业、高效、便捷的法律咨询服务，帮助用户快速理解法律问题并获得初步的建议。

## ✨ 主要功能

- **专注法律领域**：内置专业的法律知识文档，回答更具针对性和准确性。
- **知识库驱动**：采用检索增强生成（RAG）技术，结合本地知识库进行问答，有效减少模型幻觉。
- **双模型支持**：支持接入多种大语言模型，如 OpenAI 的 GPT 系列和本地部署的 ChatGLM 等。
- **友好交互界面**：基于 Streamlit 构建，提供简洁直观的 Web 用户界面。
- **易于扩展**：可以轻松地在 `data` 目录中添加、修改或删除你自己的法律知识文档。

## 📸 项目演示

![LawMind UI](images/law-mind-ui.png)

## 🛠️ 技术架构

本项目采用检索增强生成（RAG）方案，其工作流程如下：

1.  **数据预处理**：加载 `data` 目录下的法律知识文档，并使用文本分割器进行处理。
2.  **向量化**：使用 `flagembedding``Sentence-Transformers` 等嵌入模型将文本块转换为向量。
3.  **存入向量库**：将生成的向量存储在 `FAISS` 向量数据库中，并进行持久化。
4.  **用户提问**：用户通过 Uniapp 界面输入问题。
5.  **向量检索**：将用户的问题向量化，在 FAISS 向量库中检索最相关的文本块。
6.  **构建提示词**：将检索到的相关文本和用户问题整合成一个精确的提示词（Prompt）。
7.  **调用大模型**：将构建好的提示词发送给大语言模型（如 Qwen3 或 deepseek OpenAI GPT）。
8.  **生成并返回答案**：大模型根据提示词生成回答，并通过界面展示给用户。

## 📚 技术栈

- **Web 框架**: Uniapp
- **LLM 应用框架**: LangChain
- **大语言模型 (LLM)**: deepseek API, Qwen3 (及其他 Transformers 支持的模型)
- **向量嵌入 (Embedding)**: `flagembedding`
- **向量数据库**: FAISS
- **核心库**: `torch`, `transformers`

## 🚀 快速开始

请按照以下步骤在本地运行本项目。

### 1. 克隆项目

```bash
git clone https://github.com/wieldsickle/LawMind.git
cd LawMind
```

### 2. 创建虚拟环境并安装依赖

建议使用虚拟环境以避免包版本冲突。

```bash
# 创建虚拟环境 (Python 3.9+)
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装所有依赖项
pip install -r requirements.txt
```

### 3. 配置模型

本项目支持多种模型，请根据需要选择并配置。

- **使用 deepseek 模型**:
  在项目根目录下创建一个 `.env` 文件，并填入你的I API Key。
  ```
  DEEPSEEK_API_KEY="sk-YourApiKey"
  ```


- **使用本地 Qwen3 模型**:
  1.  从 Huggingface 或 modelscope 下载 Qwen3 或其他模型的权重文件。
  2.  打开 `src/main.py` 文件，修改 `LLM_MODEL` 变量为 `"Qwen3"`，并确保 `MODEL_PATH` 变量指向你下载的模型权重路径。

### 4. 创建知识库向量索引

在首次运行前，你需要将 `data` 目录下的文档加载到向量数据库中。

```bash
# 运行脚本来创建和持久化向量数据库
# （请确保你的模型路径和嵌入模型配置正确）
python src/vector_db/vector_db.py 
```
该脚本会读取 `data` 目录下的所有 `.md` 文件，生成向量索引并保存在 `vector_db/faiss_index` 目录下。

### 5. 启动应用

一切准备就绪后，运行以下命令启动 Streamlit Web 应用。

```bash
streamlit run src/main.py
```

现在，在浏览器中打开显示的 URL (通常是 `http://localhost:8501`)，即可开始与 LawMind 互动。

## 📁 项目结构

```
LawMind/
├── data/                 # 存放原始法律知识文档 (.md)
├── images/               # 存放项目截图
├── src/                  # 核心源代码
│   ├── main.py           # Streamlit 应用主入口
│   ├── models/           # 大语言模型封装 (chatglm.py, openai.py)
│   ├── prompt/           # 提示词模板
│   └── vector_db/        # 向量数据库相关脚本 (vector_db.py)
├── .gitignore            # Git 忽略文件配置
├── LICENSE               # 项目许可证 (Apache 2.0)
└── requirements.txt      # Python 依赖包列表
```

## 🤝 如何贡献

欢迎对本项目做出贡献！你可以通过以下方式参与：

-   提交 Bug 报告或功能建议到 [Issues](https://github.com/wieldsickle/LawMind/issues)。
-   通过 [Pull Requests](https://github.com/wieldsickle/LawMind/pulls) 提交你的代码。
-   完善和补充 `data` 目录下的法律知识库。

在提交代码前，请确保你的代码风格与项目保持一致。
