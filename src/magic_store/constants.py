class MESSAGES:
    OK_CODE = 100
    INCORRECT_NAMESPACE_CODE = 202
    INCORRECT_TYPE_CODE = 207
    INCORRECT_GUARD_CODE = 205
    INCORRECT_KEY_CODE = 203

    OK = {"code": OK_CODE, "description": "OK"}
    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE, "description": "Incorrect (nonexisting) namespace"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE, "description": "Incorrect type"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE, "description": "Incorrect guard"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE, "description": "Incorrect key"}

    USER_ALREADY_EXISTS_CODE = 201
    USER_CREATED_CODE = 200
    USER_NOT_FOUND_CODE = 204
    USER_UPDATED_CODE = 200
    USER_DELETED_CODE = 200

    USER_ALREADY_EXISTS = {"code": USER_ALREADY_EXISTS_CODE, "description": "User already exists"}
    USER_CREATED = {"code": USER_CREATED_CODE, "description": "User created"}
    USER_NOT_FOUND = {"code": USER_NOT_FOUND_CODE, "description": "User not found"}
    USER_UPDATED = {"code": USER_UPDATED_CODE, "description": "User updated"}
    USER_DELETED = {"code": USER_DELETED_CODE, "description": "User deleted"}

    AT_LEAST_ONE_TAG_REQUIRED_CODE = 206
    TAG_DELETED_CODE = 200
    TAG_NOT_FOUND_CODE = 204

    AT_LEAST_ONE_TAG_REQUIRED = {"code": AT_LEAST_ONE_TAG_REQUIRED_CODE, "description": "At least one tag required"}
    TAG_DELETED = {"code": TAG_DELETED_CODE, "description": "Tag deleted"}
    TAG_NOT_FOUND = {"code": TAG_NOT_FOUND_CODE, "description": "Tag not found"}

    FILE_CREATED_CODE = 200
    FILE_DELETED_CODE = 200
    FILE_NOT_FOUND_CODE = 204

    FILE_CREATED = {"code": FILE_CREATED_CODE, "description": "File created"}
    FILE_DELETED = {"code": FILE_DELETED_CODE, "description": "File deleted"}
    FILE_NOT_FOUND = {"code": FILE_NOT_FOUND_CODE, "description": "File not found"}

    @classmethod
    def ok(cls, value, guard=None):
        result = cls.OK.copy()
        result['value'] = value
        result['guard'] = guard
        return result
