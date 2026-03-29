import requests
import random


class GossipProtocol:
    def __init__(self, nodes):
        self.nodes = nodes

    def spread_metadata(self, file_metadata: dict, replication_factor=2):
        selected_nodes = random.sample(self.nodes, replication_factor)

        for node in selected_nodes:
            try:
                requests.post(
                    f"{node['url']}/metadata",
                    json=file_metadata
                )
            except:
                pass

    def query_metadata(self, file_id: str):
        nodes = self.nodes.copy()
        random.shuffle(nodes)

        for node in nodes:
            try:
                res = requests.get(f"{node['url']}/metadata/{file_id}")
                if res.status_code == 200:
                    return res.json()
            except:
                continue

        return None