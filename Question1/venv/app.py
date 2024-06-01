from flask import Flask, jsonify
import requests
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)
unique_numbers = set()

ID_TO_ENDPOINT = {
    'p': 'prime',
    'f': 'fibonacci',
    'r': 'random',
    'e': 'even'
}

BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE3MjE5NTI0LCJpYXQiOjE3MTcyMTkyMjQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjQ3NzU4NDdiLTUxNWItNDU3Yy1hNjQ5LTdlOWM5NTdkYzRiYyIsInN1YiI6InNhcnRoYWsuMjEyNWNzbWUxMDIxQGtpZXQuZWR1In0sImNvbXBhbnlOYW1lIjoiRGVtb1NvbCIsImNsaWVudElEIjoiNDc3NTg0N2ItNTE1Yi00NTdjLWE2NDktN2U5Yzk1N2RjNGJjIiwiY2xpZW50U2VjcmV0IjoiSmd3RUFRUmp4a3pVVWdmciIsIm93bmVyTmFtZSI6IlNhcnRoYWsgRHViZXkiLCJvd25lckVtYWlsIjoic2FydGhhay4yMTI1Y3NtZTEwMjFAa2lldC5lZHUiLCJyb2xsTm8iOiIyMTAwMjkxNTMwMDQ4In0.B_hxPj2WQPhye-SxvOEIidWIoWPW6tbjZA0HNkJTdgY'

def fetch_numbers(qualified_id):
    endpoint = ID_TO_ENDPOINT.get(qualified_id)
    if not endpoint:
        return []
    
    url = f"20.244.56.144/test/{qualified_id}"
    try:
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        response = requests.get(url, headers=headers, timeout=0.5)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.RequestException:
        return []
    return []

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<qualified_id>', methods=['GET'])
def get_numbers(qualified_id):
    if qualified_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    window_prev_state = list(window)

    new_numbers = fetch_numbers(qualified_id)

    for number in new_numbers:
        if number not in unique_numbers:
            if len(window) >= WINDOW_SIZE:
                oldest = window.popleft()
                unique_numbers.remove(oldest)
            window.append(number)
            unique_numbers.add(number)

    window_curr_state = list(window)
    avg = calculate_average(window_curr_state)

    return jsonify({
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    })

