from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Depends

from app.database import Base, engine
from app.claimprocess.router import router as ClaimsRouter
from app.providers.router import router as ProvidersRouter

app = FastAPI(title="Claim Process", version="0.1.1")

Base.metadata.create_all(engine)

app.include_router(ClaimsRouter)
app.include_router(ProvidersRouter)


@app.get("/")
async def root():
    return {"message": "Claim Processing is up"}
