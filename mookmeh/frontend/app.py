# frontend/app.py
from fasthtml.common import *
import requests

app, rt = fast_app(hdrs=(
    # Tailwind CSS
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
    # SweetAlert2
    Script(src="https://cdn.jsdelivr.net/npm/sweetalert2@11"),
    # Custom SweetAlert2 Theme (dark)
    Style("""
    .swal2-popup {
        background: linear-gradient(to bottom right, #0f172a, #1e293b, #312e81) !important;
        color: #e0e7ff !important;
        border-radius: 1rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }
    .swal2-title {
        font-weight: bold !important;
        color: #93c5fd !important;
        font-size: 1.4rem !important;
    }
    .swal2-html-container {
        font-size: 1rem !important;
        color: #cbd5e1 !important;
    }
    .swal2-confirm {
        background: linear-gradient(to right, #2563eb, #7c3aed) !important;
        color: white !important;
        border-radius: 0.75rem !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
    }
    .swal2-cancel {
        background: linear-gradient(to right, #ef4444, #dc2626) !important;
        color: white !important;
        border-radius: 0.75rem !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
    }
    """),
))

API_URL = "http://127.0.0.1:8001"

# --- Main Page ---
@rt("/")
def main_page():
    return Div(
        Div(
            H1("Hilbert's Hotel", cls="text-4xl font-bold mb-6 text-center text-white drop-shadow-lg"),
            Form(
                Input(name="old_guess", placeholder="old guest amount", required=True,
                      cls="block w-full mb-3 p-3 rounded bg-gray-800 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400"),
                Input(name="chanel", placeholder="new channel", required=True,
                      cls="block w-full mb-3 p-3 rounded bg-gray-800 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400"),
                Input(name="max", placeholder="max channel", required=True,
                      cls="block w-full mb-6 p-3 rounded bg-gray-800 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400"),
                Button("SUBMIT", type="submit",
                       cls="w-full py-3 rounded bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold hover:opacity-90 transition"),
                action="/hotel", method="post"
            ),
            cls="bg-black/70 p-8 rounded-2xl shadow-2xl w-full max-w-md"
        ),
        cls="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-blue-900 p-6"
    )

