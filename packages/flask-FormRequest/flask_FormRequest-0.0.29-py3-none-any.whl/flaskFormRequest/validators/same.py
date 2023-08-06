from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Same(Validator):
    def __init__(self, field: str, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or f"This field is not equal to {field}"
        self.another_field = field

    def handler(self, value, field, request):
        field_to_match = self.data.get(self.another_field)
        if value != field_to_match:
            raise ValidationError(self.message)
