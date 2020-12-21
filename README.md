# TODO

documentation:
- set env vars (USERNAME, API_KEY, SECRET_TOKEN)
- hook config

code:
- swap out target url and event, dender id selection, add team ID

# installation

## aws setup

### 1. create profile
⚠️ make sure you set the *profile name* to `ferrous`

```console
➜  sponsor-hook git:(feature/dockerfile) ✗ aws configure sso
SSO start URL [None]: http://ferrous-systems.awsapps.com/start/
SSO Region [None]: eu-central-1
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://device.sso.eu-central-1.amazonaws.com/

Then enter the code:

XXXX-XXXX
The only AWS account available to you is: XXXXXXXXXXXXX
Using the account ID XXXXXXXXXXXXX
The only role available to you is: PowerUserAccess
Using the role name "PowerUserAccess"
CLI default client Region [None]: eu-central-1
CLI default output format [None]:
CLI profile name [PowerUserAccess-914124514389]: ferrous

To use this profile, specify the profile name using --profile, as shown:
```

## using docker

### building (and updating) the docker image

Build the docker image by running `docker build -t knurling-zappa .` in the projects root directory. This only required once or when the zappa version is updated. The resulting container will have awscli, zappa and a basic set of dependencies pre-installed.

### running the docker container

!NOTE! Windows users will need to provide absolute path values in the folling command, because docker. If you're running the command from WSL2, it will work without modification.

Run `docker run -v ```pwd```/:/home/code -v ~/.aws:/root/.aws -eUSERNAME=changeme -eAPI_KEY=changeme -eSECRET_TOKEN=changeme -p127.0.0.1:4567:4567/tcp -it knurling-zappa /bin/bash`. Replace github username, API key and secret_token with suitable values.

This will mount the current directory in the path `/home/code` as well as the AWS config directory required by zappa and give you a shell inside the container. It will expose port `4567` used by the application server to the docker host.

You can start the SSO login process outside the container and run `zappa deploy|update|....` inside the container.

## using virtualenv

Make sure you're operating in a [virtual environment](https://docs.python.org/3/library/venv.html) **with python 3.7**:

```console
$ python3.7 -m venv env
$ source env/bin/activate
```

## dependencies

Install dependencies:
```console
$ cd sponsor-hook
$ pip3 install -r requirements.txt
```
This also installs [Zappa](https://github.com/Miserlou/Zappa) and all the dependencies needed for a Zappa deploy

# deploying

```console
$ cd sponsor-hook
$ zappa update dev
Calling update for stage dev..
Downloading and installing dependencies..
Packaging project as zip.
Uploading sponsor-hook-dev-1607075088.zip (5.9MiB)..
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6.20M/6.20M [00:03<00:00, 1.76MB/s]
Updating Lambda function code..
Updating Lambda function configuration..
Uploading sponsor-hook-dev-template-1607075097.json (1.6KiB)..
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.64k/1.64k [00:00<00:00, 15.5kB/s]
Deploying API Gateway..
Scheduling..
Unscheduled sponsor-hook-dev-zappa-keep-warm-handler.keep_warm_callback.
Scheduled sponsor-hook-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
Your updated Zappa deployment is live!: https://8s1p6pf5e2.execute-api.eu-central-1.amazonaws.com/dev
```

# Webhook setup

- Webhook contenttype must be set to `application/json`
- `config.json` must contain github credentials (see `config.json.sample`)
- generate and set `secret_token` in config as described in
  https://docs.github.com/en/free-pro-team@latest/developers/webhooks-and-events/securing-your-webhooks
