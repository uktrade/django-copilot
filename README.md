# DBT Copilot Django

A set of utility functions for running Django & Flask apps in AWS ECS via AWS Copilot.

## Using  dbt-copilot-python

### Installation

```
pip install dbt-copilot-python
```

### Usage

In settings.py:

1. Add the container IP to ALLOWED_HOSTS so that the load balancer/ALB healthcheck will succeed: 
```

from dbt-copilot-python import get_aws_ecs_container_ip

ALLOWED_HOSTS = [...]

container_ip = get_ecs_container_ip()

if container_ip
    ALLOWED_HOSTS.append(container_ip)
```

2. Configure the `DATABASES` setting from an RDS json object stored in SSM parameter store

```
from dbt-copilot-python import aws_database_config

DATABASES = aws_database_config("ENVIRONMENT_KEY")
```

## Contributing to dbt-copilot-python

### Requirements

* Poetry  
  `pip install poetry`

### Install dependencies

`poetry install`

### Run the tests

`poetry run pytest`
