<h1 align="center"> Aiorq </h1>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7 | 3.8 | 3.9 | 3.10-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</p>

## Introduction

Aiorq is a distributed task queue with asyncio and redis, which rewrite from arq to make improvement and include web
interface.

See [documentation](https://aiorq.readthedocs.io) for more details.

## Requirements

- redis >= 5.0
- aioredis >= 2.0.0

## Install

```shell
pip install aiorq
```

## Quick Start

### Task Definition

```python
# demo.py
# -*- coding: utf-8 -*-
import asyncio
import os

from aiorq.connections import RedisSettings
from aiorq.cron import cron


async def say_hello(ctx, name) -> None:
    await asyncio.sleep(5)
    print(f"Hello {name}")


async def startup(ctx):
    print("starting... done")


async def shutdown(ctx):
    print("ending... done")


async def run_cron(ctx, name_):
    return f"hello {name_}"


class WorkerSettings:
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "127.0.0.1"),
        port=os.getenv("REDIS_PORT", 6379),
        database=os.getenv("REDIS_DATABASE", 0),
        password=os.getenv("REDIS_PASSWORD", None)
    )

    functions = [say_hello]

    on_startup = startup

    on_shutdown = shutdown

    cron_jobs = [
        cron(coroutine=run_cron, kwargs={"name_": "pai"}, hour={17, 12, 18}, minute=40, second=50,
             keep_result_forever=True)
    ]

```

### Run aiorq worker

```text
> aiorq tasks.WorkerSettings worker
15:08:50: Starting Queue: ohuo
15:08:50: Starting Worker: ohuo@04dce85c-1798-43eb-89d8-7c6d78919feb
15:08:50: Starting Functions: say_hello, EnHeng
15:08:50: redis_version=5.0.10 mem_usage=731.12K clients_connected=2 db_keys=9
starting...
```

## Integration in FastAPI

```text
> aiorq tasks.WorkerSettings server
INFO:     Started server process [4524]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

## Dashboard

See [dashboard](https://github.com/PY-GZKY/aiorq-dashboard) for more details.

## Thanks

- [Arq](https://github.com/samuelcolvin/arq) and [FastAPI](https://github.com/tiangolo/fastapi)

## License

[MIT](./LICENSE)




