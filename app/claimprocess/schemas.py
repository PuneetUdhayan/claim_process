import re
from datetime import datetime
from typing import Optional
from price_parser import Price

from pydantic import BaseModel, constr, conint, validator


def process_field(field_name: str) -> str:
    field_name = field_name.strip()
    field_name = field_name.lower()
    field_name = field_name.replace(" ", "_").replace("/", "_")
    field_name = field_name.replace("#", "_number")
    return re.sub("_+", "_", field_name)


def get_currency_and_amount(amount: str, currency: str) -> float:
    price = Price.fromstring(amount)
    if price.currency != currency:
        raise ValueError("Currencies don't match")
    return price.amount_float


class ClaimPayload(BaseModel):
    service_date: datetime
    submitted_procedure: constr(regex=r"^D.*$")
    quadrant: Optional[str]
    plan_group_number: str
    subscriber_number: int
    provider_npi: conint(strict=True)
    currency: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float

    def __init__(self, **data):
        processed_data = {process_field(key): value for key, value in data.items()}
        try:
            processed_data["currency"] = Price.fromstring(
                processed_data["provider_fees"]
            ).currency
        except Exception as e:
            raise ValueError("Invalid curreny in amount fields.")
        super().__init__(**processed_data)

    @validator("service_date", pre=True)
    def validate_service_date(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%m/%d/%Y %H:%M")
            return parsed_date
        except Exception as e:
            raise ValueError("Invalid date format. Expected format: MM/DD/YYYY HH:MM")

    @validator("provider_npi", pre=True)
    def validate_number_length(cls, value):
        if len(str(value)) != 10:
            raise ValueError("Provider NPI must be exactly 10 digits long")
        return value

    @validator("provider_fees", pre=True)
    def validate_provider_fees(cls, value, values):
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("allowed_fees", pre=True)
    def validate_allowed_fees(cls, value, values):
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("member_coinsurance", pre=True)
    def validate_member_coinsurance(cls, value, values):
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("member_copay", pre=True)
    def validate_member_copay(cls, value, values):
        return get_currency_and_amount(amount=value, currency=values["currency"])
