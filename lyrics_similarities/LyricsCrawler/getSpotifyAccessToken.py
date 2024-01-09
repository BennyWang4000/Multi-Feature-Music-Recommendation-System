import requests

SPOTIFY_CLIENT_ID = '94dccbe6ffcf40ed9d14b9bb614a3d5c'
SPOTIFY_CLIENT_SECRET = '4cfe542a2f19452cb5a0dc853dec046a'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORIZATION_CODE = 'AQA3F9y85yaEJ79_6VgQAYENvyJ0tukFEl0C6qGC_i5KoikVbczCLViXsKlJFFSShpsJGO3acY-LDNI7yvEGF6CHRRDkuH0zSz5eMrMvy4_T6VoYj2ZiTxgvkYaUy0sca8_CpzuIXeZwgyFR4Z7bWBsSGNoZDlWzaAzRrrGcoyxQlA'

auth_url = 'https://accounts.spotify.com/api/token'
auth_data = {
    'grant_type': 'authorization_code',
    'code': AUTHORIZATION_CODE,
    'redirect_uri': REDIRECT_URI,
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
}

auth_response = requests.post(auth_url, data=auth_data)
auth_response_data = auth_response.json()
print(auth_response_data)

access_token = auth_response_data.get('access_token')
print(access_token)
