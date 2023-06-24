import os

from sqlalchemy.orm import Session


def db_session_handler(function: str, arguments: dict, db: Session):
    try:
        db.begin()
        data = function(**arguments)
        db.commit()
        return data
    except Exception as e:
        db.rollback()
        raise e


async def get_identifier(request) -> str:
    """Rate limiter identifier has been overridden to use api key insead
    of ip. Doing this ensures rate limit will be applied when multiple
    API instances are running.

    Args:
        request (Request): provides request as input. This will be useful
        if multiple users use the system.

    Returns:
        str: API key
    """
    return os.environ["API_KEY"]
