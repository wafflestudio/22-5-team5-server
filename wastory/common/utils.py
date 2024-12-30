from wastory.common.errors import InvalidFieldFormatError


def validate_phone_number(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.startswith("010") or not len(value) == 11 or not value.isdigit():
        raise InvalidFieldFormatError()
    return value