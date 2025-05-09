class Engine:
    PAGE_SIZE = 4096

    def __init__(self):
        self.buffer = bytearray(self.PAGE_SIZE)
        self.record_offsets = []

    def add_record(self, record_data):
        pass
