Wait For Output
===============

Waits for a pattern to match output of a command or docker container logs.

**Features:**
- Waiting for a pattern to appear in docker container logs
- Waiting for a generic command output to appear
- Finding container name by regexp pattern
- Returns result as a exit code and message
- Output of checked command/container log is passed through to the console

Installing
----------

```bash
pip install waitforoutput
```

Usage with docker
-----------------

`--container` takes a regexp expression, or a full container name. Output from container is streamed to the console until timeout is reached, at the end
only result is displayed - the container is not killed.

If multiple containers are found the application will exit with an error.

```bash
$ waitforoutput 'Configuration complete; ready for start up' --container 'nginx_*' --timeout 5
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
[2021-05-14 05:01:46.188][info]: Match found
```

Usage with any shell command
----------------------------

Command specified with `--command` parameter will be launched, and the `waitforoutput` will be streaming output until the `--timeout` is reached.
After timeout the process will be killed.

```bash
$ waitforoutput 'Linux' --command 'uname -a'
Linux riotkit-dev 5.10.23-1-MANJARO #1 SMP PREEMPT Thu Mar 11 18:47:18 UTC 2021 x86_64 GNU/Linux
[2021-05-14 05:01:46.188][info]: Match found
```

Authors
=======

Created by Riotkit anarchist tech-collective.
