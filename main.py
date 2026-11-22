from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title="DK Site", version="2.0.0")

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(Path("index.html").read_text(encoding="utf-8"))

@app.get("/api/health")
async def health():
    return {"ok": True, "app": "DK Site", "ai_mode": "on-device"}
