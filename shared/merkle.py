from shared.hashing import sha256_hash


def build_merkle_tree(chunks: list):
    """
    Build Merkle tree from chunk hashes.
    Returns root hash.
    """
    if not chunks:
        return None

    level = [sha256_hash(chunk) for chunk in chunks]

    while len(level) > 1:
        next_level = []

        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left

            combined = sha256_hash((left + right).encode())
            next_level.append(combined)

        level = next_level

    return level[0]