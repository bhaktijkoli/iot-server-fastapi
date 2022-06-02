import os
import settings
from loguru import logger

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def blockPrint():
    sys.stdout = open(os.devnull, "w")


@app.get("/ping")
async def ping():
    return "OK", 200


@app.post("/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    logger.debug(token)
    if len(token) <= 0:
        raise HTTPException(status_code=404, detail="Token not found")

    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


if os.environ.get("LOGS", "1") != "1":
    print("blocked")
    blockPrint()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
