from enum import Enum


class StrEnum(str, Enum):
    """
    StrEnum subclasses that create variants using `auto()` will have values equal to their names

    usage:
    class A(StrEnum):
        a = auto()
        b = auto()

    will be equivalent to:
        class A(StrEnum):
        a = 'a'
        b = 'b'
    """

    def _generate_next_value_(name, start, count, last_values) -> str:  # noqa
        """ ses the name as the automatic value"""
        return name
