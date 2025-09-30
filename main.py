# for api
# run here!
from fastapi import FastAPI
from fastapi import Request
from fastapi import Query
from fastapi.responses import JSONResponse
from typing import List
import time
from pympler import asizeof
from caesar.controller.inputController import createGuests
from caesar.controller.inputController import get_roomnumberAndguests
from caesar.util.add_room import add_room
from caesar.util.delete import delete
from caesar.util.sort_data import sort_data
from caesar.util.search import search_room
from icy.duty import save_to_json
from icy.duty import load_from_json
from pix.util.add_guest import add

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
    start_time = time.perf_counter()
    try:
        data = await request.json()
        old_guess = data["old_guess"]
        chanel = data["chanel"]
        max = data["max"]
        
        old, new = createGuests(old_guess, chanel, max)
        if not isinstance(old, list):
            return JSONResponse(
            content={"error": old},
            status_code=400
        )
        if not isinstance(new, list):
            return JSONResponse(
            content={"error": new},
            status_code=400
        )
        roomData = {}
        
        start_insert = time.perf_counter()

        roomData = add(roomData, old)

        roomData = add(roomData, new)
            
        end_insert = time.perf_counter()

        if not isinstance(roomData, dict):
            return JSONResponse(
            content={"error": roomData},
            status_code=400
        )
        
        datasize = asizeof.asizeof(roomData)
        
        save_to_json(roomData, "DB/roomData.json")
        
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={
                "message": f"{len(old) + len(new)} rooms created",
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "insert_time_taken": f"{end_insert - start_insert:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"
            },
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
async def add_room_api(req: Request):
    start_time = time.perf_counter()
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
        roomData = load_from_json("DB/roomData.json")
        old_roomnumbers, old_guests = get_roomnumberAndguests(roomData)
        # calculate roomnumber method
        new_roomnumbers  = [] #mock
        ####################
        start_insert = time.perf_counter()
        
        for room in roomnumber:
            global count
            add_room(temporaryRoomdata, room, f"Chanel:force-add,Order:{count}")
            count+=1
        for room, guest in zip(new_roomnumbers, old_guests):
            add_room(temporaryRoomdata, room, guest)
            
        end_insert = time.perf_counter()
        
        datasize = asizeof.asizeof(temporaryRoomdata)
        
        save_to_json(temporaryRoomdata, "DB/roomData.json")
        
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={"message": f"{len(old_guests)+len(roomnumber)} rooms created",
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "insert_time_taken": f"{end_insert - start_insert:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"},
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
    start_time = time.perf_counter()
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
            
        db = load_from_json("DB/roomData.json")
        
        start_delete = time.perf_counter()
        for room in roomnumber:
            if room not in db:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            delete(db, room)
        end_delete = time.perf_counter()
        
        datasize = asizeof.asizeof(db)

        save_to_json(db, "DB/roomData.json")
        
        end_time = time.perf_counter()

        return JSONResponse(
            content={"message": f"Room {roomnumber} deleted",
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "delete_time_taken": f"{end_delete - start_delete:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"},
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
    start_time = time.perf_counter()
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
            
        db = load_from_json("DB/roomData.json")
        
        results = {}
        start_search = time.perf_counter()
        for room in roomnumber:
            if room not in db:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            results[room] = search_room(db, room)
            
        datasize = asizeof.asizeof(db)
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={"results": results,
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "search_time_taken": f"{end_time - start_search:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"},
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
    start_time = time.perf_counter()
    try:
        db = load_from_json("DB/roomData.json")
        
        if not db:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        start_sort = time.perf_counter()
            
        sorted_rooms = sort_data(db)
        
        end_sort = time.perf_counter()
        
        datasize = asizeof.asizeof(sorted_rooms)
        
        save_to_json(sorted_rooms, "DB/roomData.json")
        
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={"sorted_rooms": sorted_rooms,
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "sort_time_taken": f"{end_sort - start_sort:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
