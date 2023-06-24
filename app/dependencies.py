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
