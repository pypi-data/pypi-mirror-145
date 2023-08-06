"""Module with functions for 'types' subpackage."""


def validate_sequence(value, variable):
    if isinstance(value, str):
        raise TypeError(
            f"Variable '{variable}' must not be string, but Sequence. It can be tuple or list for example. "
            "Beware that if you use tuple with just one member like this ('string'), it's finally parsed as "
            "string. If this is the case, add coma like this ('string',)."
        )
