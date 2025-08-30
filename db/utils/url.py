import re
from datetime import datetime

from api.core.settings import settings, Settings, TimeZone


class PsqlUrl:
    name: str | None = None
    sync_uri: str | None = None
    async_uri: str | None = None

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        name: str,
        port: int = 5432,
    ):
        self.name = name
        self.sync_uri = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"  # noqa: E231
        self.async_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"  # noqa: E231

    @classmethod
    def create_using_settings(cls, settings: Settings):
        return PsqlUrl(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            name=settings.POSTGRES_DB,
            port=settings.POSTGRES_PORT
        )


postgres_url = PsqlUrl.create_using_settings(settings=settings)


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
