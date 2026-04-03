from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from pathlib import Path
import requests

from storage import StorageEngine
from audit import AuditLog
from jurisdiction import Jurisdiction
from config import NodeConfig
from dht import DHT

app = FastAPI()

config = NodeConfig()
self_node = config.get_self()
peers = config.get_peers()

BASE_DATA_DIR = Path("/app/data")
NODE_DATA_DIR = BASE_DATA_DIR / config.node_id
NODE_DATA_DIR.mkdir(parents=True, exist_ok=True)

storage = StorageEngine(base_path=str(NODE_DATA_DIR))
audit = AuditLog()
jurisdiction = Jurisdiction(config.region)
dht = DHT(self_node, peers)

METADATA_STORE = {}


def forward_request(node, endpoint, method="GET", files=None, data=None):
    """
    Kept only for optional debugging/future use.
    Not used in store/fetch in the stable version.
    """
    try:
        url = f"{node['url']}{endpoint}"
        if method == "POST":
            return requests.post(url, files=files, data=data, timeout=5)
        return requests.get(url, timeout=5)
    except Exception as e:
        print(f"[FORWARD-ERROR] node={self_node['node_id']} url={url} err={e}")
        return None


@app.post("/store")
async def store_chunk(
    chunk_id: str = Form(...),
    region: str = Form(None),
    file: UploadFile = File(...)
):
    data = await file.read()

    print(
        f"[STORE-REQ] node={self_node['node_id']} "
        f"chunk={chunk_id} size={len(data)} region={region}"
    )

    # Enforce jurisdiction policy
    if region and not jurisdiction.is_allowed(region):
        print(
            f"[JURISDICTION-DENY] node={self_node['node_id']} "
            f"node_region={jurisdiction.get_region()} required={region}"
        )
        return JSONResponse(
            content={
                "error": "jurisdiction_violation",
                "node_region": jurisdiction.get_region(),
                "required_region": region
            },
            status_code=403
        )

    storage.store_chunk(chunk_id, data)
    audit.log_event("STORE", f"{chunk_id} at {self_node['node_id']}")

    return {
        "status": "stored",
        "node": self_node["node_id"],
        "region": self_node["region"],
        "chunk_id": chunk_id,
        "size": len(data),
    }


@app.get("/fetch/{chunk_id}")
def fetch_chunk(chunk_id: str):
    print(
        f"[FETCH-REQ] node={self_node['node_id']} "
        f"chunk={chunk_id}"
    )

    data = storage.retrieve_chunk(chunk_id)

    if data is None:
        print(
            f"[FETCH-MISS] node={self_node['node_id']} "
            f"chunk={chunk_id} available={storage.list_chunks()}"
        )
        return JSONResponse(
            content={
                "error": "not found",
                "node": self_node["node_id"],
                "chunk_id": chunk_id
            },
            status_code=404
        )

    print(
        f"[FETCH-HIT] node={self_node['node_id']} "
        f"chunk={chunk_id} size={len(data)}"
    )

    audit.log_event("FETCH", f"{chunk_id} accessed")

    return Response(
        content=data,
        status_code=200,
        media_type="application/octet-stream"
    )


@app.post("/metadata")
async def store_metadata(metadata: dict):
    file_id = metadata["file_id"]
    METADATA_STORE[file_id] = metadata

    print(
        f"[META-STORE] node={self_node['node_id']} "
        f"file_id={file_id} chunks={len(metadata.get('chunks', []))}"
    )

    audit.log_event("META_STORE", file_id)
    return {"status": "stored", "node": self_node["node_id"]}


@app.get("/metadata/{file_id}")
def get_metadata(file_id: str):
    print(f"[META-GET] node={self_node['node_id']} file_id={file_id}")

    data = METADATA_STORE.get(file_id)
    if not data:
        print(f"[META-MISS] node={self_node['node_id']} file_id={file_id}")
        return JSONResponse({"error": "not found"}, status_code=404)

    return data


@app.get("/status")
def status():
    return {
        "node_id": self_node["node_id"],
        "region": self_node["region"],
        "stored_chunks": storage.list_chunks()
    }


@app.get("/audit")
def get_audit():
    return audit.get_logs()