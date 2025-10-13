def insert_to_dict(d: dict, key, value):
    try:
        d[key] = value
        return "success"
    except Exception as e:
        return f"Error: {str(e)}"
