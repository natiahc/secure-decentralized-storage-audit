class NodeRegistry:
    def __init__(self):
        self.nodes = [
            {"node_id": "node1", "url": "http://node1:5001", "region": "IN"},
            {"node_id": "node2", "url": "http://node2:5002", "region": "EU"},
            {"node_id": "node3", "url": "http://node3:5003", "region": "US"},
        ]

    def get_all_nodes(self):
        return self.nodes

    def get_node(self, node_id: str):
        for node in self.nodes:
            if node["node_id"] == node_id:
                return node
        return None