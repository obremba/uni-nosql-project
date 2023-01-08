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

    @classmethod
    def ok(cls, value, guard):
        result = cls.OK.copy()
        result['value'] = value
        result['guard'] = guard
        return result