import struct


class Engine:
    def __init__(self) -> None:
        pass

    def write_record(file, record):
        """int(4B) str(var)"""
        data = struct.pack("ID", record["id"], record["value"])
        data += record["name"].encode("utf-8") + b"\x00"  # terminate with NULL
        file.write(data)
