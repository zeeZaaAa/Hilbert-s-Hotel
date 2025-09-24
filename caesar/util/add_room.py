def add_room(db: dict, roomnumber, guest):
    try:
        db[roomnumber] = str(guest)
        return "success"
    except TypeError as e:
        return f"TypeError: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

    
    
    