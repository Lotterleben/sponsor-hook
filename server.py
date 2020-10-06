#!/usr/bin/env python3
import hashlib
import hmac
import json
import requests
from bottle import Bottle, route, run, template, request

# Authentication for the user who is adding the sponsor.
USERNAME = ''      # read from config.json
API_KEY = ''       # read from config.json
SECRET_TOKEN = b'' # read from config.json

TARGET_EVENT = 'issue_comment' # TODO change to 'sponsorship'

# NOTE:
# - Webhook contenttype must be set to `application/json`
# - `config.json` must contain github credentials (see `config.json.sample`)
# - generate and set `secret_token` in config as described in
#   https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks
# - TODO add requirements.txt for dependency installation

ORG_API_URL = 'https://api.github.com/orgs/congenial-guacamole-org/'

app = Bottle()

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


def verify_signature(payload_body: bytes, x_hub_signature: str) -> bool:
    h = hmac.new(SECRET_TOKEN, payload_body, hashlib.sha1)
    signature = 'sha1=' + h.hexdigest()

    print("received signature:", x_hub_signature)
    print("computed signature:", signature)

    return hmac.compare_digest(signature, x_hub_signature)


@app.route('/payload', method=['GET', 'POST'])
def index():
    print("got request: ")
    print(request)

    # check signature before everything else
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if x_hub_signature == None:
        print('missing signature, ignoring request')
        return '401 Unauthorized'
    signature_valid = verify_signature(request.body.getvalue(), x_hub_signature)
    if signature_valid == False:
        print('signature mismatch, ignoring request')
        return '401 Unauthorized'

    # TODO Also check if the sender IP belongs to github.com?

    if request.method == 'POST' and request.headers.get('X-GitHub-Event') == TARGET_EVENT:
        payload = request.json

        # only take action when a new sponsorship is *created*
        if payload['action'] == 'created':
            try:
                # TODO pull info from payload['sponsorship']['sponsor']['id'] instead
                sender_gh_user_id = payload['sender']['id']
                print("our new sponsor is: ", sender_gh_user_id)

                add_sponsor(sender_gh_user_id)

                return '200 OK'
            except:
                print("missing sponsor data (unexpected request type?)")


if __name__ == '__main__':
    with open('config.json', 'r') as config:
        config_json = json.loads(config.read())
        USERNAME = config_json['username']
        API_KEY = config_json['api_key']
        SECRET_TOKEN = bytearray(config_json['secret_token'], 'utf-8')

    # start server
    run(app, host='localhost', port=4567)

