from sqlalchemy import Column, BigInteger, String, Index, DateTime, Float

from . import Base


class Claim(Base):
    __tablename__ = "claims"

    # pk = Column(BigInteger, primary_key=True, index=True)
    id = Column(String(32), primary_key=True, nullable=False)
    service_date = Column(DateTime, nullable=False)
    submitted_procedure = Column(String, nullable=True)
    plan_group_number = Column(String, nullable=False)
    subscriber_number = Column(BigInteger, nullable=False)
    provider_npi = Column(BigInteger, nullable=False)
    currency = Column(
        String(10), nullable=False
    )  # Provided in case the buisness expands to multiple countries.
    # An assumption has been made that all amounts mentioned in a single claim will be of the same currency
    provider_fees = Column(Float, nullable=False)
    allowed_fees = Column(Float, nullable=False)
    member_coinsurance = Column(Float, nullable=False)
    member_copay = Column(Float, nullable=False)
    net_fees = Column(Float, nullable=False)


class AgregateProviderFees(Base):
    __tablename__ = "aggregate_provider_fees"

    provider_npi = Column(BigInteger, primary_key=True,)
    aggregate_net_fees = Column(Float)


aggregate_net_fees_index = Index(
    "aggregate_net_fees_index", AgregateProviderFees.aggregate_net_fees.desc()
)

provider_npi_index = Index("provider_npi_index", AgregateProviderFees.provider_npi)
