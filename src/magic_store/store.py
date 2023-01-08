import uuid
import json
import os

from magic_store.constants import MESSAGES


class Store:

    def __init__(self, filename):
        self._store = {"__default__": {}}
        self._filename = filename
        self._currentNamespace = None

    def createNamespace(self, namespace):
        if namespace == "__default__":
            return MESSAGES.INCORRECT_NAMESPACE

        self._store[namespace] = {}
        return MESSAGES.OK

    def put(self, key, value, *, namespace=None, guard=None):
        namespace = self._checkNamespace(namespace)
        if namespace == None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not self._guardKVArgs(key, value):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            self._store[namespace] = {}

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v['guard'] == guard:
                v['guard'] = uuid.uuid4().hex
                v['value'] = value
            else:
                return MESSAGES.INCORRECT_GUARD
        else:
            self._store[namespace][key] = {"guard": uuid.uuid4().hex, "value": value}

        return MESSAGES.OK

    def get(self, key=None, *, namespace=None):
        namespace = self._checkNamespace(namespace)

        if namespace is None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not self._guardKVArgs(key, ''):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            self._store[namespace] = {}

        if not (key in self._store[namespace]):
            return MESSAGES.INCORRECT_KEY

        store_value = self._store[namespace][key]['value']
        if isinstance(store_value, dict) or isinstance(store_value, list):
            value = store_value.copy()
        else:
            value = store_value

        return MESSAGES.ok(value, self._store[namespace][key]['guard'])

    def delete(self, key, *, namespace=None, guard=None):
        namespace = self._checkNamespace(namespace)

        if namespace is None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not self._guardKVArgs(key, ''):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            return MESSAGES.INCORRECT_NAMESPACE

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v['guard'] == guard:
                del self._store[namespace][key]
                return MESSAGES.OK
            else:
                return MESSAGES.INCORRECT_GUARD
        else:
            return MESSAGES.INCORRECT_KEY

    def save(self):
        with open(self._filename, 'w') as file:
            json.dump(self._store, file)
        return MESSAGES.OK

    def load(self):
        if os.path.exists(self._filename):
            with open(self._filename) as file:
                self._store = json.load(file)
        return MESSAGES.OK

    def _checkNamespace(self, namespace):
        if namespace == '__default__':
            return

        if namespace is None:
            if self._currentNamespace is not None:
                return self._currentNamespace
            return "__default__"

        return namespace

    def _guardKVArgs(self, key, _):
        return isinstance(key, str) and len(key) > 0