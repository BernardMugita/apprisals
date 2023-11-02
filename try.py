from flask import *
from flask_cors import CORS
import user_funcs

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Py is running'

@app.route("/users/getbyid", methods=['POST'])
def getuserbyid():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            id = request.json.get('id') # provide ID of user to get
            users = user_funcs.get_user_by_id(id, usr["organization"]) 
            return users
    else:
        return "Invalid Token" 

if __name__ == '__main__':
    app.run(port=8001)

