# Python API client for NeuroIO


[![PyPI version](https://badge.fury.io/py/neuroio.svg)](http://badge.fury.io/py/neuroio)
[![codecov](https://codecov.io/gh/neuroio/neuroio-python/branch/master/graph/badge.svg)](https://codecov.io/gh/neuroio/neuroio-python)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/neuroio/)
[![Downloads](https://pepy.tech/badge/neuroio)](https://pepy.tech/project/neuroio)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)

_________________

[Read Latest Documentation](https://neuroio.github.io/neuroio-python/) - [Browse GitHub Code Repository](https://github.com/neuroio/neuroio-python/)
_________________

This library strives to be a complete mirror of official NeuroIO API in terms of methods and interfaces.

Official latest API documentation can be found [here](https://kb.neuroio.com/).

For your convenience, you can make API calls using sync or async (asyncio) interface.

## Installation

```sh
pip install neuroio
```

Note that it is always recommended pinning version of your installed packages.

## Usage example (sync)

An example of how to create a source:

```python
from neuroio import Client


if __name__ == '__main__':
    # api_token is just str with your API token from NeuroIO
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(api_token=api_token)
    # Issue API request to create source
    client.sources.create(name="test_name")

```

Now that we have our source created, we can create person inside that source:

```python
from neuroio import Client


def create_persons_example(client: Client):
    source_name = "test_name"
    with open("image.png", "rb") as f:
        response = client.persons.create(
            image=f,
            source=source_name,
            facesize=1000,
            create_on_ha=True,
            create_on_junk=True,
            identify_asm=True
        )
    print("Persons Create Response:\n", response.json(), flush=True)


if __name__ == '__main__':
    # api_token is just str with your API token from NeuroIO
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(api_token=api_token)
    # Issue API request to create a person
    create_persons_example(client)

```

Now that we have our source & person created, we can search for persons:

```python
from neuroio import Client


def search_persons_example(client: Client):
    with open("image.png", "rb") as f:
        response = client.persons.search(
            image=f,
            identify_asm=True
        )
    print("Persons Search Response:\n", response.json(), flush=True)


if __name__ == '__main__':
    # api_token is just str with your API token from NeuroIO
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(api_token=api_token)
    # Issue API request to search persons
    search_persons_example(client)

```

An example of how to listen for events:

```python
import asyncio
import json
import logging
import signal

from neuroio import EventListener


async def event_handler_func(event_message: str):
    # NOTE: this must be awaitable and accept single param Union[str, bytes]
    json_message = json.loads(event_message)
    is_ping_response = "PING" in json_message.keys()
    is_auth_response = "auth" in json_message.keys()
    is_error_response = "error" in json_message.keys()
    if is_ping_response:
        if json_message["PING"] != "PONG":
            # something is wrong with socket connection
            raise RuntimeError()
        else:
            # this is correct pong response on our periodic pings
            logging.info("Connection is alive")
    elif is_auth_response:
        logging.info("Authorized successfully")
    elif is_error_response:
        # something is wrong with provided token
        logging.info(json_message["error"], flush=True)
    else:
        # this must be event about entry itself
        # now you can inspect json_message for information about that
        logging.info(json_message["data"]["face_image"])


async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    logging.info(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    
    # NOTE: You are advised to hook-up uvloop here for improved performance
    
    api_token = "1234567890"
    events_listener = EventListener(
        api_token=api_token, event_handler_func=event_handler_func
    )

    loop = asyncio.get_event_loop()
    # May want to catch other signals too
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda _s=s: asyncio.create_task(shutdown(_s, loop))
        )

    try:
        loop.create_task(events_listener.listen())
        loop.run_forever()
    finally:
        loop.close()
        logging.info("Successfully shutdown")


```

_For more examples and usage, please refer to the [docs](https://neuroio.github.io/neuroio-python/)._

## Development setup

To install all the development requirements:

```sh
pip install --upgrade pip
pip install poetry
poetry install --no-root
```

To run linters & test suite:

```sh
./scripts/test.sh
```

## Release History
* 0.1.0
    * Support for WebSocket Events
    * Drop Python 3.6 support
* 0.0.9
    * Fixes to the sources API in terms of required fields
* 0.0.8
    * Updated library to latest API version (at the time of this release - 1.3.1)
    * Updated README & docs
* 0.0.7
    * Updated library to latest API version (at the time of this release - 1.3.0)
    * Updated requirements
    * Updated README & docs
* 0.0.6
    * Updated library to latest API version (at the time of this release - 1.2.1)
    * Updated README & docs
* 0.0.5
    * Fixed persistent connection problems
    * Updated requirements
    * Codebase cleanup
* 0.0.4
    * Changed the way how we treat httpx connection - now we don't close it after every request (which was supposedly right way in httpx docs)
* 0.0.3
    * Updated httpx version, disabled cruft check since it just messes up project files

## License

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
