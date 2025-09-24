def delete(db: dict, roomnumber):
    try:
        del db[roomnumber]
        return "success"
    except Exception as e:
        return f"Error: {str(e)}"