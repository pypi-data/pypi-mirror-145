<p align="center">
  <img src="https://admin.pngme.com/logo.png" alt="Pngme" width="100" height="100">
</p>

<h3 align="center">Python API Client</h3>

This package exposes a synchronous and asynchronous client used to interact with Pngme's financial data APIs.

## Install

Install the latest version with:

```bash
pip3 install pngme-api
```

## Quick start

Create a `Client` instance using your API `token` found in the [Pngme Dashboard](https://admin.pngme.com):

```python
from pngme.api import Client

token = "" # your API token
client = Client(token)
```

> If you're using [`asyncio`](https://docs.python.org/3/library/asyncio.html), you can import and use the `AsyncClient` instead.

We can list or search the available [`/users`](https://developers.api.pngme.com/reference/get_users):

```python
users = client.users.get()
users = client.users.get(search="2343456789012")
```

For a user of interest, we can get a list of the user's [`/institutions`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions):

```python
user_uuid = "33b6215d-3d75-4271-801c-6da27603a8be"

institutions = client.institutions.get(user_uuid=user_uuid)
```

Then for a given institution, we can get a list of the user's [`/transactions`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-transactions), [`/balances`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-balances), or [`/alerts`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-alerts):

```python
user_uuid = "33b6215d-3d75-4271-801c-6da27603a8be"
institution_id = "zenithbank"

transactions = client.transactions.get(user_uuid=user_uuid, institution_id=institution_id)
balances = client.balances.get(user_uuid=user_uuid, institution_id=institution_id)
alerts = client.alerts.get(user_uuid=user_uuid, institution_id=institution_id)
```

## Development environment

We use [Poetry](https://python-poetry.org) to build, package, and publish this project. You'll need to [install Poetry](https://python-poetry.org/docs/#installation) to use the development tools.

Clone this repo and install the development dependencies:

```bash
make install
```

> You may need to configure your IDE to point to the newly created virtual environment after running install.

This will create a virtual environment in the `.venv` directory. You can activate the virtual environment with `source .venv/bin/activate` or `poetry shell`.

You can type `make help` to see a list of other options, which aren't strictly necessary as part of our day-to-day development practices.

### Integration tests

You can replicate the integration tests (which run in a GitHub action on every push) locally. To do this, you'll need to set the `PNGME_TOKEN` environment variable with your API key from the [Pngme Dashboard](https://admin.pngme.com).

This can be done in 2 ways:

1. Create a `.env` file from the template (`.env.local`) and set your `PNGME_TOKEN` there

```bash
cp .env.local .env
# set your PNGME_TOKEN in the .env file
make ci
```

2. Or set the variable in your active shell and run the tests:

```bash
export PNGME_TOKEN=...
make ci
```

### Dependencies

Production dependencies are listed in [setup.cfg](./setup.cfg) under `options.install_requires`, see [`setuptools` dependency management](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#dependency-management).

Development dependencies are listed in [requirements.txt](./requirements.txt).

Running `make install` will install **both** production and development dependencies. Running `pip install .` (where `.` is the path to the directory containing [pyproject.toml](./pyproject.toml)) will install only the production dependencies.
