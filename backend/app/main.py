from flask import Flask, redirect, url_for, session, request
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from discount import Discount

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/discounts": {"origins": "http://localhost"}
    }
)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id = env.get("AUTH0_CLIENT_ID"),
    client_secret = env.get("AUTH0_CLIENT_SECRET"),
    api_base_url = f"https://{env.get('AUTH0_DOMAIN')}",
    access_token_url = f"https://{env.get('AUTH0_DOMAIN')}/oauth/token",
    authorize_url = f"https://{env.get('AUTH0_DOMAIN')}/authorize",
    client_kwargs = {
        "scope": "openid profile email",
    },
    server_metadata_url = f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    assert auth0 is not None, "Auth0 client is not configured."
    
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True),
        audience=f"https://{env.get('AUTH0_DOMAIN')}/userinfo"
    )

@app.route("/callback")
def callback():
    assert auth0 is not None, "Auth0 client is not configured."

    token = auth0.authorize_access_token()
    userinfo = token.get("userinfo") or token
    session["user"] = userinfo
    return redirect("http://localhost/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("http://localhost/")


@app.route("/discounts")
def discounts():
    if "user" not in session:
        return {"error": "Unauthorized"}, 401

    return {
        "discounts": [
            dict(discount) for discount in get_discounts()
        ]
    }

def get_discounts() -> list[Discount]:
    return [
        Discount("SAVE10", 10.0, "Walmart"),
        Discount("SAVE20", 20.0, "Pepco"),
        Discount("SAVE30", 30.0, "Domino's"),
    ]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)