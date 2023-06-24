import uuid

from sqlalchemy import Column, Integer, BigInteger, String, Index, UUI, DateTime, Float

from . import Base


class Claim(Base):
    __tablename__ = "claims"

    pk = Column(BigInteger, primary_key=True, index=True)
    id = Column(Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4))
    service_date = Column(DateTime, nullable=False)
    submitted_procedure = Column(String, nullable=False)
    plan_group_number = Column(String)
    subscriber_number = Column(BigInteger)
    provider_npi = Column(BigInteger)
    currency = Column(
        String(10)
    )  # Provided in case the buisness expands to multiple countries.
    # An assumption has been made that all amounts mentioned in a single claim will be of the same currency
    provider_fee = Column(Float)
    allowed_fee = Column(Float)
    member_coinsurance = Column(Float)
    member_copay = Column(Float)
    net_fees = Column(Float)


class AgregateProviderFees(Base):
    __tablename__ = "aggregate_provider_fees"

    pk = Column(BigInteger, primary_key=True, index=True)
    provider_npi = Column(BigInteger)
    aggregate_net_fees = Column(BigInteger)


aggregate_net_fees_index = Index(
    "aggregate_net_fees_index", AgregateProviderFees.aggregate_net_fees.desc
)

provider_npi_index = Index("provider_npi_index", AgregateProviderFees.provider_npi)
