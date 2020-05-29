import os
import requests

import misc.jsonHandler as js

mode = js.read_json('mode.json')
mode = mode['dev']

class Oauth(object):
    client_id = str(os.getenv("clientId"))
    client_secret = str(os.getenv("clientSecret"))
    scope = "identify"
    redirect_url_dev = "http://127.0.0.1:5000/auth"
    redirect_url = "https://avex.dev/auth"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=697115395504603248&redirect_uri=https%3A%2F%2Favex.dev%2Fauth&response_type=code&scope=identify"
    discord_login_url_dev = "https://discord.com/api/oauth2/authorize?client_id=715526745033539615&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauth&response_type=code&scope=identify"
    discord_token_url = "https://discordapp.com/api/oauth2/token"
    discord_api_url = "https://discordapp.com/api/"

    @staticmethod
    def get_access_token(code):
        if mode == True:
            payload = {
                'client_id': Oauth.client_id,
                'client_secret': Oauth.client_secret,
                'grant_type': 'authorization_code',
                'code':code,
                'redirect_uri':Oauth.redirect_url_dev,
                'scope':Oauth.scope
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            r = requests.post(url=Oauth.discord_token_url, data=payload, headers=headers)
            json = r.json()
            if json.get('access_token') is None:
                return "invalid code"
            return str(json.get("access_token"))
        else:
            payload = {
                'client_id': Oauth.client_id,
                'client_secret': Oauth.client_secret,
                'grant_type': 'authorization_code',
                'code':code,
                'redirect_uri':Oauth.redirect_url,
                'scope':Oauth.scope
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            r = requests.post(url=Oauth.discord_token_url, data=payload, headers=headers)
            json = r.json()
            print(json)
            if json.get('access_token') is None:
                return "invalid code"
            return json


    @staticmethod
    def get_user_object(code):
        url = Oauth.discord_api_url + "users/@me"
        headers = {'Authorization': 'Bearer {}'.format(code)}
        user_object = requests.get(url=url, headers=headers)
        user_json = user_object.json()

        if user_json.get('username') is None:
            return "INVALID"

        return user_json
