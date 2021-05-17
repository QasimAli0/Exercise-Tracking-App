import requests

AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = '0a70e192c0ef436b9901456b8f60ee7e'
CLIENT_SECRET = 'cd917a86e4b8453c8350e2476e1c1908'


def get_spotify_access_token():

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']
