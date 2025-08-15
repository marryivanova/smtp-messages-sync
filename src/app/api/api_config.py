from dotenv import load_dotenv
from os.path import join, dirname

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.helpers.static_content import description, title

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = FastAPI(
    title=title,
    description=description,
    version="0.1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)