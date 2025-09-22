"""storage functions module"""

from pathlib import Path

data_dir = "/home/flu/Project/blankDB/data"
data_path = Path(data_dir)
# need better definition of pages size when implementing create table


def has_storage_folder() -> bool:
    return data_path.is_dir()


def _from(value: str) -> Path | None:
    """function to exectute FROM logic"""
    table_path = Path(f"{data_dir}/{value}.sql")
    if table_path.exists():
        return table_path
    # handle error
    return


def _select(value: str, table_path: Path) -> list:
    """function to exectute SELECT logic"""
    sattr: str = value.value  # selected attribute from token value
    with open(table_path, "r") as table_in:
        page_size: int = int(table_in.readline().strip())
        attr_list: list[str] = table_in.readline().strip().split(",")
        attr_list_length: int = len(attr_list)
        if sattr not in attr_list:
            # handle error
            return
        attr_index: int = attr_list.index(sattr)

        result: list = []
        flag_eof = False
        iter_index = 0
        while not flag_eof:
            iter_attr: str = table_in.readline(page_size)

            if not len(iter_attr):
                flag_eof = True
                continue

            elif iter_index % attr_list_length == attr_index:
                result.append(iter_attr.strip())

            iter_index += 1

        return result


if __name__ == "__main__":
    table_path = _from("dummy")
    result = _select("id", table_path)
    print(result)
