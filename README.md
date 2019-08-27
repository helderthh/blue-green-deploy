# A simple blue green deployment

In this repository you will find a *Python3* script called `bg-deploy.py` to execute a blue green deployment with Kubernetes and a folder containing the source code of a simple [ping pong service](../blob/master/ping-pong) using Flask, which you can use in case you want to test this script or whatever you need.


# bg-deploy

The `bg-deploy.py` script can be executed using:

```
python bg-deploy.py ping-pong ping-pong
```


It will receive 2 commnand line arguments:


Argument|Type|Description
---|---|---
`project_root` | str | path to the project's root folder
`deployment_name` | str | deployment's name used to get its data


## Algorithm

- Check what is the color of the deployment currently available.
- Generate a copy of `{project_root}/production/deployment.yaml` and `{project_root}/production/service.yaml`.
- Replace the color in the `deployment.yaml` copy and apply it.
- Wait till the deployment is ready.
- Replace the color in the `service.yaml` copy and apply it.
- Finally, remove the copies of .yaml files.


## Requirements

Your project should have:
- A `production` folder
- A `production/deployment.yaml` file with the label `deployment: ${DEPLOY_VERSION}`
- A `production/service.yaml` file with the label `deployment: ${DEPLOY_VERSION}`

Please check a simple example in the [ping pong service](../blob/master/ping-pong) example.

