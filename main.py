# main.py
from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI()

# Include your API routes
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
