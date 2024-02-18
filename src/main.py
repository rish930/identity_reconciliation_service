from fastapi import FastAPI
from src.identify.router import router as identify_router

app = FastAPI()


app.include_router(identify_router)