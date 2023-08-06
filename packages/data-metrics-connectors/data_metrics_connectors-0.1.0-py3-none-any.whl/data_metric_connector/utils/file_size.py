import math


def convert_size(size_bytes: float) -> str:
    """
    Converts bytes to "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB".

    :param size_bytes: size in bytes
    :return: converted size
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
