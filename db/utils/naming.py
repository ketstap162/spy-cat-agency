import re


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