# --- Hotel POST ---
@rt("/hotel", methods=["POST"])
def hotel_page(old_guess: str = None, chanel: str = None, max: str = None):
    try:
        resp = requests.post(f"{API_URL}/create-data", json={
            "old_guess": old_guess,
            "chanel": chanel,
            "max": max
        })
        resp.raise_for_status()
        data = resp.json()
        used_time = data.get("time", "N/A")
        used_mem = data.get("memory", "N/A")
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'old_guess: <b>{old_guess}</b><br>'
                     + 'chanel: <b>{chanel}</b><br>'
                     + 'max: <b>{max}</b><br><br>'
                     + 'Time: <b>{used_time}</b><br>'
                     + 'Memory: <b>{used_mem}</b>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
    except Exception as e:
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to create data.<br><small>{str(e)}</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/";
            }});
        """)

# --- Action Page ---
@rt("/action", methods=["GET"])
def action_page():
    return Div(
        Div(
            H1("Hotel Actions", cls="text-4xl font-bold mb-8 text-center text-white drop-shadow-lg"),
            Div(
                A("Add Room", href="/add-room",
                  cls="block w-full mb-4 py-3 px-4 rounded bg-gradient-to-r from-green-500 to-emerald-600 text-white text-center font-medium hover:opacity-90 transition"),
                A("Delete Room", href="/delete-room",
                  cls="block w-full mb-4 py-3 px-4 rounded bg-gradient-to-r from-red-500 to-pink-600 text-white text-center font-medium hover:opacity-90 transition"),
                A("Search Room", href="/search-room",
                  cls="block w-full mb-4 py-3 px-4 rounded bg-gradient-to-r from-yellow-500 to-orange-600 text-white text-center font-medium hover:opacity-90 transition"),
                A("Sort Room", href="/sort-room",
                  cls="block w-full mb-4 py-3 px-4 rounded bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-center font-medium hover:opacity-90 transition"),
                cls="max-w-md mx-auto"
            ),
            cls="bg-black/70 p-10 rounded-2xl shadow-2xl w-full max-w-lg"
        ),
        cls="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-blue-900 p-6"
    )

# --- Styled Form Helper ---
def styled_form(title, placeholder, action, button_text, btn_color):
    return Div(
        Div(
            H1(title, cls="text-3xl font-semibold mb-6 text-center text-white"),
            Form(
                Input(name="roomnumber", placeholder=placeholder, required=True,
                      cls="block w-full mb-6 p-3 rounded bg-gray-800 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-400"),
                Button(button_text, type="submit",
                       cls=f"w-full py-3 rounded {btn_color} text-white font-semibold hover:opacity-90 transition"),
                action=action, method="post"
            ),
            cls="bg-black/70 p-8 rounded-2xl shadow-xl w-full max-w-md"
        ),
        cls="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-blue-900 p-6"
    )

# --- Add/Delete/Search/Sort Pages ---
@rt("/add-room", methods=["GET"])
def add_room(): 
    return styled_form("Add Room", "เช่น 101,102,103 (text)", "/add-room-done", "ADD", "bg-gradient-to-r from-green-500 to-emerald-600")

@rt("/delete-room", methods=["GET"])
def delete_room_form(): 
    return styled_form("Delete Room", "เช่น 101,102 (text)", "/delete-room-done", "DELETE", "bg-gradient-to-r from-red-500 to-pink-600")

@rt("/search-room", methods=["GET"])
def search_room_form(): 
    return styled_form("Search Room", "เช่น 101,102 (text)", "/search-room-done", "SEARCH", "bg-gradient-to-r from-yellow-500 to-green-600")

@rt("/sort-room", methods=["GET"])
def sort_room_form():
    return Div(
        Div(
            H1("Sort Rooms", cls="text-3xl font-semibold mb-6 text-center text-white"),
            Form(
                Button("SORT", type="submit",
                       cls="w-full py-3 rounded bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold hover:opacity-90 transition"),
                action="/sort-room-done", method="post"
            ),
            cls="bg-black/70 p-8 rounded-2xl shadow-xl w-full max-w-md"
        ),
        cls="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-blue-900 p-6"
    )

# --- Add Room POST ---
@rt("/add-room-done", methods=["POST"])
def add_room_done(roomnumber: str = None):
    try:
        resp = requests.post(f"{API_URL}/add-room", json={"roomnumber": roomnumber})
        resp.raise_for_status()
        data = resp.json()
        used_time = data.get("time", "N/A")
        used_mem = data.get("memory", "N/A")
        return Script(f"""
            Swal.fire({{
                title: 'Room Added!',
                html: 'add room <b>{roomnumber}</b> successfully!<br>'
                     + 'Time: <b>{used_time}</b><br>'
                     + 'Memory: <b>{used_mem}</b>',
                icon: 'success',
                confirmButtonText: 'Go Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
    except Exception as e:
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to add room.<br><small>{str(e)}</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/add-room";
            }});
        """)

# --- Delete Room POST ---
@rt("/delete-room-done", methods=["POST"])
def delete_room_done(roomnumber: str = None):
    try:
        resp = requests.delete(f"{API_URL}/delete-room", params={"roomnumber": roomnumber})
        resp.raise_for_status()
        data = resp.json()
        used_time = data.get("time", "N/A")
        used_mem = data.get("memory", "N/A")
        return Script(f"""
            Swal.fire({{
                title: 'Room Deleted!',
                html: 'delete room <b>{roomnumber}</b> successfully!<br>'
                     + 'Time: <b>{used_time}</b><br>'
                     + 'Memory: <b>{used_mem}</b>',
                icon: 'warning',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
    except Exception as e:
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to delete room.<br><small>{str(e)}</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/delete-room";
            }});
        """)

# --- Search Room POST ---
@rt("/search-room-done", methods=["POST"])
def search_room_done(roomnumber: str = None):
    try:
        resp = requests.get(f"{API_URL}/search-room", params={"roomnumber": roomnumber})
        resp.raise_for_status()
        data = resp.json()
        used_time = data.get("time", "N/A")
        used_mem = data.get("memory", "N/A")
        found = data.get("found", False)
        msg = f"room <b>{roomnumber}</b> found!" if found else f"room <b>{roomnumber}</b> not found!"
        return Script(f"""
            Swal.fire({{
                title: 'Search Result',
                html: '{msg}<br>Time: <b>{used_time}</b><br>Memory: <b>{used_mem}</b>',
                icon: 'info',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
    except Exception as e:
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Search failed.<br><small>{str(e)}</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/search-room";
            }});
        """)

# --- Sort Room POST ---
@rt("/sort-room-done", methods=["POST"])
def sort_room_done():
    try:
        resp = requests.get(f"{API_URL}/sort-room")
        resp.raise_for_status()
        data = resp.json()
        used_time = data.get("time", "N/A")
        used_mem = data.get("memory", "N/A")
        sorted_rooms = data.get("sorted_rooms", [])
        return Script(f"""
            Swal.fire({{
                title: 'Rooms Sorted!',
                html: 'sort room successfully!<br>'
                     + 'Time: <b>{used_time}</b><br>'
                     + 'Memory: <b>{used_mem}</b><br>'
                     + 'Sorted Rooms: <b>{', '.join(map(str, sorted_rooms))}</b>',
                icon: 'success',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
    except Exception as e:
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Sorting failed.<br><small>{str(e)}</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/sort-room";
            }});
        """)
