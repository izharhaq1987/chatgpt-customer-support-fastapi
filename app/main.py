from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import tickets

app = FastAPI(
    title = "ChatGPT Customer Support – Mock Zendesk Flow",
    version = "0.1.0"
)

@app.get("/")
def index():
    return JSONResponse({"message": "Mock Zendesk ticket flow API running."})

app.include_router(tickets.router)
