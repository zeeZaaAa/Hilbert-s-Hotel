def search_room(db: dict, roomnumber):
    try:
        return str(db[roomnumber])
    except KeyError:
        return f"Room not found: {roomnumber}"
    except Exception as e:
        return f"Error: {str(e)}"
