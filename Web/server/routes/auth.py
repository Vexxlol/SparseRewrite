from flask import Blueprint, request, render_template, redirect, session, make_response, jsonify
from misc.oauth import Oauth
router = Blueprint("auth", __name__)


import misc.jsonHandler as jh
dev = jh.read_json("mode.json")
dev = dev['dev']
@router.route("/auth", methods=["post"])
def index():
    if request.args.get("code") is None:
        d = {"data": "INVALID"}
        return jsonify(d)
    else:
        code = request.args.get("code")
        access_token = Oauth.get_access_token(code)
        responsee = {"data": access_token}
        return jsonify(responsee)
