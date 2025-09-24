# for api
# run here!
from fastapi import FastAPI
from fastapi import Request
from fastapi import Query
from fastapi.responses import JSONResponse
from typing import List
from caesar.controller.inputController import createGuests
from caesar.controller.inputController import get_roomnumberAndguests
from caesar.util.add_room import add_room
from caesar.util.delete import delete
from caesar.util.sort_data import sort_data
from caesar.util.search import search_room
from icy.duty import save_to_json
from icy.duty import load_from_json

app = FastAPI()

# input
old_guess = 10
chanel = [1,2,3,"bus"]
max = [5,3,1,4]

count = 1

# guesses = createGuests(old_guess, chanel, max)
# for guess in guesses:
#     print(guess)

# print(roomData)
# roomData["1"] = guesses[0]
# print(roomData)
# value = roomData.get("1")
# print(f'value: {value}')

#######################################
# fast api example for test call api
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
######################################

#################################
# real api
##################################
# path | POST /create-data
# body = old_guess(int), chanel(List[int]), max(List[int])
@app.post("/create-data")
async def create_data(request: Request):
    try:
        data = await request.json()
        old_guess = data["old_guess"]
        chanel = data["chanel"]
        max = data["max"]
        
        guests = createGuests(old_guess, chanel, max)
        if not isinstance(guests, list):
            return JSONResponse(
            content={"error": guests},
            status_code=400
        )
        # calculate roomnumber method
        roomnumbers  = [] #mock
        ####################
        roomData = {}
        for roomnumber,guest in zip(roomnumbers,guests):
            add_room(roomData, roomnumber, guest)
        
        save_to_json(roomData, "DB/roomData.json")
        
        return JSONResponse(
            content={"message": f"{len(guests)} rooms created"},
            status_code=200
        )

    except KeyError as e:
        return JSONResponse(
            content={"error": f"Missing key: {str(e)}"},
            status_code=400
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
    
# path | POST /add-room
# body = roomnumber(List[int])
@app.post("/add-room")
async def add_room(req: Request):
    try:
        data = await req.json()
        roomnumber = data.get("roomnumber")
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
        # calculate roomnumber method
        temporaryRoomdata = {}
        for room in roomnumber:
            global count
            add_room(temporaryRoomdata, room, f"Chanel:force-add,Order:{count}")
            count+=1
        roomData = load_from_json("DB/roomData.json")
        old_roomnumbers, old_guests = get_roomnumberAndguests(roomData)
        # calculate roomnumber method
        new_roomnumbers  = [] #mock
        ####################
        for room, guest in zip(new_roomnumbers, old_guests):
            add_room(temporaryRoomdata, room, guest)
        
        save_to_json(roomData, "DB/roomData.json")
        
        return JSONResponse(
            content={"message": f"{len(old_guests)+len(roomnumber)} rooms created"},
            status_code=200
        )
        
    except KeyError as e:
        return JSONResponse(
            content={"error": f"Missing key: {str(e)}"},
            status_code=400
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
        
# path | DELETE /delete-room?roomnumber=111
# body = None
@app.delete("/delete-room")
def delete_room(roomnumber: List[str] = Query(...)):
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
            
        db = load_from_json("DB/roomData.json")
        
        for room in roomnumber:
            if room not in db:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            delete(db, room)

        save_to_json(db, "DB/roomData.json")

        return JSONResponse(
            content={"message": f"Room {roomnumber} deleted"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
    
# path | GET /search-room?roomnumber=111&roomnumber=333&roomnumber=444
# body = None
@app.get("/search-room")
def search(roomnumber: List[str] = Query(...)):
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
            
        db = load_from_json("DB/roomData.json")
        
        results = {}
        for room in roomnumber:
            if room not in db:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            results[room] = search_room(db, room)
        
        return JSONResponse(
            content={"data": results},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )

# path | GET /sort-room
# body = None
@app.get("/sort-room")
def sort_room():
    try:
        db = load_from_json("DB/roomData.json")
        
        if not db:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        sorted_rooms = sort_data(db)
        
        save_to_json(sorted_rooms, "DB/roomData.json")
        
        return JSONResponse(
            content={"sorted_rooms": sorted_rooms},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
