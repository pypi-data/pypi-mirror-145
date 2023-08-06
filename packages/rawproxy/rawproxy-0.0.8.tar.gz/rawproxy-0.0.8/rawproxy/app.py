from flask import Flask, make_response, request
import requests

app = Flask(__name__)


@app.route("/raw.githubusercontent.com/<path:subpath>")
def proxy(subpath):
    print(request.url)
    r = requests.get(f"https:/{request.full_path}")
    resp = make_response(r.text)
    resp.content_type = "text/plain; charset=utf-8"
    return resp
