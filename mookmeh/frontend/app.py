# frontend/app.py
from fasthtml.common import *
import requests
import json

app, rt = fast_app(hdrs=(
    # Tailwind CSS
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
    # SweetAlert2
    Script(src="https://cdn.jsdelivr.net/npm/sweetalert2@11"),
    # Custom SweetAlert2 
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
        chanel = [i for i in chanel.split()]
        max = [int(i) for i in max.split()]
        if len(max) != len(chanel):
            raise ValueError("Length of max and chanel must be equal")
        
        resp = requests.post(f"{API_URL}/create-data", json={
            "old_guess": int(old_guess),
            "chanel": chanel,
            "max": max
        })
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/";
                }});
            """)
            
        message =  json.dumps(data.get("message"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        insert_time_taken =  json.dumps(data.get("insert_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'message: <b>' + {message} + '</b><br>'
                     + 'insert time taken: <b>' + {insert_time_taken} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to create data.<br><small>' + {error_msg} + '</small>',
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
                Div(
                    Form(
                        Button("Save File",
                               cls="w-full py-3 rounded bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold hover:opacity-90 transition"),
                        action="/save-file-done", method="post",
                        cls="flex-1",
                    ),
                    Form(
                        Button("Current Data Size", 
                               cls="w-full py-3 rounded bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold hover:opacity-90 transition"),
                        action="/data-size-done", method="post",
                        cls="flex-1",
                    ),
                    cls="mt-6 space-x-4 flex"
                ),
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
    return styled_form("Add Room", "EX: 101 102", "/add-room-done", "ADD", "bg-gradient-to-r from-green-500 to-emerald-600")

@rt("/delete-room", methods=["GET"])
def delete_room_form(): 
    return styled_form("Delete Room", "EX: 101 102", "/delete-room-done", "DELETE", "bg-gradient-to-r from-red-500 to-pink-600")

@rt("/search-room", methods=["GET"])
def search_room_form(): 
    return styled_form("Search Room", "EX: 101 102", "/search-room-done", "SEARCH", "bg-gradient-to-r from-yellow-500 to-green-600")

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
        roomnumber = [int(i) for i in roomnumber.split()]
        
        resp = requests.post(f"{API_URL}/add-room", json={"roomnumber": roomnumber})
        
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)

        message =  json.dumps(data.get("message"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        insert_time_taken =  json.dumps(data.get("insert_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'message: <b>' + {message} + '</b><br>'
                     + 'insert time taken: <b>' + {insert_time_taken} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to add room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)

# --- Delete Room POST ---
@rt("/delete-room-done", methods=["POST"])
def delete_room_done(roomnumber: str = None):
    try:
        roomnumber = [int(i) for i in roomnumber.split()]
        
        resp = requests.delete(f"{API_URL}/delete-room", params={"roomnumber": roomnumber})
        
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)

        message =  json.dumps(data.get("message"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        delete_time_taken =  json.dumps(data.get("delete_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'message: <b>' + {message} + '</b><br>'
                     + 'delete time taken: <b>' + {delete_time_taken} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to delete room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)

# --- Search Room POST ---
@rt("/search-room-done", methods=["POST"])
def search_room_done(roomnumber: str = None):
    try:
        roomnumber = [int(i) for i in roomnumber.split()]
        
        resp = requests.get(f"{API_URL}/search-room", params={"roomnumber": roomnumber})
        
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)

        results =  json.dumps(data.get("results"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        search_time_taken =  json.dumps(data.get("search_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'results: <b>' + {results} + '</b><br>'
                     + 'search time taken: <b>' + {search_time_taken} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to search room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)

# --- Sort Room POST ---
@rt("/sort-room-done", methods=["POST"])
def sort_room_done():
    try:
        resp = requests.get(f"{API_URL}/sort-room")
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)
            
        sorted_rooms =  json.dumps(data.get("sorted_rooms"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        sort_time_taken =  json.dumps(data.get("sort_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'sorted_rooms: <b>' + {sorted_rooms} + '</b><br>'
                     + 'sort time taken: <b>' + {sort_time_taken} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to sort room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
@rt("/data-size-done", methods=["POST"])
def sort_room_done():
    try:
        resp = requests.get(f"{API_URL}/data-size")
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)
            
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        data_size = json.dumps(data.get("data_size", "N/A"))

        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'current data size: <b>' + {data_size} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to sort room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
@rt("/save-file-done", methods=["POST"])
def sort_room_done():
    try:
        resp = requests.get(f"{API_URL}/save-file")
        try:
            resp.raise_for_status()  
            data = resp.json()
        except requests.exceptions.HTTPError:
            try:
                error_data = resp.json()
                error_msg =  json.dumps(error_data.get("error"))
            except Exception:
                error_msg =  json.dumps("Unknown error from API")
            return Script(f"""
                Swal.fire({{
                    title: 'API Error!',
                    html: {error_msg},
                    icon: 'error',
                    confirmButtonText: 'Back'
                }}).then(() => {{
                    window.location.href = "/action";
                }});
            """)
            
        message =  json.dumps(data.get("message"))
        all_time_taken =  json.dumps(data.get("all_time_taken", "N/A"))
        
        return Script(f"""
            Swal.fire({{
                title: 'Success!',
                html: 'Input sent to backend:<br>'
                     + 'message: <b>' + {message} + '</b><br>'
                     + 'all time taken: <b>' + {all_time_taken} + '</b><br><br>',
                icon: 'success',
                confirmButtonText: 'OK'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
        
    except Exception as e:
        error_msg = json.dumps(str(e))
        return Script(f"""
            Swal.fire({{
                title: 'Error!',
                html: 'Failed to sort room.<br><small>' + {error_msg} + '</small>',
                icon: 'error',
                confirmButtonText: 'Back'
            }}).then(() => {{
                window.location.href = "/action";
            }});
        """)
