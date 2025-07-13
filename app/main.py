from fastapi import FastAPI

app = FastAPI(title="AsyncPixel")

@app.get("/")
async def root():
    return {"message": "Да прибудет AsyncPixel API!"}
