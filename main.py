import os
import settings
import uuid
from zeroconf_service import register_zeroconf, unregister_zeroconf
from loguru import logger

import uvicorn
from fastapi import FastAPI, File, UploadFile
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


# Ping API

@app.get("/ping")
async def ping():
    return "OK", 200

# Upload File API


@app.post('/upload')
async def upload_file(
    file: UploadFile = File(...)
):
    file_location = f"uploads/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        logger.info(f"Uploaded file saved at {file_location}")
    return {"success": True}

# Zeroconf
register_zeroconf()


@app.on_event("shutdown")
def shutdown_event():
    unregister_zeroconf()


# Uploads Dirs
if not os.path.exists('uploads'):
    os.mkdir('uploads')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
