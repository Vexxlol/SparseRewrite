from flask import Blueprint, render_template, jsonify

router = Blueprint("index", __name__)

@router.route("/", methods=["get"])
def index():
    d = {"data": "fuck off!"}
    return jsonify(d)
