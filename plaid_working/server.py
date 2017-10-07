import os
import datetime
import plaid
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from helpers import *

app = Flask(__name__)

# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = '59bf7ecebdc6a40ac87ed156'
PLAID_SECRET = '764ae7923ee6a06817d6b55ce69464'
PLAID_PUBLIC_KEY = 'f8bc11ee98572a8a89506b01ec69e5'
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV='development'

client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

@app.route("/")
def index():
   return render_template('index.ejs', plaid_public_key=PLAID_PUBLIC_KEY, plaid_environment=PLAID_ENV)

access_token, public_token = None, None

@app.route("/get_access_token", methods=['POST'])
def get_access_token():
  global access_token
  exchange_response = client.Item.public_token.exchange(request.form['public_token'])
  access_token, item_id = exchange_response['access_token'], exchange_response['item_id']

  transacts = transactions(access_token, client)

  return jsonify(exchange_response)


if __name__ == "__main__":
    app.run()
