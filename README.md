# TODO

documentation:
- config.json
- hook config

code:
- swap out target url and event, dender id selection, add team ID

# installation

## dependencies

```console
$ pip3 install -r requirements.txt
```
This also installs [Zappa](https://github.com/Miserlou/Zappa) and all the dependencies needed for a Zappa deploy

# deploying
TODO add docker container

Make sure you're operating in a [virtual environment](https://docs.python.org/3/library/venv.html) **with python 3.7**

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