# frontend/app.py
from fasthtml.common import *
import requests

app, rt = fast_app(hdrs=(
    # เพิ่มลิงก์ tailwind css
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
))

API_URL = "http://127.0.0.1:8001"

@rt("/")
def main_page():
    return Div(
        H1("Infinite HOTEL", cls="text-white text-3xl mb-6 text-center"),
        Form(
            Input(name="old_guess", placeholder="old guest amount", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Input(name="chanel", placeholder="new channel", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Input(name="max", placeholder="max channel", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Button("SUBMIT", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/hotel", method="post"
        ),
        cls="min-h-screen flex items-center justify-center bg-black p-10"
    )

@rt("/hotel", methods=["POST"])
def hotel_page(old_guess: str = None, chanel: str = None, max: str = None):
    if not old_guess or not chanel or not max:
        return Div("กรุณากรอกข้อมูลให้ครบถ้วน", cls="text-red-500")

    try:
        old_guess = int(old_guess)
        chanel = [x.strip() for x in chanel.split(",")]
        max = [int(x.strip()) for x in max.split(",")]
        resp = requests.post(f"{API_URL}/create-data", json={
            "old_guess": old_guess,
            "chanel": chanel,
            "max": max
        })
        data = resp.json()
        if resp.status_code != 200:
            return Div(f"เกิดข้อผิดพลาด: {data.get('error', 'Unknown error')}", cls="text-red-500")
    except Exception as e:
        return Div(f"เกิดข้อผิดพลาด: {str(e)}", cls="text-red-500")

    return Div(
        Button("add room", onclick="window.location.href='/add-room'", cls="px-4 py-2 bg-blue-500 text-white rounded"),
        Button("delete room", onclick="window.location.href='/delete-room'", cls="px-4 py-2 bg-blue-500 text-white rounded"),
        Button("search room", onclick="window.location.href='/search-room'", cls="px-4 py-2 bg-blue-500 text-white rounded"),
        Button("sort room", onclick="window.location.href='/sort-room'", cls="px-4 py-2 bg-blue-500 text-white rounded"),
        Button("back", onclick="window.location.href='/'", cls="px-4 py-2 bg-blue-500 text-white rounded")
    )

# --- Add Room ---
@rt("/add-room", methods=["GET"])
def add_room():
    return Div(
        Form(
            Input(name="roomnumber", placeholder="เช่น 101,102,103", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Button("SUBMIT", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/add-room-done", method="post"
        )
    )

@rt("/add-room-done", methods=["POST"])
def add_room_done(roomnumber: str = None):
    if not roomnumber:
        return Div("กรุณากรอกหมายเลขห้อง", cls="text-red-500")
    try:
        room_list = [x.strip() for x in roomnumber.split(",") if x.strip()]
        resp = requests.post(f"{API_URL}/add-room", json={"roomnumber": room_list})
        data = resp.json()
        if resp.status_code != 200:
            return Div(f"เกิดข้อผิดพลาด: {data.get('error', 'Unknown error')}", cls="text-red-500")
        return H1(f"เพิ่มห้อง {', '.join(room_list)} สำเร็จ!", cls="text-green-500")
    except Exception as e:
        return Div(f"เกิดข้อผิดพลาด: {str(e)}", cls="text-red-500")

# --- Delete Room ---
@rt("/delete-room", methods=["GET"])
def delete_room_form():
    return Div(
        Form(
            Input(name="roomnumber", placeholder="เช่น 101,102", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Button("ลบห้อง", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/delete-room-done", method="post"
        )
    )

@rt("/delete-room-done", methods=["POST"])
def delete_room_done(roomnumber: str = None):
    if not roomnumber:
        return Div("กรุณากรอกหมายเลขห้อง", cls="text-red-500")
    try:
        room_list = [x.strip() for x in roomnumber.split(",") if x.strip()]
        # ส่งเป็น query string หลายตัว
        params = [("roomnumber", r) for r in room_list]
        resp = requests.delete(f"{API_URL}/delete-room", params=params)
        data = resp.json()
        if resp.status_code != 200:
            return Div(f"เกิดข้อผิดพลาด: {data.get('error', 'Unknown error')}", cls="text-red-500")
        return H1(f"ลบห้อง {', '.join(room_list)} สำเร็จ!", cls="text-green-500")
    except Exception as e:
        return Div(f"เกิดข้อผิดพลาด: {str(e)}", cls="text-red-500")

# --- Search Room ---
@rt("/search-room", methods=["GET"])
def search_room_form():
    return Div(
        Form(
            Input(name="roomnumber", placeholder="เช่น 101,102", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Button("ค้นหาห้อง", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/search-room-done", method="post"
        )
    )

@rt("/search-room-done", methods=["POST"])
def search_room_done(roomnumber: str = None):
    if not roomnumber:
        return Div("กรุณากรอกหมายเลขห้อง", cls="text-red-500")
    try:
        room_list = [x.strip() for x in roomnumber.split(",") if x.strip()]
        params = [("roomnumber", r) for r in room_list]
        resp = requests.get(f"{API_URL}/search-room", params=params)
        data = resp.json()
        if resp.status_code != 200:
            return Div(f"เกิดข้อผิดพลาด: {data.get('error', 'Unknown error')}", cls="text-red-500")
        result = data.get("data", {})
        return Div(
            H1("ผลการค้นหา", cls="text-xl text-white mb-4"),
            *(Div(f"{k}: {v}", cls="text-white") for k, v in result.items())
        )
    except Exception as e:
        return Div(f"เกิดข้อผิดพลาด: {str(e)}", cls="text-red-500")

# --- Sort Room ---
@rt("/sort-room", methods=["GET"])
def sort_room_form():
    return Div(
        Form(
            Button("เรียงลำดับห้อง", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/sort-room-done", method="post"
        )
    )

@rt("/sort-room-done", methods=["POST"])
def sort_room_done():
    try:
        resp = requests.get(f"{API_URL}/sort-room")
        data = resp.json()
        if resp.status_code != 200:
            return Div(f"เกิดข้อผิดพลาด: {data.get('error', 'Unknown error')}", cls="text-red-500")
        sorted_rooms = data.get("sorted_rooms", {})
        return Div(
            H1("ห้องที่เรียงแล้ว", cls="text-xl text-white mb-4"),
            *(Div(f"{k}: {v}", cls="text-white") for k, v in sorted_rooms.items())
        )
    except Exception as e:
        return Div(f"เกิดข้อผิดพลาด: {str(e)}", cls="text-red-500")
