import os


class NodeConfig:
    def __init__(self):
        self.node_id = os.getenv("NODE_ID", "node1")
        self.port = int(os.getenv("PORT", "5001"))
        self.region = os.getenv("REGION", "IN")

        # Internal Docker network URLs
        self.peers = [
            {
                "node_id": "node1",
                "url": "http://node1:5001",
                "region": "IN"
            },
            {
                "node_id": "node2",
                "url": "http://node2:5002",
                "region": "EU"
            },
            {
                "node_id": "node3",
                "url": "http://node3:5003",
                "region": "US"
            }
        ]

    def get_self(self):
        for p in self.peers:
            if p["node_id"] == self.node_id:
                return p
        return None

    def get_peers(self):
        return self.peers