from magic_store.store import Store
from magic_store.models.user import User
from magic_store.constants import MESSAGES


class Database:
    def __init__(self):
        self._store = Store('db.json')
        self._store.load()

    def add_user(self, user: User):
        result = self._store.get(user.username)

        if result['code'] == MESSAGES.OK_CODE:
            return MESSAGES.USER_ALREADY_EXISTS

        result = self._store.put(user.username, user.__dict__, namespace='users')
        if result['code'] != MESSAGES.OK_CODE:
            return result
        else:
            self._store.save()
            return MESSAGES.USER_CREATED

    def get_user(self, username: str):
        result = self._store.get(username, namespace='users')
        if result['code'] != MESSAGES.OK_CODE:
            return result
        else:
            values = result['value']
            return MESSAGES.ok(
                User(values['name'], values['username'], values['email'], values['id']),
                result['guard']
            )

    def update_user(self, username: str, user: User):
        result = self.get_user(username)
        if result['code'] != MESSAGES.OK_CODE:
            return result

        user_data = result['value']
        user_data.name = user.name
        user_data.email = user.email

        result = self._store.put(username, user_data.__dict__, namespace='users', guard=result['guard'])
        if result['code'] != MESSAGES.OK_CODE:
            return result
        else:
            self._store.save()
            return MESSAGES.USER_UPDATED

    def delete_user(self, username: str):
        user = self.get_user(username)
        if user['code'] == MESSAGES.OK_CODE:
            result = self._store.delete(username, namespace='users', guard=user['guard'])
            if result['code'] != MESSAGES.OK_CODE:
                return result
            else:
                self._store.save()
                return MESSAGES.USER_DELETED
        else:
            return MESSAGES.USER_NOT_FOUND
