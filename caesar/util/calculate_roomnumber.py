def calculate_roomnumber(r: int, c: int):
    if not isinstance(r, int) or not isinstance(c, int):
        return "Error, n and m must be integers"
    return int(((r + c + 1) * (r + c)) / 2 + c)