# A simple blue green deployment

In this repository you will find a *Python3* script called `bg-deploy.py` to execute a blue green deployment with Kubernetes. In addition, you will find a folder containing the source code of a simple [ping pong service](../master/ping-pong) using Flask, which you can use in case you want to test this script or whatever you need.


# bg-deploy.py

This script will start a new deployment called _DEPLOYMENT_NAME-COLOR_, where COLOR will be set as the opposite of the current deployment color (this is automatically readed) and DEPLOYMENT_NAME is given as a command line argument (*deployment_name*).

For reading the current  deployment color, the process will need a label (*deployment_app_label*, passed in the command line arguments) to request the deployment resource data, it should be set in the deployment.yaml at `spec -> template -> metadata -> labels -> app` with something similar to :

```
...
labels:
    app: PingPong  # <--
    deployment: ping-pong-${DEPLOY_VERSION}
...
```

The only extra data this script needs to do its job, is the project root folder, you can pass it in the command line arguments too (*project_root*).

Finally, the script will wait until the deployment is ready to update the service applying `service.yaml` and make it manage the new deployment. Then, it will remove the old deployment.

## Command line arguments

It will receive 2 commnand line arguments:


Argument|Type|Description
---|---|---
`project_root` | str | path to the project's root folder
`deployment_name` | str | deployment's base name used to check when it's ready
`deployment_app_label` | str | deployment's app label used to check the current version found in _deployment.yaml_ (spec -> template -> metadata -> labels -> app)
`h, help` | optional | will show a command line arguments help message

Example to execute hte ping-pong service:

```
python bg-deploy.py ping-pong ping-pong PingPong
```

## Algorithm

- Check what is the color of the deployment currently available.
- Generate a copy of `{project_root}/production/deployment.yaml` and `{project_root}/production/service.yaml`.
- Replace the color in the `deployment.yaml` copy and apply it.
- Wait till the deployment is ready.
- Replace the color in the `service.yaml` copy and apply it.
- Finally, remove the copies of .yaml files.


## Requirements

Your project should have:
- A `production` folder.
- A `production/deployment.yaml` file with the tag `${DEPLOY_VERSION}`, which the script will replace temporally. Example:
    ```
    ...
    metadata:
        name: DEPLOYMENT_NAME-${DEPLOY_VERSION}
    ...
    spec:
        template:
            labels:
                app: APP_NAME
                deployment: ${DEPLOY_VERSION}
    ...
    ```
    where APP_NAME is just the name of your app and DEPLOYMENT_NAME the name of your deployment.

- A `production/service.yaml` file with the tag `${DEPLOY_VERSION}`, which the script will replace temporally. Example:

    ```
    ...
    spec:
        selector:
            app: APP_NAME
            deployment: ${DEPLOY_VERSION}
    ...
    ```

Check a simple use in the [ping pong service](../master/ping-pong) example, specially, take a look into the .yaml files.

