import textwrap
from backend.constants import LINE_MAX_CHARACTERS
from backend.fastapi.core.config import Settings
from backend.fastapi.request_handler.api_requests import rollback_manager
from backend.utils.image import encode_image
from backend.line.operations import (
    get_or_create_user,
    create_message,
    prepare_memory_for_llm,
    llm_text_api_call,
    llm_image_api_call,
    load_animation,
    get_content
)
from linebot.v3.webhooks import MessageEvent
from linebot.v3.messaging import TextMessage, ReplyMessageRequest

async def handle_message_event_text(event: MessageEvent, settings: Settings):
    user_line_id = event.source.user_id
    user_input = event.message.text

    async with rollback_manager() as resources_to_rollback:
        # Step 1: User Handling
        user_id = await get_or_create_user(user_line_id, resources_to_rollback)

        # Optional: Animation
        _ = await load_animation(user_line_id)
        
        # Step 2: Call a LLM API
        memory = await prepare_memory_for_llm(user_id)
        llm_response = await llm_text_api_call(user_input, memory)

        # Step 3: Create a new message(User)
        new_user_message = await create_message(user_id, "user", user_input, resources_to_rollback)

        # Step 4: Create a new message(Server)
        new_server_message = await create_message(user_id, "server", llm_response, resources_to_rollback)

    # LINE has a character limit per message, so we need to split the response if necessary
    # response_chunks = textwrap.wrap(llm_response, LINE_MAX_CHARACTERS)
    # messages = [TextMessage(text=chunk) for chunk in response_chunks]

    await settings.LINE_BOT_API.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=llm_response)]
        )
    )

async def handle_message_event_image(event: MessageEvent, settings: Settings):
    user_line_id = event.source.user_id
    messageId = event.message.id

    async with rollback_manager() as resources_to_rollback:
        # Step 1: User Handling
        user_id = await get_or_create_user(user_line_id, resources_to_rollback)

        # Step 2: Fetch input image
        message_content = await get_content(messageId)

        # Optional: Animation
        _ = await load_animation(user_line_id)
        
        # Step 3: Call a LLM API(Image)
        llm_response = await llm_image_api_call(encode_image(message_content["content"]))

        # Step 4: Create a new message(User)
        new_user_message = await create_message(user_id, "user", f"messageId:{messageId}", resources_to_rollback)

        # Step 4: Create a new message(Server)
        new_server_message = await create_message(user_id, "server", llm_response, resources_to_rollback)
        
    # LINE has a character limit per message, so we need to split the response if necessary
    # response_chunks = textwrap.wrap(llm_response, LINE_MAX_CHARACTERS)
    # messages = [TextMessage(text=chunk) for chunk in response_chunks]

    await settings.LINE_BOT_API.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=llm_response)]
        )
    )
