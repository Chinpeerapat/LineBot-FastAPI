import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from backend.fastapi.core.init_settings import args, global_settings as settings
from backend.fastapi.api.v1.endpoints import base, doc, line, message, user
from backend.fastapi.dependencies.database import init_db, AsyncSessionLocal
from backend.fastapi.request_handler.api_requests import rollback_manager
from backend.line.operations.user import get_or_create_user
from linebot.v3 import WebhookHandler
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi
)

# Run before initiate the FastAPI App.
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize the database connection
    init_db()

    # Initialize the LINE Messaging API
    settings.parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
    settings.LINE_BOT_API = AsyncMessagingApi(AsyncApiClient(settings.LINE_CONFIGURATION))

    yield

# Initiate a FastAPI App.
app = FastAPI(lifespan=lifespan)

# Frontend
templates = Jinja2Templates(directory="frontend/login/templates")
app.mount("/static", StaticFiles(directory="frontend/login/static"), name="static")

# Set Middleware
# Define the allowed origins
origins = [
    settings.API_BASE_URL,
    "http://localhost",
    "http://localhost:5000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Document protection middleware
@app.middleware("http")
async def add_doc_protect(request: Request, call_next):
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        if not request.session.get('authenticated'):
            return RedirectResponse(url="/login")
    response = await call_next(request)
    return response
# Add session middleware with a custom expiration time (e.g., 30 minutes)
app.add_middleware(SessionMiddleware, 
                   secret_key="your_secret_key", 
                   max_age=18000)  # 18000 seconds = 300 minutes

# Add the routers to the FastAPI app
app.include_router(base.router, prefix="", tags=["main"])
app.include_router(doc.router, prefix="", tags=["doc"])
app.include_router(message.router, prefix="/api/v1", tags=["message"])
app.include_router(user.router_sync, prefix="/api/v1", tags=["user"])
app.include_router(line.router)

if __name__ == "__main__":
    # mounting at the root path
    uvicorn.run(
        app="backend.fastapi.main:app",
        host = args.host,
        port=int(os.getenv("PORT", 5000)),
        reload=args.mode == "dev"  # Enables auto-reloading in development mode
    )