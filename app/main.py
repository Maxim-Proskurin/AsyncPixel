from fastapi import FastAPI
from app.api import task

import app.models
from app.api import auth, user

app = FastAPI(title="AsyncPixel")


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "AsyncPixel API is running!"}