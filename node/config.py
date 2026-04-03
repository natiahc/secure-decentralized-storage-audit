import os


class NodeConfig:
    def __init__(self):
        # Node identity from environment
        self.node_id = os.getenv("NODE_ID", "node1")
        self.port = int(os.getenv("PORT", "5001"))
        self.region = os.getenv("REGION", "IN")
        self.host = os.getenv("HOST", self.node_id)

        # Bootstrap peers (no self here)
        self.peers = [
            {"node_id": "node1", "url": "http://node1:5001"},
            {"node_id": "node2", "url": "http://node2:5002"},
            {"node_id": "node3", "url": "http://node3:5003"},
        ]

    def get_self(self):
        """
        Return this node's identity using environment config.
        """
        return {
            "node_id": self.node_id,
            "url": f"http://{self.host}:{self.port}",
            "region": self.region
        }

    def get_peers(self):
        """
        Return peers excluding this node.
        """
        return [p for p in self.peers if p["node_id"] != self.node_id]