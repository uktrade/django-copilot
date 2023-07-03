# DBT Copilot Django

A set of utility functions for running Django & Flask apps in AWS ECS via AWS Copilot.

## Using `dbt-copilot-python`

### Installation

```
pip install dbt-copilot-python
```

### Usage

In `settings.py`:

1. Add the ECS container IP to `ALLOWED_HOSTS` so that the Application Load Balancer (ALB) healthcheck will succeed:

    ```
    from dbt_copilot_python.network import setup_allowed_hosts
    
    ALLOWED_HOSTS = [...]
    
    ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)
    ```

2. Configure the `DATABASES` setting from an RDS JSON object stored in SSM Parameter Store:

    ```
    from dbt-copilot-python import aws_database_config
   
    DATABASES = aws_database_config("ENVIRONMENT_KEY")
    ```

## Contributing to `dbt-copilot-python`

### Requirements

- [Poetry](https://python-poetry.org/); `pip install poetry`

### Install dependencies & pre-commit hooks

```
poetry install && poetry run pre-commit install
```

### Run the tests

```
poetry run pytest
```
