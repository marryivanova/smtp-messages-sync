import os
import uvicorn
from dotenv import load_dotenv
from os.path import join, dirname

from src.app.api.api_config import app
from src.app.api.discount import router_discount
from src.app.api.smtp import router
from src.app.api.user import router_users

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


app.include_router(router)
app.include_router(router_users)
app.include_router(router_discount)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(os.getenv("APP_HOST")),
        port=int(os.getenv("APP_PORT")),
        reload=bool(os.getenv("APP_DEBUG")),
        log_level="debug" if os.getenv("APP_DEBUG") else "info",
    )
