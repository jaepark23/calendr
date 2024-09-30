from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import routes

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


