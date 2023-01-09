from magic_store.store import Store
from magic_store.models.user import User
from magic_store.models.file import File
from magic_store.constants import MESSAGES
from typing import Union


class Database:
    def __init__(self):
        self._store = Store('db.json')
        self._store.load()

    def add_user(self, user: User):
        result = self.get_user(user.username)

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

    def add_file(self, username: str, file: File, tags: list[str]):
        result = self.get_user(username)
        if result['code'] != MESSAGES.OK_CODE:
            return MESSAGES.USER_NOT_FOUND

        for tag in tags:
            tag_key = f'{username}:{tag}'
            tag_value = self._store.get(tag_key, namespace='files')
            if tag_value['code'] == MESSAGES.OK_CODE:
                tag_value['value'].append(file.__dict__)
                result = self._store.put(tag_key, tag_value['value'], namespace='files', guard=tag_value['guard'])
            else:
                result = self._store.put(tag_key, [file.__dict__], namespace='files')
            if result['code'] != MESSAGES.OK_CODE:
                return result

        self._store.save()
        return MESSAGES.FILE_CREATED

    def get_file(self, username: str, filename: str, tag: Union[str, None] = None):
        if tag:
            tag = self.get_tag(username, tag)
            if tag['code'] != MESSAGES.OK_CODE:
                return MESSAGES.TAG_NOT_FOUND

            for f in tag['value']:
                if f['filename'] == filename:
                    return MESSAGES.ok(File(f['filename'], f['path'], f['id']), tag['guard'])
            return MESSAGES.FILE_NOT_FOUND
        else:
            for tag in self.get_all_tags(username)['value']:
                tag_data = self.get_tag(username, tag)
                if tag_data['code'] == MESSAGES.OK_CODE:
                    for f in tag_data['value']:
                        if f['filename'] == filename:
                            return MESSAGES.ok(File(f['filename'], f['path'], f['id']), tag['guard'])
            return MESSAGES.FILE_NOT_FOUND

    def delete_file(self, username: str, filename: str, tag: Union[str, None] = None):
        user = self.get_user(username)
        if user['code'] != MESSAGES.OK_CODE:
            return MESSAGES.USER_NOT_FOUND

        if tag:
            tag_data = self.get_tag(username, tag)
            if tag_data['code'] != MESSAGES.OK_CODE:
                return MESSAGES.TAG_NOT_FOUND

            for f in tag_data['value']:
                to_save = [f.__dict__ for f in tag_data['value'] if f['filename'] != filename]
                result = self._store.put(f'{username}:{tag}', to_save, namespace='files', guard=tag_data['guard'])
                if result['code'] != MESSAGES.OK_CODE:
                    return result
                else:
                    self._store.save()
                    return MESSAGES.FILE_DELETED
            return MESSAGES.FILE_NOT_FOUND
        else:
            for tag in self.get_all_tags(username)['value']:
                tag_data = self.get_tag(username, tag)
                if tag_data['code'] == MESSAGES.OK_CODE:
                    for f in tag_data['value']:
                        to_save = [f.__dict__ for f in tag_data['value'] if f['filename'] != filename]
                        result = self._store.put(
                            f'{username}:{tag}', to_save, namespace='files', guard=tag_data['guard'])
                        if result['code'] != MESSAGES.OK_CODE:
                            return result
                        else:
                            self._store.save()
                            return MESSAGES.FILE_DELETED
            return MESSAGES.FILE_NOT_FOUND

    def get_tag(self, username: str, tag: str):
        tag = self._store.get(f'{username}:{tag}', namespace='files')
        if tag['code'] != MESSAGES.OK_CODE:
            return MESSAGES.TAG_NOT_FOUND

        files = []
        for f in tag['value']:
            files.append(File(f['filename'], f['path'], f['id']))
        return MESSAGES.ok(files, tag['guard'])

    def get_all_tags(self, username: str):
        result = self.get_user(username)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            tags = []
            if not 'files' in self._store._store:
                return MESSAGES.ok(tags)

            for key in self._store._store['files']:
                key_data = key.split(':')
                if key_data[0] == username:
                    tags.append(key_data[1])
            return MESSAGES.ok(tags)
