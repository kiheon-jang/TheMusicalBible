from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import generation, suno_manual

app = FastAPI(title="The Musical Bible Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation.router, prefix="/api", tags=["generation"])
app.include_router(suno_manual.router, prefix="/api/manual", tags=["manual"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
