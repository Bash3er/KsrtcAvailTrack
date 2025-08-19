import time
import requests
from datetime import datetime
import pyttsx3

# Config
FROM_CITY_ID = 298
TO_CITY_ID = 445
FROM_CITY_NAME = "Bangalore"
TO_CITY_NAME = "Kollam"
JOURNEY_DATE = "2025-08-25"  # YYYY-MM-DD
CHECK_INTERVAL = 5  # seconds

# Voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def check_seats():
    url = "https://onlineksrtcswift.com/api/resource/searchRoutesV4"
    params = {
        "fromCityID": FROM_CITY_ID,
        "toCityID": TO_CITY_ID,
        "fromCityName": FROM_CITY_NAME,
        "toCityName": TO_CITY_NAME,
        "journeyDate": JOURNEY_DATE,
        "mode": "oneway"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://onlineksrtcswift.com/",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

    data = r.json()

    # Ensure buses list is extracted
    buses = []
    if isinstance(data, list):
        buses = data
    elif isinstance(data, dict):
        buses = data.get("data", [])

    found = False
    for bus in buses:
        seats = bus.get("AvailableSeats", 0)  # Correct key
        service = bus.get("ServiceType", "Unknown Service")  # Correct key
        departure = bus.get("DepartureTime", "")
        arrival = bus.get("ArrivalTime", "")
        if seats > 0:
            message = f"🚨 Seat available in {service}: {seats} seats. Departure: {departure}, Arrival: {arrival}"
            print(message)
            speak(message)
            found = True

    if not found:
        print(f"[{datetime.now()}] No seats available for {JOURNEY_DATE}")
        # return True

    return found

if __name__ == "__main__":
    while True:
        if check_seats():
            break
        time.sleep(CHECK_INTERVAL)
