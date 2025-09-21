# frontend/app.py
from fasthtml.common import *
import requests

app, rt = fast_app()

API_URL = "http://127.0.0.1:8000/create-data"   # backend API

@rt("/")
def main_page():
    return Div(
        H1("Infinite HOTEL", cls="text-white text-3xl mb-6 text-center"),
        Form(
            Input(name="guests", placeholder="จำนวนแขกเดิม", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Input(name="paths", placeholder="จำนวนแขกแต่ละช่องทาง", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Input(name="channel", placeholder="หมายเลขช่องทาง", required=True,
                  cls="block w-full mb-3 p-2 rounded bg-red-900 text-white"),
            Button("SUBMIT", type="submit",
                   cls="bg-gray-600 text-white px-6 py-2 rounded"),
            action="/hotel", method="post"
        ),
        cls="min-h-screen flex items-center justify-center bg-black p-10"
    )

@rt("/hotel")
def hotel_page(guests: int, paths: int, channel: int):
    # เรียก backend API
    resp = requests.post(API_URL, json={
        "guests": guests,
        "paths": paths,
        "channel": channel
    })
    data = resp.json()

    return Div(
        H1("HOTEL", cls="text-white text-3xl mb-6 text-center"),
        P(f"Result: {data['result']}", cls="text-white text-lg"),
        P(f"TIME SPENT: {data['time_spent']}", cls="text-white text-lg"),
        P(f"MEMORIES SPENT: {data['memories_spent']}", cls="text-white text-lg"),
        cls="min-h-screen flex flex-col items-center justify-center bg-black p-10"
    )
