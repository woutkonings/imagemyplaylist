from .flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "3ddb444f64434d81929090cdadd76b3d"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "2ce0f93bbcf84328830798bbe7f1e014"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://127.0.0.1"
PATH = "spotify_auth/callback/"
#Add needed scope from spotify user
SCOPE = "playlist-modify-private user-read-currently-playing"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/{}".format(CALLBACK_URL, PORT, PATH), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/{}".format(CALLBACK_URL, PORT, PATH))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA