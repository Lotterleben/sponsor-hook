#!/usr/bin/env python3
import json
import requests
from bottle import route, run, template, request

# Authentication for the user who is adding the sponsor.
USERNAME = '' # read from config.json
API_KEY = ''  # read from config.json

# NOTE:
# - Webhook contenttype must be set to `application/json`
# - `config.json` must contain github credentials (see `config.json.sample`)

ORG_API_URL = 'https://api.github.com/orgs/congenial-guacamole-org/'

# TODO. also mention username for log readig convenience
def add_sponsor(invitee_id: int):
    print('adding sponsor with id', id)

    invitations_endpoint = ORG_API_URL + 'invitations'

    session = requests.Session()
    session.auth = (USERNAME, API_KEY)

    invitation = {'invitee_id': invitee_id,
                  'role': 'direct_member'} # TODO: add team ids

    result = session.post(invitations_endpoint, json.dumps(invitation))
    if result.status_code == 201:
        print('Successfully added sponsor "%s"' % invitee_id)
    else:
        print('Failed to add sponsor "%s"' % invitee_id)
        print('Response:', result.content)


@route('/payload', method=['GET', 'POST'])
def index():
    print("got request: ")
    print(request)

    if request.method == 'POST':
        # TODO https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks
        # TODO Check if the POST request is from github.com

        payload = request.json

        if payload['action'] == 'created':
            # only take action when a new sponsorship is created

            # TODO pull info from payload['sponsorship']['sponsor']['id'] instead
            sender_gh_user_id = payload['sender']['id']
            print("our new sponsor is: ", sender_gh_user_id)

            add_sponsor(sender_gh_user_id)

            return 'OK'

    # DELETEME only for debugging
    elif request.method == 'GET':
        sender_gh_user_id = 581552 # my own id to prevent spamming anoyne
        add_sponsor(sender_gh_user_id)

if __name__ == '__main__':
    with open('config.json', 'r') as config:
        config_json = json.loads(config.read())
        USERNAME = config_json['username']
        API_KEY = config_json['api_key']
    # TODO add nice error msg if config is missing

    # start server
    run(host='localhost', port=4567)

