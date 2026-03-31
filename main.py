import os
import uvicorn
from fastapi import FastAPI
from api import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    print("Welcome to the test cases generator")

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
