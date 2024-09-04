from backend.fastapi.core.init_settings import global_settings as settings

LINE_MAX_CHARACTERS = 3000
MEMORY_WINDOW_SIZE=3
TEMPERATURE=0.5
OPENAI_LLM_ENDPOINT="gpt-4o-mini"
API_BASE_URL_SYNC =settings.API_BASE_URL_SYNC
API_BASE_URL_ASYNC =settings.API_BASE_URL_ASYNC