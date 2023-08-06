def format_size(size: int, bits=False) -> str:
    """
    The function converts bytes or bits to formatted units of measurement.

    :param size: The number of bytes or bits to format. Must be an Integer.
    :param bits: Specify True if you are passing bits (1/8 from byte) to the function, not bytes.
    :return: A string with formatted units of measurement.
    """
    if bits:
        if abs(size) < 1000:
            return f"{round(size, 1)}  Бит"
        size /= 8
    for unit in ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ', 'ПБ', 'ЭБ', 'ЗБ']:
        if abs(size) < 1000:
            return f"{round(size, 1)} {unit}"
        size /= 1000
    return f"{round(size, 1)} ЙБ"