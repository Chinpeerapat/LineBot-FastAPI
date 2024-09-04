import os
from openai import AsyncOpenAI
from typing import List, Optional, Tuple
from backend.constants import OPENAI_LLM_ENDPOINT, TEMPERATURE
from llm.prompt.base_text_templates import TEXT_PROMPT_TEMPLATE_V1

async def llm_OpenAI_memory_chain(
        user_input: str,
        memory: Optional[List[Tuple[str, str]]] = None,
    ) -> str:

    client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Build the conversation history for the prompt
    messages = [{"role": "system", "content": TEXT_PROMPT_TEMPLATE_V1}]

    if memory:
        for message in memory:
            messages.append({"role": message[0], "content": message[1]})

    # Add the current user input to the conversation history
    messages.append({"role": "user", "content": user_input})

    # Make the API call to OpenAI's chat completion endpoint
    chat_completion = await client.chat.completions.create(
        model=OPENAI_LLM_ENDPOINT,
        messages=messages,
        temperature=TEMPERATURE,
    )

    # Extract and return the llm's response
    llm_response = chat_completion.choices[0].message.content
    return llm_response