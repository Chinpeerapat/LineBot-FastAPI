from fastapi import APIRouter, HTTPException, Header, Request
from backend.fastapi.core.init_settings import global_settings as settings
from backend.line.handlers.message_event import handle_message_event_text, handle_message_event_image
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
)

router = APIRouter(
    prefix="/webhooks",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}},
)

@router.post("/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body = body.decode()
    try:
        events = settings.parser.parse(body, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature.")
    
    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            await handle_message_event_text(event, settings)
        elif isinstance(event, MessageEvent) and isinstance(event.message, ImageMessageContent):
            await handle_message_event_image(event, settings)
        else:
            print(f"Unhandled event type: {type(event)}")

    return 'OK'