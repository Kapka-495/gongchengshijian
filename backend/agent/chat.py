"""
AI Chat 接口
提供 /ai/chat 对话接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

import tomli

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .rag import retrieve, format_retrieved_context, init_knowledge_base
from .prompts import SYSTEM_PROMPT, RAG_QUERY_TEMPLATE

router = APIRouter(tags=["AI Agent"])


# ========== 配置加载 ==========
def load_agent_config():
    """从 config.toml 加载配置"""
    config_file = Path(__file__).resolve().parent.parent / "config" / "config.toml"
    if config_file.exists():
        with open(config_file, "rb") as f:
            return tomli.load(f)
    return {}


# 加载配置
_config = load_agent_config()
_agent_config = _config.get("agent", {})
_rag_config = _config.get("rag", {})

# LLM 配置
LLM_CONFIG = {
    "model": _agent_config.get("llm_model", "gpt-3.5-turbo"),
    "temperature": _agent_config.get("llm_temperature", 0.7),
    "max_tokens": _agent_config.get("llm_max_tokens", 1000),
    "api_key": _agent_config.get("api_key", ""),
    "base_url": _agent_config.get("base_url", ""),
}

# RAG 配置
RAG_CONFIG = {
    "top_k": _rag_config.get("top_k", 5),
    "max_history": _rag_config.get("max_history", 10),
}

# 全局 LLM 实例
_llm = None


def get_llm():
    """获取 LLM 实例（单例）"""
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=LLM_CONFIG["model"],
            temperature=LLM_CONFIG["temperature"],
            max_tokens=LLM_CONFIG["max_tokens"],
            api_key=LLM_CONFIG["api_key"],
            base_url=LLM_CONFIG["base_url"] if LLM_CONFIG["base_url"] else None,
        )
    return _llm


# ========== 请求/响应模型 ==========

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    reply: str
    actions: List[str] = []
    timestamp: str


# ========== 路由 ==========

@router.post("/ai/chat")
async def chat(request: ChatRequest):
    """
    AI 对话接口
    接收用户消息，检索知识库，调用 LLM 生成回答
    """
    try:
        # 1. 初始化知识库（首次调用时）
        try:
            init_knowledge_base()
        except Exception as e:
            print(f"知识库初始化跳过: {e}")

        # 2. RAG 检索
        retrieved = retrieve(request.message, top_k=RAG_CONFIG["top_k"])
        context = format_retrieved_context(retrieved)

        # 3. 构造 Prompt
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_msg = SYSTEM_PROMPT.format(current_time=current_time)

        # 4. 构建消息列表
        messages = [SystemMessage(content=system_msg)]

        # 5. 添加历史对话（截断）
        if request.history:
            for msg in request.history[-RAG_CONFIG["max_history"]:]:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                else:
                    messages.append(SystemMessage(content=msg.content))

        # 6. 添加当前问题（RAG增强）
        rag_prompt = RAG_QUERY_TEMPLATE.format(
            question=request.message,
            retrieved_context=context
        )
        messages.append(HumanMessage(content=rag_prompt))

        # 7. 调用 LLM
        llm = get_llm()
        response = llm.invoke(messages)

        # 8. 解析响应
        reply = response.content if hasattr(response, "content") else str(response)

        # 9. 返回结果
        return {
            "code": 200,
            "msg": None,
            "data": {
                "reply": reply,
                "actions": [],  # 暂时为空，后续可扩展
                "timestamp": datetime.now().isoformat()
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话处理失败: {str(e)}")


@router.get("/ai/health")
async def health_check():
    """
    Agent 健康检查
    用于测试 LLM 连接是否正常
    """
    try:
        llm = get_llm()
        # 发送一个简单测试
        test_response = llm.invoke([HumanMessage(content="你好，请回复'健康'")])
        return {
            "code": 200,
            "msg": None,
            "data": {
                "status": "ok",
                "llm_model": LLM_CONFIG["model"],
                "test_response": test_response.content if hasattr(test_response, "content") else "ok"
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "msg": None,
            "data": {
                "status": "error",
                "error": str(e)
            }
        }