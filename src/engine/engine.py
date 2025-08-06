"""blankDB engine"""

from pathlib import Path


class SQLengine:
    """simple database engine class"""

    def __init__(self, db_path: str | None = None) -> None:
        self.database_path = db_path if db_path else "./data/"

    def sql_create(self, parameters: list):
        # CREATE TABLE <name>
        create_type, db_name = parameters

        match create_type:
            case "TABLE":
                self.db_file = Path(self.database_path + db_name)
                if self.db_file.exists():
                    print("E: table already exists!")
                    raise FileExistsError

    def sql_from(self):
        pass

    def sql_select(self):
        pass
