import requests
import os
from dotenv import load_dotenv
load_dotenv()

"""
Run this to get the 'twitch_oauth_token' in the .env
Make sure that you add 'oauth' in front of it:

For example: oauth:************************
The asterisk are the oauth you receive.
"""

CLIENT_ID = os.getenv('twitch_client_id')
CLIENT_SECRET = os.getenv('twitch_client_secret')

url = "https://id.twitch.tv/oauth2/token"

params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials"
}

response = requests.post(url, params=params)
data = response.json()

if "access_token" in data:
    print("Access token:", data["access_token"])
else:
    print("Invalid Client ID or Secret")
