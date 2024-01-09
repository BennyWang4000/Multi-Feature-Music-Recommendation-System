from flask import Flask, redirect, request

app = Flask(__name__)


@app.route('/authorize')
def authorize():
    # Construct the Spotify authorization URL
    spotify_auth_url = (
        'https://accounts.spotify.com/authorize'
        '?response_type=code'
        '&client_id=94dccbe6ffcf40ed9d14b9bb614a3d5c'
        '&redirect_uri=http://localhost:5000/callback'  # Your redirect URI
    )
    return redirect(spotify_auth_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization code from the callback URL
    authorization_code = request.args.get('code')
    
    # Perform token exchange using the obtained authorization code (as described in the previous response)
    
    return f'Authorization Code: {authorization_code}'

if __name__ == '__main__':
    app.run(port=5000)
