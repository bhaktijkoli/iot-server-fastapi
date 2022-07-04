import os
import settings
import uuid
from zeroconf_service import register_zeroconf, unregister_zeroconf
from loguru import logger

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

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


# Ping API


@app.get("/ping")
async def ping():
    return "OK", 200


# Upload File API


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_location = f"uploads/{file_name}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        logger.info(f"Uploaded file saved at {file_location}")
    return {"success": True, "file": file_name}


# Get Upload File API
@app.get("/uploads/{file_id}")
async def read_item(file_id):
    file_location = f"uploads/{file_id}"
    if os.path.exists(file_location):
        return FileResponse(file_location)
    else:
        raise HTTPException(status_code=404, detail="File not found")


# Zeroconf
register_zeroconf()


@app.on_event("shutdown")
def shutdown_event():
    unregister_zeroconf()


# Uploads Dirs
if not os.path.exists("uploads"):
    os.mkdir("uploads")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        ssl_keyfile="./certs/private.key",
        ssl_certfile="./certs/CA.crt",
    )
