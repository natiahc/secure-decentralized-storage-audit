class ChunkMetadata:
    def __init__(self, chunk_id: str, node: str, index: int):
        self.chunk_id = chunk_id
        self.node = node
        self.index = index

    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "node": self.node,
            "index": self.index
        }


class FileMetadata:
    def __init__(self, file_id: str, chunks: list[ChunkMetadata], merkle_root=None):
        self.file_id = file_id
        self.chunks = chunks
        self.merkle_root = merkle_root

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "merkle_root": self.merkle_root,
            "chunks": [c.to_dict() for c in self.chunks]
        }


class NodeInfo:
    def __init__(self, node_id: str, url: str, region: str):
        self.node_id = node_id
        self.url = url
        self.region = region

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "url": self.url,
            "region": self.region
        }