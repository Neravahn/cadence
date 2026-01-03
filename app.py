from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth/github')
def gihub_login():
    github_authorize_url = "https://github.com/login/oauth/authorize"
    redirect_uri = url_for('github_callback', _external = True)
    return redirect(f"{github_authorize_url}?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=user:email")

@app.route('/auth/github/callback')
def github_callback():
    code = request.args.get("code")
    if not code:
        return "Authorisation Failed : 400" #WILL ADD A ERROR 400 PAGE HERE
    

    token_url = 'https://github.com/login/oauth/access_token'
    headers = {"Accept" : "application/json"}
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }

    token_res = requests.get(token_url, headers=headers, data=data).json()
    access_token = token_res.get("access_token")

    if not access_token:
        return "Failed to get the access token" #WILL ADD A CUSTOM PAGE HEERE
    


    #FETCHING USER INFO
    user_res = requests.get("https://api.github.com/user", headers={
        "Authorization": f"token {access_token}"
    }).json()


    email_res = requests.get("https://api.github.com/user/emails", headers={
        "Authorization": f"token {access_token}"
    }).json()


    primary_email = next((e["email"] for e in email_res if e["primary"]), None)
    email = primary_email
    name = user_res.get("name") or user_res.get("login")
    pic = user_res.get("avatar_url")
    provider = "github"

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return "Dashboard"
    


if __name__ == "__main__":
    app.run(debug=True)

