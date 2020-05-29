from flask import Blueprint, request, render_template, redirect, session, make_response, jsonify
from misc.oauth import Oauth
router = Blueprint("userInfo", __name__)


import misc.jsonHandler as jh
dev = jh.read_json("mode.json")
dev = dev['dev']
@router.route("/", methods=["post"])
def index():
    d = {}
    if request.args.get("code") is None:
        d = {"data": "INVALID"}
        return jsonify(d)
    else:
        response = Oauth.get_user_object(request.args.get("code"))
        if response == "INVALID":
            d = {"data": "INVALID"}
            return jsonify(d)

        d = {"data" : response}
        print(response)
        return jsonify(d)
        #code = request.args.get("code")
        #access_token = Oauth.get_access_token(code)
        #responsee = {"code": str(access_token)}
        #return jsonify(responsee)
