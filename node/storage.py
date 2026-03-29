from pathlib import Path
from shared.hashing import sha256_hash


class StorageEngine:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

        print(f"[STORAGE-INIT] base_path={self.base_path}")

    def get_chunk_path(self, chunk_id: str) -> Path:
        return self.base_path / chunk_id

    def store_chunk(self, chunk_id: str, data: bytes):
        path = self.get_chunk_path(chunk_id)

        print(
            f"[STORAGE-STORE] path={path} "
            f"size={len(data)} hash={sha256_hash(data)}"
        )

        path.write_bytes(data)

        print(
            f"[STORAGE-STORE-DONE] path={path} "
            f"exists={path.exists()} size_on_disk={path.stat().st_size}"
        )

    def retrieve_chunk(self, chunk_id: str):
        path = self.get_chunk_path(chunk_id)

        print(f"[STORAGE-GET] path={path} exists={path.exists()}")

        if not path.exists():
            files = self.list_chunks()
            print(f"[STORAGE-MISS] base_path={self.base_path} files={files}")
            return None

        data = path.read_bytes()

        print(
            f"[STORAGE-HIT] path={path} "
            f"size={len(data)} hash={sha256_hash(data)}"
        )

        return data

    def list_chunks(self):
        if not self.base_path.exists():
            return []
        return sorted([p.name for p in self.base_path.iterdir() if p.is_file()])