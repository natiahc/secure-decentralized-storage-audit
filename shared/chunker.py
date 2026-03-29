CHUNK_SIZE = 10240  # 10KB


def split_file(data: bytes):
    """
    Split file into chunks.
    """
    return [
        data[i:i + CHUNK_SIZE]
        for i in range(0, len(data), CHUNK_SIZE)
    ]


def merge_chunks(chunks: list):
    """
    Merge chunks back into original file.
    """
    return b"".join(chunks)