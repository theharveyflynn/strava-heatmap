import os
import requests

CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]

def get_access_token():
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    return response.json()["access_token"]


from stravalib.client import Client
import json
import os

CLIENT_ID = 192179
CLIENT_SECRET = "ebcf36ca8e0f7ec9fcac5ccc8879ca4d9760397f"

client = Client()

# Step 1: Ask user to authorize
print("Go to this URL and authorize the app:")
auth_url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri='http://localhost',
        scope=['activity:read_all']
)
print(auth_url)

# Step 2: Paste the code Strava gives you
code = input("Enter the code from the URL: ")

# Step 3: Exchange code for token
token_response = client.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
)

access_token = token_response['access_token']
client.access_token = access_token

# Step 4: Download ALL Activities (correct pagination with datetime)
import os

os.makedirs("activities", exist_ok=True)

before = None
total_saved = 0

while True:
    print(f"Fetching activities before: {before}")

    # Pass before as a datetime, not an int
    activities = client.get_activities(limit=200, before=before)
    activities_list = list(activities)

    if not activities_list:
        print("No more activities found.")
        break

    for activity in activities_list:
        streams = client.get_activity_streams(activity.id, types=['latlng'])

        if streams is None:
            continue

        if 'latlng' not in streams:
            continue

        filename = f"activities/{activity.id}.json"
        with open(filename, "w") as f:
            json.dump(streams['latlng'].data, f)

        total_saved += 1
        print(f"Saved {filename}")

    # Move the "before" cursor backward in time
    last_activity = activities_list[-1]
    before = last_activity.start_date  # <-- keep as datetime

print(f"Done! Saved {total_saved} GPS activities.")

