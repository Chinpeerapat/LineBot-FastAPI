from llm.chain.llm_text_chain import llm_OpenAI_memory_chain
from llm.chain.llm_image_chain import send_image_openai

async def llm_text_api_call(user_input: str, memory: list) -> str:
    try:
        llm_response = await llm_OpenAI_memory_chain(user_input, memory)
        return llm_response
    except Exception as e:
        raise RuntimeError(f"Failed to process LLM response: {str(e)}")
    
async def llm_image_api_call(base64_image: str) -> str:
    try:
        llm_response = await send_image_openai(base64_image)
        return llm_response
    except Exception as e:
        raise RuntimeError(f"Failed to process LLM response: {str(e)}")