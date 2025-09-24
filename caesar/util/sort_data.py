def sort_data(db: dict):
    try:
        sorted_db = dict(sorted(db.items(), key=lambda x: int(x[0])))
        return sorted_db
    except ValueError as e:
        return f"ValueError: {str(e)}"
    except TypeError as e:
        return f"TypeError: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"