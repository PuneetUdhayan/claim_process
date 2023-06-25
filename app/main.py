import os

from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

from app.database import Base, engine
from app.dependencies import get_identifier
from app.claimprocess.router import router as ClaimsRouter
from app.providers.router import router as ProvidersRouter

app = FastAPI(title="Claim Process", version="0.1.1")


@app.on_event("startup")
async def startup():
    r = redis.from_url(
        f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r,identifier=get_identifier)


Base.metadata.create_all(engine)

app.include_router(ClaimsRouter)
app.include_router(ProvidersRouter)


@app.get("/")
async def root():
    return {"message": "Claim Processing is up"}
