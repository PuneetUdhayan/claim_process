import re
from datetime import datetime
from typing import Optional
from price_parser import Price

from pydantic import BaseModel, constr, conint, validator


def process_field(field_name: str) -> str:
    """Clean up input field. Makes all characters lower space
    handles spaces and other special characters.

    Args:
        field_name (str): field name

    Returns:
        str: processed_field_name
    """
    field_name = field_name.strip()
    field_name = field_name.lower()
    field_name = field_name.replace(" ", "_").replace("/", "_")
    field_name = field_name.replace("#", "_number")
    return re.sub("_+", "_", field_name)


def get_currency_and_amount(amount: str, currency: str) -> float:
    """Converts string with currency float
    and validates if currency matches provided currency

    Args:
        amount (str): String containing amount
        currency (str): currency to compare and validate against

    Raises:
        ValueError: Throws value error is currency in amount does not
        match currency

    Returns:
        float: Amount in float
    """
    price = Price.fromstring(amount)
    if price.currency != currency:
        raise ValueError("Currencies don't match")
    return price.amount_float


class ClaimPayload(BaseModel):
    """Request body for a claim

    Raises:
        ValueError: service date is not in format MM/DD/YY HH:MM
        ValueError: Provider NPI is not 10 digits long
        ValueError: Any currencies are matching types

    """

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
            raise ValueError("Invalid currency in amount fields.")
        super().__init__(**processed_data)

    @validator("service_date", pre=True)
    def validate_service_date(cls, value):
        """Converts service date from string to datetype

        Args:
            value (str): service date

        Raises:
            ValueError: service date cannot be parsed to datetime

        Returns:
            datetime: service date as a datetime object
        """
        try:
            parsed_date = datetime.strptime(value, "%m/%d/%y %H:%M")
            return parsed_date
        except Exception as e:
            raise ValueError("Invalid date format. Expected format: MM/DD/YY HH:MM")

    @validator("provider_npi", pre=True)
    def validate_number_length(cls, value):
        """Validates if provider NPI is a 10 digit number

        Args:
            value (int): provider npi

        Raises:
            ValueError: If provider NPI id not 10 digits long

        Returns:
            int: provider npi
        """
        if len(str(value)) != 10:
            raise ValueError("Provider NPI must be exactly 10 digits long")
        return value

    @validator("provider_fees", pre=True)
    def validate_provider_fees(cls, value, values):
        """Converts string amount to float amount and stores currency

        Args:
            value (str): amount
            values (dict): all values in payload

        Returns:
            float: amount
        """
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("allowed_fees", pre=True)
    def validate_allowed_fees(cls, value, values):
        """Converts string amount to float amount and stores currency

        Args:
            value (str): amount
            values (dict): all values in payload

        Returns:
            float: amount
        """
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("member_coinsurance", pre=True)
    def validate_member_coinsurance(cls, value, values):
        """Converts string amount to float amount and stores currency

        Args:
            value (str): amount
            values (dict): all values in payload

        Returns:
            float: amount
        """
        return get_currency_and_amount(amount=value, currency=values["currency"])

    @validator("member_copay", pre=True)
    def validate_member_copay(cls, value, values):
        """Converts string amount to float amount and stores currency

        Args:
            value (str): amount
            values (dict): all values in payload

        Returns:
            float: amount
        """
        return get_currency_and_amount(amount=value, currency=values["currency"])


class ClaimDetails(BaseModel):
    """Stores all claim details provided by user as well as claim_id and net_fees"""

    claim_id: str
    service_date: datetime
    submitted_procedure: str
    quadrant: Optional[str]
    plan_group_number: str
    subscriber_number: int
    provider_npi: conint(strict=True)
    currency: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float
    net_fees: float
