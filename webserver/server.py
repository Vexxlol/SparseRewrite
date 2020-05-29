from flask import Flask, request, render_template, redirect, session, make_response
from misc.injectENV import bang
bang()
# ROUTE IMPORTS
from routes.index import router as indexRoute
from routes.auth import router as authRoute
from routes.userinfo import router as userRoute
app = Flask(__name__)

app.register_blueprint(indexRoute, url_prefix="/")
app.register_blueprint(authRoute, url_prefix="/auth")
app.register_blueprint(userRoute, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=True,port=int("5000"))
