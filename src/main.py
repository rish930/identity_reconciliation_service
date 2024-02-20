from fastapi import FastAPI
from src.identify.router import router as identify_router
from src.db import Base, engine

app = FastAPI()


app.include_router(identify_router)

Base.metadata.create_all(engine)


@app.get("/")
def health_check():
    return "Identify Reconciliation Service is LIVE!!"
