# server.py
from fastmcp import FastMCP
from typing import Union, List
from pydantic import Field
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Create an MCP server
mcp = FastMCP("AsyncAction", host="0.0.0.0", port=9999)


async def async_action(topics: Union[List[str], str], message: str, system_args: dict) -> str:
    """模拟异步操作, 例如向设备发送消息"""
    client_id = system_args.get("client_id", "unknown_client")
    await asyncio.sleep(10)  # 模拟异步延迟
    logger.info(f"Sent Message '{message}' to client:{client_id} on topic:{topics} successfully.")


@mcp.tool(exclude_args=["system_args"])
async def send_message(
    topics: Union[List[str], str] = Field(description="目标话题"),
    message: str = Field(description="str 要发送的消息内容"),
    system_args: dict = Field(default_factory=dict ,description="服务器参数, 必带且需要被exclude_args排除, 由服务器自动传入")
) -> str:
    """
    向客户端异步发送主题/消息
    """
    # asyncio.run_coroutine_threadsafe(async_action(topics, message, system_args), loop) # 在子线程事件循环中运行协程
    loop = asyncio.get_event_loop()
    loop.create_task(async_action(topics, message, system_args))  # 在当前事件循环中运行协程
    return "Message is being sent asynchronously."


@mcp.tool()
def get_topics():
    """
    返回支持发布的主题
    """
    topics = ["A", "B", "C", "D"]
    return f"Topics: {', '.join(topics)}"


# Start the server
if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except Exception as e:
        logger.info(f"Server error: {e}")
