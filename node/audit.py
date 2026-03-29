import time
from shared.hashing import hash_string


class AuditLog:
    def __init__(self):
        self.chain = []

    def _get_last_hash(self):
        if not self.chain:
            return "GENESIS"
        return self.chain[-1]["hash"]

    def log_event(self, event_type: str, details: str):
        prev_hash = self._get_last_hash()

        timestamp = str(time.time())
        raw_data = f"{event_type}|{details}|{timestamp}|{prev_hash}"

        current_hash = hash_string(raw_data)

        entry = {
            "event": event_type,
            "details": details,
            "timestamp": timestamp,
            "prev_hash": prev_hash,
            "hash": current_hash
        }

        self.chain.append(entry)

        return entry

    def get_logs(self):
        return self.chain