from faker import Faker
from sqlalchemy import insert
from models.user import User
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import settings


def populate_user_model(session: Session, num_of_records: int = 1) -> None:
    faker = Faker()
    records_to_insert = []

    for _ in range(num_of_records):
        record = {
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'email': faker.free_email(),
            'signup_datetime': faker.date_between(date.today() - timedelta(days=5*365), date.today()),
            'date_of_birth': faker.date_of_birth(minimum_age=18, maximum_age=79),
            'status_id': 1,
        }
        records_to_insert.append(record)
    session.execute(insert(User), records_to_insert)

def get_db_session(expire_on_commit: bool = True, echo: bool = False) -> Session:
    engine = create_engine(settings.CONN_STRING, echo=echo)
    return Session(engine, expire_on_commit=expire_on_commit)
