# for api
# run here!
from fastapi import FastAPI
from fastapi import Request
from fastapi import Query
from fastapi.responses import JSONResponse
from typing import List
import time
from pympler import asizeof
import json
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

roomData = {}

count = 1

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
        
        global roomData
        roomData = {}
        
        start_insert = time.perf_counter()

        roomData = add(roomData, old)

        roomData = add(roomData, new)
        # start = 0
        # for guest in max:
        #     guest = int(guest)
        #     sliceData = new[start:start+guest]
        #     roomData = add(roomData, sliceData)
        #     start+=guest

        end_insert = time.perf_counter()

        if not isinstance(roomData, dict):
            return JSONResponse(
            content={"error": roomData},
            status_code=400
        )
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={
                "message": f"{len(old) + len(new)} rooms created",
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "insert_time_taken": f"{end_insert - start_insert:.4f} seconds",
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
        
        return JSONResponse(
            content={"message": f"{len(old_guests)+len(roomnumber)} rooms created",
                "all_time_taken": f"{end_insert - start_time:.4f} seconds",
                "insert_time_taken": f"{end_insert - start_insert:.4f} seconds",
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
            
        global roomData
        
        start_delete = time.perf_counter()
        for room in roomnumber:
            room = int(room)
            if room not in roomData:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            delete(roomData, room)
        end_delete = time.perf_counter()

        return JSONResponse(
            content={"message": f"Room {roomnumber} deleted",
                "all_time_taken": f"{end_delete - start_time:.4f} seconds",
                "delete_time_taken": f"{end_delete - start_delete:.4f} seconds",
            },
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
            
        global roomData
        
        results = {}
        start_search = time.perf_counter()
        for room in roomnumber:
            room = int(room)
            if room not in roomData:
                return JSONResponse(
                    content={"error": f"Room not found: {room}"},
                    status_code=404
                )
            results[room] = search_room(roomData, room)
            
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={"results": json.dumps(results),
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "search_time_taken": f"{end_time - start_search:.4f} seconds",
                },
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
        global roomData
        
        if not roomData:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        start_sort = time.perf_counter()
            
        sorted_rooms = sort_data(roomData)
        
        end_sort = time.perf_counter()

        if not isinstance(sorted_rooms, dict):
            return JSONResponse(
            content={"error": sorted_rooms},
            status_code=500
            )
        
        end_time = time.perf_counter()
        
        return JSONResponse(
            content={"sorted_rooms": json.dumps(sorted_rooms),
                "all_time_taken": f"{end_time - start_time:.4f} seconds",
                "sort_time_taken": f"{end_sort - start_sort:.4f} seconds",
                },
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
        
@app.get("/data-size")
def get_data_size():
    start_time = time.perf_counter()
    try:
        global roomData
        if not roomData:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        datasize = asizeof.asizeof(roomData)
        end_sizing = time.perf_counter()
        
        return JSONResponse(
            content={"all_time_taken": f"{end_sizing - start_time:.4f} seconds",
                "data_size": f"{datasize/1024:.4f} KB"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
        
@app.get("/save-file")
def save_file():
    start_time = time.perf_counter()
    try:
        global roomData
        if not roomData:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        save_to_json(roomData, "File/roomData.json")
        end_save = time.perf_counter()
        
        return JSONResponse(
            content={"all_time_taken": f"{end_save - start_time:.4f} seconds",
                "message": "File Saved!"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
