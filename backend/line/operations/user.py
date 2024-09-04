import os
from typing import List, Tuple
import httpx
from backend.fastapi.request_handler.api_requests import post_request, get_request

async def get_or_create_user(user_line_id: str, resources_to_rollback: List[Tuple[str, str, dict]]) -> str:
    user_data = {"line_id": user_line_id}
    try:
        user = await get_request("user/", params=user_data)
        return user["id"]
    except httpx.HTTPStatusError as e:
        # User does not exist
        if e.response.status_code == 404:
            # Get User Line Profile
            user_profile = await get_line_user_profile(user_line_id)
            user_data = {
                "line_id": user_line_id,
                "user_name": user_profile.get("displayName", ""), 
                "pictureUrl": user_profile.get("pictureUrl", ""),
                "statusMessage": user_profile.get("statusMessage", "") 
            }
            new_user = await post_request("users/", user_data)
            resources_to_rollback.append(("create", "users", {"resource_id": new_user["id"]}))
            return new_user["id"]
        else:
            raise e

async def get_line_user_profile(user_line_id: str) -> dict:
    url = f"https://api.line.me/v2/bot/profile/{user_line_id}"
    headers = {
        'Authorization': f'Bearer {os.getenv("LINE_CHANNEL_ACCESS_TOKEN")}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
