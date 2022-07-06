import uvicorn
import os

from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        ssl_keyfile="./certs/private.key",
        ssl_certfile="./certs/CA.crt",
        lifespan="on",
    )
