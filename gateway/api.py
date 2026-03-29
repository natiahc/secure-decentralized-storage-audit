from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import requests

from client import upload_file, download_file
from shared.models import ChunkMetadata, FileMetadata
from network.registry import NodeRegistry
from network.gossip import GossipProtocol


registry = NodeRegistry()
gossip = GossipProtocol(registry.get_all_nodes())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()

    file_meta = upload_file(data)

    gossip.spread_metadata(file_meta.to_dict())

    return file_meta.to_dict()


@app.get("/download/{file_id}")
def download(file_id: str):
    meta = gossip.query_metadata(file_id)

    if not meta:
        return JSONResponse({"error": "metadata not found"}, status_code=404)

    chunks = [
        ChunkMetadata(c["chunk_id"], c["node"], c["index"])
        for c in meta["chunks"]
    ]

    file_meta = FileMetadata(
        meta["file_id"],
        chunks,
        meta.get("merkle_root")
    )

    data = download_file(file_meta)

    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file_id}"'
        }
    )


@app.get("/status")
def status():
    nodes = registry.get_all_nodes()
    result = []

    for node in nodes:
        try:
            res = requests.get(f"{node['url']}/status")
            result.append(res.json())
        except:
            result.append({"node": node["node_id"], "status": "down"})

    return result


@app.get("/audit")
def audit():
    nodes = registry.get_all_nodes()
    logs = []

    for node in nodes:
        try:
            res = requests.get(f"{node['url']}/audit")
            logs.append({"node": node["node_id"], "logs": res.json()})
        except:
            logs.append({"node": node["node_id"], "logs": "error"})

    return logs