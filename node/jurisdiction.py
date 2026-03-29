class Jurisdiction:
    def __init__(self, region: str):
        self.region = region

    def get_region(self):
        return self.region

    def is_allowed(self, required_region: str):
        """
        Check if this node can store data for given region policy.
        """
        return self.region == required_region