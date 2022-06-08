<div align="center">
  <h1>User registration in microservice with FastAPI</h1>
</div>

# Introduction

This repository contains a base project to develop a microservice with FastAPI. The objective of this repository is to structure a base project in FastAPI. This project establishes the necessary folder structure for the domain and services layers, in addition to the tests, in this way, the development stage is simplified so that it focuses on what is really necessary.

# Table of Contents

- [Set environment variables](#set-environment-variables)
- [Migrations](#migrations)

# Set environment variables

The `.env` file is **optional**, in which you can store the environment variables you want to load. This hosts the **secret** to perform password encryption and the variables to connect the service to the **database**.

```
SECRET="my-secret-key"
DB_DIALECT="postgresql"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="users"
DB_USER="test"
DB_PASSWORD="test"
```

To use these variables correctly, they must be initialized in the `config.py` file, in this way we control the default values they could have if they are not present in the system.

```py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret: str = os.getenv("SECRET")
    db_dialect: str = os.getenv("DB_DIALECT")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")

    class Config:
        env_file = ".env"
```

To obtain the values of the environment variables, it is recommended to use the `get_settings` function, which returns an object of the `Settings` class that has all the values.

```py
from config import get_settings

settings = get_settings()

assert settings.secret == "my-secret-key"
```

It is recommended to create functions that use the environment variables in the `config.py` file, as in the following example.

```py
from functools import lru_cache

@lru_cache()    # Save in cache the result because the DB URL never change
def get_db_url() -> str:
    settings = get_settings()
    return f"{settings.db_dialect}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

```

# Migrations

To apply migrations execute

```
alembic upgrade head
```

To downgrade the migrations execute

```
alembic downgrade <base | -int>
```
