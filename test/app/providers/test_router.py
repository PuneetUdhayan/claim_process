import os

import pytest
import redis
from fastapi.testclient import TestClient
from fastapi_limiter import FastAPILimiter

from app.main import app
from app.dependencies import get_identifier


@pytest.mark.last
def test_claim_process_without_quadrant(set_up_env):
    with TestClient(app) as client:
        for i in range(10):
            response = client.get(
                "/providers/top-ten", params={"access_token": os.environ["API_KEY"]}
            )
            assert response.status_code == 200
            assert response.json()["data"] == [
                {"aggregate_net_fees": 90, "provider_npi": 1497775531},
                {"aggregate_net_fees": 0, "provider_npi": 1497775530},
            ]
        response = client.get(
            "/providers/top-ten", params={"access_token": os.environ["API_KEY"]}
        )
        response.status_code == 429 
