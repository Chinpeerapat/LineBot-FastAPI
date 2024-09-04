import os
import httpx
from openai import AsyncOpenAI
from backend.constants import OPENAI_LLM_ENDPOINT
from llm.prompt.base_text_templates import VISION_PROMPT_TEMPLATE_V1

async def llm_OpenAI_vision_chain(
        image_url: str
    ) -> str:

    client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Build the conversation history for the prompt
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_PROMPT_TEMPLATE_V1},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    },
                },
            ]
        }
    ]

    # Make the API call to OpenAI's chat completion endpoint
    chat_completion = await client.chat.completions.create(
        model=OPENAI_LLM_ENDPOINT,
        messages=messages
    )

    # Extract and return the llm's response
    llm_response = chat_completion.choices[0].message.content
    return llm_response

async def send_image_openai(base64_image: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": VISION_PROMPT_TEMPLATE_V1
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Ensure the request was successful
        chat_completion = response.json()
        llm_response = chat_completion["choices"][0]["message"]["content"]
        return llm_response