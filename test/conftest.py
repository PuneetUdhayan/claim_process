import pytest

from app.database import get_db
from app.database import models


@pytest.fixture(scope="session")
def set_up_env():

    db = get_db().__next__()

    db.query(models.Claim).delete()
    db.query(models.AgregateProviderFees).delete()

    db.commit()
    db.close()