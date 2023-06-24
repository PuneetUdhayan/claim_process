import os

from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyQuery


api_key_query = APIKeyQuery(name="access_token", auto_error=False)


def validate_api_key(api_key: str = Security(api_key_query)):
    """Checks if API key is sent in query params and matched the API key provided during set-up

    Args:
        api_key (str, optional): aki_key to validate. Defaults to Security(api_key_query).

    Raises:
        HTTPException: Raises exception if API key is not provided or is incorrect
    """
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate API KEY",
        )
