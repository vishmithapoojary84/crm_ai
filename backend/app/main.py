from fastapi import FastAPI

from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.core.logger import logger

from app.api import hcp, interaction, chat

def init_db():
    Base.metadata.create_all(bind=engine)
    
app = FastAPI(title="AI First CRM")
init_db()
logger.info("Application started. Database initialized.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hcp.router, prefix="/api/v1")
app.include_router(interaction.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "AI First CRM Backend Running"
    }

app.include_router(
    hcp.router,
    prefix="/api/hcps"
)

app.include_router(
    interaction.router,
    prefix="/api/interactions"
)

app.include_router(
    chat.router,
    prefix="/api/chat"
)