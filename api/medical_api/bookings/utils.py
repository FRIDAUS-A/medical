import requests
import base64

# Replace with your Zoom app credentials
ZOOM_CLIENT_ID = "ebnuIdJJR_GGk5WSU_1lQ"
ZOOM_CLIENT_SECRET = "FqVjpxvkLRMe47eifI93T9fhW0Ul1hIT"

def get_zoom_access_token():
    """
    Generate an OAuth access token using Server-to-Server OAuth.
    """
    url = "https://zoom.us/oauth/token"
    credentials = f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get Zoom token: {response.json()}")

def create_zoom_meeting(doctor_name):
    """
    Create a Zoom meeting for a consultation with the given doctor name.
    """
    # Get the access token
    access_token = get_zoom_access_token()
    print(access_token)

    # Zoom API endpoint for creating a meeting
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "topic": f"Consultation with {doctor_name}",
        "type": 2,  # Scheduled meeting
        "start_time": "2025-01-02T10:00:00Z",  # ISO format
        "duration": 30,  # 30 minutes
        "settings": {
            "join_before_host": False,
            "waiting_room": True
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()["join_url"]
    else:
        raise Exception(f"Failed to create meeting: {response.json()}")
