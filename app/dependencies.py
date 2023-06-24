import os

from sqlalchemy.orm import Session


def db_session_handler(function: str, arguments: dict, db: Session):
    """Used to rollback d operations if an exception occurs

    Args:
        function (str): function to be called
        arguments (dict): arguments to the function
        db (Session): database session

    Raises:
        e: raises exception caught

    Returns:
        Any: returns data returned by function
    """
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
