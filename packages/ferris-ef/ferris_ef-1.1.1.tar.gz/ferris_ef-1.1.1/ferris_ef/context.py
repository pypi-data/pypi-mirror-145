import json
import os
import sys

from ferris_cli.v2 import ApplicationConfigurator
from ferris_cli.v2.services.config import Consul


class Package:
    def __init__(self, name, id):
        self.name = name
        self.id = id


is_local_env = os.environ.get('EF_ENV') == 'local'


if is_local_env:
    config_file_name = 'ef_env.json'

    if not os.path.isfile(config_file_name):
        with open(config_file_name, 'w') as sf:
            json.dump({
                "params": {
                    "package_name": "local_package",
                    "package_id": "1234456778"
                },
                "config": {},
                "secrets": {}
            }, sf)

    f = open(config_file_name)
    env_file = json.load(f)

    params = env_file.get('params', {})
    package = Package(
        name=params.get("package_name", "local_package"),
        id=params.get("package_id", "01234567")
    )

    secrets = env_file.get('secrets', {})
    config = env_file.get('config', {})
else:
    params = json.loads(sys.argv[1]) or {}
    package = Package(
        name=params.get("package_name"),
        id=params.get("package_id")
    )
    secrets = params.pop("secrets", {})
    config = ApplicationConfigurator.get(package.name) or {}
    _env = os.environ.items()


class PackageState:

    def __init__(self):
        self._package = package
        self._package_state_key = f"{self._package.name}.state"
        self.consul = Consul(
            consul_host=config.get('CONSUL_HOST'),
            constul_port=config.get('CONSUL_PORT')
        )

    def get(self):
        index, data = self.consul.client.kv.get(self._package_state_key, index=None)
        return json.loads(data['Value']) if 'Value' in data else {}

    def put(self, key, value):
        try:
            state = self.get()
        except Exception as e:
            state = {}

        state[key] = value
        self.consul.put_item(self._package_state_key, json.dumps(state))


class PackageStateLocal:

    def __init__(self):
        self._package = package
        self._package_state_key = "ef_package_state.json"

        if not os.path.isfile(self._package_state_key):
            with open(self._package_state_key, 'w') as sf:
                json.dump({}, sf)

    def get(self):
        sf = open(self._package_state_key)
        data = json.load(sf)

        return data

    def put(self, key, value):
        state = self.get()
        state[key] = value

        with open(self._package_state_key, 'w') as sf:
            json.dump(state, sf)


state = PackageState() if not is_local_env else PackageStateLocal()

