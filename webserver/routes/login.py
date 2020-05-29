from flask import Blueprint, request, render_template, redirect, session, make_response
from misc.oauth import Oauth
router = Blueprint("login", __name__)

import misc.jsonHandler as jh
dev = jh.read_json("mode.json")
dev = dev['dev']
@router.route("/", methods=["post"])
def index():
    if "oauth" in request.cookies:
        # magic
        return redirect('/account')
    else:
        if dev == True:
            return redirect(Oauth.discord_login_url_dev)
        else:
            return redirect(Oauth.discord_login_url)
