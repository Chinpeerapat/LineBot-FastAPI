import httpx
from contextlib import asynccontextmanager
from urllib.parse import urljoin
from backend.constants import API_BASE_URL_SYNC
from typing import Any, Dict, List, Tuple, Optional, AsyncGenerator

@asynccontextmanager
async def rollback_manager() -> AsyncGenerator[List[Tuple[str, str, dict]], None]:
    resources_to_rollback: List[Tuple[str, str, dict]] = []
    try:
        yield resources_to_rollback
    except Exception as e:
        async with httpx.AsyncClient() as client:
            for http_method, resource_type, resource_data in reversed(resources_to_rollback):
                resource_url = urljoin(API_BASE_URL_SYNC, f"{resource_type}/{resource_data['resource_id']}")
                if http_method == "update":
                    # Restore the previous state of the resource
                    await post_request(client, resource_url, resource_data['previous_state'])
                elif http_method == "create":
                    # Default behavior for created resources: delete the resource
                    await client.delete(resource_url)
                # Additional handling can be added here for different resource types or methods
        raise e
    
async def post_request(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.post(urljoin(API_BASE_URL_SYNC, endpoint), json=data)
        response.raise_for_status()
        return response.json()

async def get_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(urljoin(API_BASE_URL_SYNC, endpoint), params=params)
        response.raise_for_status()
        return response.json()

async def put_request(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.put(urljoin(API_BASE_URL_SYNC, endpoint), json=data)
        response.raise_for_status()
        return response.json()