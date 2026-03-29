import hashlib


class DHT:
    def __init__(self, self_node, peers):
        """
        self_node: dict -> {node_id, url, region}
        peers: list of all nodes
        """
        self.self_node = self_node
        self.peers = peers

    def _hash(self, key: str) -> int:
        """
        Convert key into large integer using SHA256
        """
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)

    def _sort_nodes(self):
        """
        Sort nodes deterministically by hash of node_id
        """
        return sorted(
            self.peers,
            key=lambda n: self._hash(n["node_id"])
        )

    def find_responsible_node(self, key: str):
        """
        Given a key (chunk_id), find responsible node.
        """
        key_hash = self._hash(key)
        sorted_nodes = self._sort_nodes()

        for node in sorted_nodes:
            node_hash = self._hash(node["node_id"])
            if key_hash <= node_hash:
                return node

        # wrap-around (ring behavior)
        return sorted_nodes[0]


    def find_node_by_region(self, key: str, required_region: str):
        candidates = [n for n in self.peers if n["region"] == required_region]

        if not candidates:
            return self.find_responsible_node(key)

        key_hash = self._hash(key)

        sorted_nodes = sorted(
            candidates,
            key=lambda n: self._hash(n["node_id"])
        )

        for node in sorted_nodes:
            if key_hash <= self._hash(node["node_id"]):
                return node

        return sorted_nodes[0]


    def get_replica_nodes(self, key: str, replication_factor=2):
        """
        Get multiple nodes for replication
        """
        sorted_nodes = self._sort_nodes()
        primary = self.find_responsible_node(key)

        index = sorted_nodes.index(primary)

        replicas = []
        for i in range(replication_factor):
            replicas.append(
                sorted_nodes[(index + i) % len(sorted_nodes)]
            )

        return replicas

    def is_responsible(self, key: str):
        """
        Check if current node is responsible for this key
        """
        node = self.find_responsible_node(key)
        return node["node_id"] == self.self_node["node_id"]