import os
import datetime
import plaid
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = '59bf7ecebdc6a40ac87ed156'
PLAID_SECRET = '764ae7923ee6a06817d6b55ce69464'
PLAID_PUBLIC_KEY = 'f8bc11ee98572a8a89506b01ec69e5'
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV='sandbox'

client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

access_token = "access-sandbox-b70ad85b-6a99-4cbf-a48b-367a5d198a14"

def accounts():
    accounts = client.Auth.get(access_token)
    return jsonify(accounts)

def item():
    item_response = client.Item.get(access_token)
    institution_response = client.Institutions.get_by_id(item_response['item']['institution_id'])
    return jsonify({'item': item_response['item'], 'institution': institution_response['institution']})
