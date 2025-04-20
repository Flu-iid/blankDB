"""experimental DBMS for academic purposes with microkernel architecture in mind written in python."""

import os
from collections import defaultdict


class BlankDB:
    """blank database object"""

    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.tables = {}
        self.indexes = defaultdict(dict)

        if not os.path.exists(db_name):
            os.makedirs(db_name)
