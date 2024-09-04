import os
import httpx
from typing import List, Tuple
from backend.fastapi.request_handler.api_requests import post_request, get_request
from backend.constants import MEMORY_WINDOW_SIZE
from llm.memory.memory_management import format_memory

async def create_message(user_id: str, message_type: str, user_input: str, resources_to_rollback: List[tuple]) -> dict:
    message_data = {
        "content": user_input,
        "message_type": message_type,
        "user_id": user_id,
    }
    new_message = await post_request("messages/", message_data)
    resources_to_rollback.append(("create", "messages", {"resource_id": new_message["id"]}))

    return new_message

async def prepare_memory_for_llm(user_id: str, window_size: int = MEMORY_WINDOW_SIZE) -> List[Tuple[str, str]]:
    latest_messages = await get_request("messages/latest/", params={"user_id": user_id, "n": window_size})
    return format_memory(latest_messages)

async def load_animation(user_line_id: str) -> dict:
    url = f"https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        'Authorization': f'Bearer {os.getenv("LINE_CHANNEL_ACCESS_TOKEN")}'
    }
    data = {
        "chatId": user_line_id,
        "loadingSeconds": 30
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
async def get_content(messageId: str) -> dict:
    url = f"https://api-data.line.me/v2/bot/message/{messageId}/content"
    headers = {
        'Authorization': f'Bearer {os.getenv("LINE_CHANNEL_ACCESS_TOKEN")}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

        # Check if the content is JSON
        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            # Handle non-JSON content, e.g., save to a file or process as needed
            return {"content": response.content, "content_type": response.headers.get("Content-Type")}