#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import requests
import sys
from bottle import Bottle, route, run, template, request

# TODO add "hi we're live, point your webhooks to '/payload'" at / for nicer deploying

TARGET_EVENT = 'sponsorship'
TEAM_API_URL = 'https://api.github.com/orgs/knurling-rs/'
KNURLING_SPONSORS_TEAM_ID = 3991575

app = Bottle()

def get_env_config():
    try:
        USERNAME = os.environ['USERNAME']
        API_KEY = bytes(os.environ['API_KEY'], "utf-8")
        SECRET_TOKEN = bytes(os.environ['SECRET_TOKEN'], "utf-8")

        return USERNAME, API_KEY, SECRET_TOKEN
    except KeyError as key:
        # todo add hint that you can set this in
        # https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-central-1#/functions/sponsor-hook-dev?tab=configuration
        # or locally if you're just testing there
        sys.exit("ERROR: environment variable " + str(key) + " not set. Shutting down")

# TODO. also mention username for log readig convenience
# note that `USERNAME` is the auth user, not the user to be added to the repo!
def add_sponsor(invitee_id: int, USERNAME: str, API_KEY: bytes):
    print('adding sponsor with id:', id)

    # see https://docs.github.com/en/free-pro-team@latest/rest/reference/orgs
    invitations_endpoint = TEAM_API_URL + 'invitations'

    session = requests.Session()
    session.auth = (USERNAME, API_KEY)

    invitation = {'invitee_id': invitee_id,
                  'role': 'direct_member',
                  'team_ids': [KNURLING_SPONSORS_TEAM_ID]}

    result = session.post(invitations_endpoint, json.dumps(invitation))
    if result.status_code == 201:
        print('Successfully added sponsor "%s"' % invitee_id)
    else:
        print('Failed to add sponsor "%s"' % invitee_id)
        print('Response:', result.content)


def verify_signature(payload_body: bytes, x_hub_signature: str, SECRET_TOKEN: bytes) -> bool:
    # make sure config is set
    assert(SECRET_TOKEN != b'')

    h = hmac.new(SECRET_TOKEN, payload_body, hashlib.sha1)
    signature = 'sha1=' + h.hexdigest()

    print("received signature:", x_hub_signature)
    print("computed signature:", signature)

    return hmac.compare_digest(signature, x_hub_signature)


@app.route('/payload', method=['GET', 'POST'])
def index():
    print("got request: ")
    print(request)

    # make sure we have all of our access credentials
    USERNAME, API_KEY, SECRET_TOKEN = get_env_config()

    # check signature before everything else
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if x_hub_signature == None:
        print('missing signature, ignoring request')
        return '401 Unauthorized'
    signature_valid = verify_signature(request.body.getvalue(), x_hub_signature, SECRET_TOKEN)
    if signature_valid == False:
        print('signature mismatch, ignoring request')
        return '401 Unauthorized'

    # TODO Also check if the sender IP belongs to github.com?

    if request.method == 'POST' and request.headers.get('X-GitHub-Event') == TARGET_EVENT:
        payload = request.json

        # only take action when a new sponsorship is *created*
        if payload['action'] == 'created':
            try:
                sender_gh_user_id = payload['sponsorship']['sponsor']['id']
                print("our new sponsor is: ", sender_gh_user_id)

                add_sponsor(sender_gh_user_id, USERNAME, API_KEY)

                return '200 OK'
            except:
                print("missing sponsor data (unexpected request type?)")
    else:
        print("Ignored event: ", request.headers.get('X-GitHub-Event'))


if __name__ == '__main__':
    # start server
    run(app, host='0.0.0.0', port=4567)

