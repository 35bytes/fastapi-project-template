<div align="center">
  <h1>User registration in microservice with FastAPI</h1>
</div>

# Introduction

This repository contains a base project to develop a microservice with FastAPI. The objective of this repository is to structure a base project in FastAPI. This project establishes the necessary folder structure for the domain and services layers, in addition to the tests, in this way, the development stage is simplified so that it focuses on what is really necessary.

# Table of Contents

- [Install dependencies](#install-dependencies)
- [Set environment variables](#set-environment-variables)
- [Create Models](#create-models)
- [Migrations](#migrations)
  - [Create migrations](#create-migrations)
    - [Automatic](#automatic)
    - [Manual](#manual)
  - [Apply migrations](#apply-migrations)
  - [Downgrade migrations](#downgrade-migrations)
- [API entrypoints](#api-entrypoints)
- [Schemas](#schemas)
- [Run server](#run-server)
  - [Development](#development)
  - [Production](#production)
- [Test](#tests)

# Install dependencies

In this repository there are 2 dependency files: `requirements.txt` and `test.requirements.txt`. These dependencies are separated in this way so that only what is necessary for production is installed, which will be defined in requirements.txt

To install the dependencies you must execute the special pip command.

```bash
pip install -r requirements.txt         # Dependencies for production
pip install -r test.requirements.txt    # Dependencies for development
```

# Set environment variables

The `.env` file is **optional**, in which you can store the environment variables you want to load. This hosts the **secret** to perform password encryption and the variables to connect the service to the **database**.

```bash
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

# Create Models

You can create all your **models** in `src/domain/models.py` with **sqlalchemy**. It is very important that the model classes extend from the Base class.

```py
from sqlalchemy import Column, Integer, String

from src.adapters.orm import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

```

# Migrations

## Create migrations

There are 2 ways to create migrations: **automatic** and **manual**. Files in the `alembic/versions` folder **must be deleted**.

## Automatic

To create the migrations automatically, you must execute the special alembic command and set a name for the migration that is generated.

```bash
alembic revision --autogenerate -m "Added users table"
```

**It is important to completely review the generated migrations and modify/remove unnecessary code blocks.**

## Manual

To create the migrations manually, the special alembic command must be executed and set a name for the migration that is generated.

```bash
alembic revision -m "Added users table"
```

A file will be created in the `alembic/versions` folder with the name `*_create_users.py`. To create the necessary fields you must use **sqlalchemy**.

```py
def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

## Apply migrations

To apply the migrations in the database, the special alembic command must be executed. If you want apply the latest changes you must be executed with the value **head**. However, a certain number of migrations can also be executed by indicating a **numerical value**. There is also a third option where the **revision ID** can be referenced.

```bash
alembic upgrade <head | int | revision_id>
```

The `ids` of the revisions of the **applied migrations** will be saved in the `alembic_version` table in the database.

## Downgrade migrations

If you regret applying a migration you can undo the changes using a special alembic command. In a very similar way when applying an upgrade, the downgrade can take different values to undo the migrations, in this case they are: **base**, a **negative numerical value** or a **revision id**.

```bash
alembic downgrade <base | -int | revision_id>
```

When you apply a downgrade, the revision ids will be removed from the `alembic_version` table.

# API entrypoints

To develop the API entrypoints you have to do it from the file `src/entrypoints/main.py`. The development of these APIs will made it by the FastAPI framework.

To facilitate the work, `models`, `schemas` and `get_db` are imported from this file by default.

```py
from fastapi import FastAPI, HTTPException, Depends
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.domain import schemas, models
from src.adapters.orm import get_db

app = FastAPI()


@app.post("/", status_code=201, response_model=schemas.UserBase)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.password != user.password2:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    try:
        new_user = models.User(email=user.email, hashed_password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"email": new_user.email}

    except (IntegrityError, UniqueViolation):
        raise HTTPException(status_code=400, detail="User already exists")
```

# Schemas

FastAPI can use schemas to define the structure of the request and response. In this project you can create your schemas in the file `src/domain/schemas.py`.

```py
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    password2: str
```

# Run server

The service can be run in 2 ways: **development** and **production**.

## Development

To start a development server to be able to test your project live, you can execute the special uvicorn command.

```bash
uvicorn src.entrypoints.main:app --reload
```

## Production

To put the project into production it is no longer necessary for uvicorn to be reading the changes in the repository. In this case the execution of the server with uvicorn changes.

```bash
uvicorn src.entrypoints.main:app --host 0.0.0.0 --port 80
```

# Tests

In the repository there is a folder structure to differentiate the types of tests: **config**, **unit**, **integration** and **end to end**. The tests are carried out with Pytest and the **configuration** of the tests is carried out in `tests/conftest.py`.

To install the development and test dependencies, you have to install the packages in the file `test.requirements.txt`.

```bash
pip install -r test.requirements.txt
```

One of the default configurations that exists in the file is to create a **FastAPI client that uses an in-memory database**. The benefit of this client is to be able to carry out **end to end** tests without harming any external base, facilitating the development of the tests.

To run the tests, simply use the special **Pytest** command.

```bash
pytest  # Execute all tests in tests folder
```

In the dependencies package there is **pytest-cov**, with this package we can check the coverage of the tests throughout the code.

```bash
pytest --cov=myproj tests/  # This line will display the result report in terminal
```

There is also an option to generate an **html file** to review the coverage of each code block in the project.

```bash
pytest --cov-report html --cov=. tests/
```

This generates the `htmlcov/index.html` file which you can open with your web browser and navigate through the lines of code to see what is covered by the tests and what is not.
