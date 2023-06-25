# Claim process

_Claim process_ is a service for processing insurance claims.

# Requirements

1. docker
2. docker-compose

# Run

In order to run an instance of _claim process_ run the following command from the root
of the repository

```
docker-compose -f docker-compose.yml --env-file sample_envfile.env up -d
```

> IMPORTANT please make sure PAYMENT_GATEWAY_ENDPOINT env variable is set. You can use webhook.site to obtain a URL.

NOTE: replace _sample_envfile.env_ with an file containing the fields with secrets.

You can access the API documentation at endpoint *http://localhost:8000/docs*

# Assumptions made

1. Endpoint that returns the top 10 provider_npis by net fees, provides an aggregate of the net fees for each provider and not top 10 net fees by claim.
2. Rate limit is across multiple instances of the API and not just for a single instance.

# Retrieving top 10 Provider NPIs

## Approach taken

A database table **aggregate_provider_fees** has been created with *provider_npis* and *netfees* as columns.

provider_npis has been indexed to optimize search
netfees has been indexed to optimize order by in desc order

Every time a claim is made *netfees* is incremented with the net fee of that claim

To fetch the top 10 *provider_npis* a query is run to fetch provider_npi order by netfees in descending order.

## Alternative approach

Redis has been set up to facilitate rate limiting across multiple API instances. 
**Redis sorted sets** can be used to store the *provider_npis* along with *netfees*

# Running tests

Before running tests ensure a .env file is created with the following values

```
API_KEY=
PAYMENT_GATEWAY_ENDPOINT=
PAYMENT_GATEWAY_KEY=
POSTGRES_HOST=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
REDIS_HOST=
REDIS_PORT=
```

Make sure you have an instance of redis and postgress running for the integration tests

```

```

Run the following command to run the tests
```
python -m coverage run -m pytest
```
