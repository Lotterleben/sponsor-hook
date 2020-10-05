#!/usr/bin/env python3

from bottle import route, run, template, request

# NOTE:
# - Webhook contenttype must be set to `application/json`

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

            # TODO pull info from payload['sponsorship']['sponsor']['html_url'] instead
            sender = payload['sender']['html_url'] # todo pick whatever info we need to subscribe that person
            print("our new sponsor is: ", sender)

            # TODO take action

            return 'OK'

run(host='localhost', port=4567)