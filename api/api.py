import json
from urllib.request import urlopen
from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from flask_cors import CORS
from jose import jwt
from auth0.v3.authentication import Users
from authlib.flask.client import OAuth


AUTH0_CLIENT_ID = 's6QObRx1RW7p8Ih4df6P7rHOYLiEbktH'
AUTH0_CLIENT_SECRET = 'k14gF9ZpcCxY94DBHizR-b_M_wlLO47fLkGcBZadCRymC-z0E9K_AyWiQJ8KQtza'
AUTH0_DOMAIN = 'onilaes.auth0.com'
AUTH0_BASE_URL = "https://" + AUTH0_DOMAIN
API_AUDIENCE = 'https://ternovka.onilaes.com/auth'
ALGORITHMS = ["RS256"]
app = Flask(__name__)
CORS(app)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError as e:
                print(e)
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            users = Users(AUTH0_DOMAIN)
            user = users.userinfo(token)
            print(user)
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


@app.route("/api")
# @cross_origin(headers=['Content-Type', 'Authorization'])
def hello2():
    return "Hello World API!"


@app.route("/api/public")
# @cross_origin(headers=['Content-Type', 'Authorization'])
def hello3():
    return "Hello World Public!"


@app.route("/api/private")
# @cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def hello4():
    return "Hello World Private!"


if __name__ == '__main__':
    print('> entered application api.main')
    app.debug = False
    app.run(host="0.0.0.0", port=3000)
