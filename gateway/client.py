import requests

from shared.chunker import split_file, merge_chunks
from shared.hashing import sha256_hash
from shared.models import ChunkMetadata, FileMetadata
from shared.merkle import build_merkle_tree

NODES = [
    {"node_id": "node1", "url": "http://node1:5001"},
    {"node_id": "node2", "url": "http://node2:5002"},
    {"node_id": "node3", "url": "http://node3:5003"},
]

REGION_POLICY = "IN"


def _resolve_node_url(node_id: str) -> str:
    for node in NODES:
        if node["node_id"] == node_id:
            return node["url"]
    raise Exception(f"Unknown node_id: {node_id}")


def upload_file(file_bytes: bytes):
    chunks = split_file(file_bytes)
    chunk_metadata_list = []

    for index, chunk in enumerate(chunks):
        chunk_id = sha256_hash(chunk)

        # Deterministic DHT-style selection
        node_index = int(chunk_id, 16) % len(NODES)
        node = NODES[node_index]

        res = requests.post(
            f"{node['url']}/store",
            files={"file": ("chunk", chunk)},
            data={
                "chunk_id": chunk_id,
                "region": REGION_POLICY,
            },
            timeout=5,
        )

        if res.status_code != 200:
            raise Exception(f"Failed to store chunk {chunk_id}: {res.text}")

        result = res.json()

        chunk_metadata_list.append(
            ChunkMetadata(
                chunk_id=chunk_id,
                node=result.get("node", node["node_id"]),
                index=int(index),
            )
        )
        print(f"[UPLOAD] index={index} size={len(chunk)} hash={chunk_id}")

    file_id = sha256_hash("".join(c.chunk_id for c in chunk_metadata_list).encode())
    merkle_root = build_merkle_tree(chunks)
    return FileMetadata(file_id, chunk_metadata_list, merkle_root)


def download_file(file_meta: FileMetadata):
    chunks_by_index = {}
    sorted_chunks = sorted(file_meta.chunks, key=lambda c: int(c.index))

    for chunk in sorted_chunks:
        print(
            f"[DOWNLOAD] chunk index={chunk.index} "
            f"id={chunk.chunk_id} node={chunk.node}"
        )

        candidate_nodes = []
        try:
            primary_url = _resolve_node_url(chunk.node)
            candidate_nodes.append(primary_url)
        except Exception:
            pass

        for node in NODES:
            if node["node_id"] != chunk.node:
                candidate_nodes.append(node["url"])

        print(f"[DOWNLOAD] candidate_nodes={candidate_nodes}")

        chunk_data = None

        for base_url in candidate_nodes:
            try:
                res = requests.get(
                    f"{base_url}/fetch/{chunk.chunk_id}",
                    timeout=5,
                )

                print(
                    f"[DOWNLOAD] tried={base_url} "
                    f"status={res.status_code} "
                    f"content_type={res.headers.get('content-type')} "
                    f"size={len(res.content)}"
                )

                if res.status_code != 200:
                    continue

                if res.headers.get("content-type", "").startswith("application/json"):
                    print(f"[DOWNLOAD] skipping JSON response from {base_url}")
                    continue

                chunk_data = res.content
                downloaded_hash = sha256_hash(chunk_data)

                print(
                    f"[DOWNLOAD] expected={chunk.chunk_id} "
                    f"got={downloaded_hash}"
                )

                if downloaded_hash != chunk.chunk_id:
                    print(f"[DOWNLOAD] hash mismatch at {base_url}")
                    continue

                break

            except requests.exceptions.RequestException as e:
                print(f"[DOWNLOAD] error contacting {base_url}: {e}")
                continue

        if chunk_data is None:
            raise Exception(f"Chunk fetch failed: {chunk.chunk_id}")

        chunks_by_index[int(chunk.index)] = chunk_data

    ordered_chunks = [chunks_by_index[i] for i in range(len(sorted_chunks))]
    reconstructed = merge_chunks(ordered_chunks)

    new_root = build_merkle_tree(ordered_chunks)

    print(
        f"[DOWNLOAD] merkle_expected={file_meta.merkle_root} "
        f"merkle_got={new_root}"
    )

    if new_root != file_meta.merkle_root:
        raise Exception("Integrity check failed!")

    return reconstructed