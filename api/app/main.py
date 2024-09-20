from fastapi import FastAPI
from .routes import router
import os

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
