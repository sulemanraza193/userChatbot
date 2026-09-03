from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import FRONTEND_URL
from .database import check_database

from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.chat import router as chat_router


app = FastAPI(
    title="AI User Management Chatbot",
    description="AI-powered user management API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    try:
        check_database()
    except Exception as error:
        print("MongoDB connection failed:", error)


@app.get("/api/health")
def health():

    return {
        "success": True,
        "message": "FastAPI server is running"
    }


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)