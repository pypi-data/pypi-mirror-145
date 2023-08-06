import yaml

from eclinical.execption import required, optional


def value(func):
    def __inner__(self, *args, **kwargs):
        return self.env.get(func.__name__), func.__name__

    return __inner__


class Environment:

    def __init__(self, envir, file_path):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.env = yaml.load(f.read(), Loader=yaml.FullLoader).get("ENV").get(envir)

    @property
    @required
    @value
    def public_key(self) -> str: ...

    @property
    @optional
    @value
    def uri(self) -> str: ...

    @property
    @optional
    @value
    def user(self) -> str: ...

    @property
    @optional
    @value
    def password(self) -> str: ...

    @property
    @optional
    @value
    def company(self) -> str: ...

    @property
    @optional
    @value
    def sponsor(self) -> str: ...

    @property
    @optional
    @value
    def study(self) -> str: ...

    @property
    @optional
    @value
    def life_cycle(self) -> str: ...

    @property
    @optional
    @value
    def db(self) -> dict: ...