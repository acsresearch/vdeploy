# VastAI deployer

On your local machine:

```commandline
$ vastai set api-key <YOUR_VAST_AI_API_KEY> 
```

Next, pick your instance from VastAI market and start instance. You get instance ID after the start.
Next run the following command:

```commandline
$ poetry run -m vdeploy deploy <INSTANCE_ID> --timeout <TIMEOUT_IN_MINUTES>  
```

It installs `vdeploy` on the instance and starts a watch dog process. In case of inactivity
the instance is automatically destroyed after the timeout.

To prevent destruction of the instance, run your long-running computation on instance in the following with block:

```python
from vdeploy.watchdog import keep_alive

with keep_alive():
    ...
    # Long-running computation
    ...
```