from fastapi import Depends

from db.session import get_session, Session


class Deps:
    @staticmethod
    def get_session() -> Session:
        return Depends(get_session)
