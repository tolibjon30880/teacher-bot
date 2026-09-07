from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import teacher, student


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Teacher Bot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # mini app domenini productionda cheklang
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teacher.router)
app.include_router(student.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
