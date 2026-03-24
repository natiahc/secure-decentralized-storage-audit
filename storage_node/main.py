import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(
    title="Secure Storage Node",
    version="1.0.0"
)

NODE_ID = os.getenv("NODE_ID", "node-unknown")
NODE_NAME = os.getenv("NODE_NAME", "storage-node")
NODE_REGION = os.getenv("NODE_REGION", "unknown")
STORAGE_PATH = os.getenv("STORAGE_PATH", "/data/node_storage")

storage_dir = Path(STORAGE_PATH)
storage_dir.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Storage node is running",
        "node_id": NODE_ID,
        "node_name": NODE_NAME,
        "region": NODE_REGION,
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "storage_node",
        "node_id": NODE_ID,
        "node_name": NODE_NAME,
        "region": NODE_REGION,
    }


@app.post("/store")
async def store_file(object_path: str, file: UploadFile = File(...)):
    target_path = storage_dir / object_path

    target_path.parent.mkdir(parents=True, exist_ok=True)

    content = await file.read()

    with open(target_path, "wb") as f:
        f.write(content)

    return {
        "message": "File stored successfully",
        "node_id": NODE_ID,
        "object_path": object_path,
        "size": len(content),
    }


@app.get("/download/{object_path:path}")
def download_file(object_path: str):
    target_path = storage_dir / object_path

    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Object not found")

    return FileResponse(
        path=str(target_path),
        filename=target_path.name,
        media_type="application/octet-stream"
    )


@app.delete("/delete/{object_path:path}")
def delete_file(object_path: str):
    target_path = storage_dir / object_path

    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Object not found")

    target_path.unlink()

    return {
        "message": "File deleted successfully",
        "node_id": NODE_ID,
        "object_path": object_path,
    }
