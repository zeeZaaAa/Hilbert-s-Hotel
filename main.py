# for api
# run here!
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from caesar.controller.inputController import createGuests

roomData = {}

app = FastAPI()

# input
old_guess = 10
chanel = [1,2,3,"bus"]
max = [5,3,1,4]

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

# real api
@app.post("/create-data")
async def create_data(request: Request):
    data = await request.json()
    old_guess = data[old_guess]
    chanel = data[chanel]
    max = data[max]
    guesses = createGuests(old_guess, chanel, max)
    
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
        # add room method
        
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
        
@app.delete("/delete-room")
def delete_room(roomnumber: str | None = None):
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )

        if roomnumber not in roomData:
            return JSONResponse(
                content={"error": f"Room {roomnumber} not found"},
                status_code=404
            )

        del roomData[roomnumber]

        return JSONResponse(
            content={"message": f"Room {roomnumber} deleted"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
    
@app.get("/search-room")
def search(roomnumber: str | None = None):
    try:
        if not roomnumber:
            return JSONResponse(
                content={"error": "Missing roomnumber"},
                status_code=400
            )
        value = roomData.get(roomnumber)
        if value is None:
            return JSONResponse(
                content={"error": f"Room {roomnumber} not found"},
                status_code=404
            )
        return JSONResponse(
            content={"data": {roomnumber: value}},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )

@app.get("/sort-room")
def sort_room():
    try:
        if not roomData:
            return JSONResponse(
                content={"error": "No rooms available"},
                status_code=404
            )
            
        sorted_rooms = dict(sorted(roomData.items(), key=lambda x: int(x[0])))
        
        return JSONResponse(
            content={"sorted_rooms": sorted_rooms},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
