import os
import datetime
import plaid
from flask import jsonify


def transactions(access_token, client):
    #start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
    #end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
    start_date = '2017-09-12'
    end_date = '2017-09-20'

    response = client.Transactions.get(access_token, start_date=start_date, end_date=end_date)
    return response['transactions'][0]

def accounts(access_token, client):
    accounts = client.Auth.get(access_token)
    return jsonify(accounts)

def item(access_token, client):
    item_response = client.Item.get(access_token)
    institution_response = client.Institutions.get_by_id(item_response['item']['institution_id'])
    return jsonify({'item': item_response['item'], 'institution': institution_response['institution']})
