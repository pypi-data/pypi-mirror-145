from django.db.models.fields import BigIntegerField
from django.utils.translation import gettext_lazy as _

from . import EightID


class EightIDField(BigIntegerField):
    default_error_messages = {
        "invalid": _("'%(value)s' is not a valid EightID."),
    }
    description = "EightID: a (really) short id, it fits in 8 bytes"

    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("unique", True)
        kwargs["default"] = EightID
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return value

        return int(value)

    def to_python(self, value):
        if isinstance(value, EightID):
            return value

        elif isinstance(value, int):
            return EightID.from_int(value)

        elif isinstance(value, str):
            return EightID.from_string(value)

        return value

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value
        return EightID.from_int(value)
