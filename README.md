<div align="center">
  <h1>User registration in microservice with FastAPI</h1>
</div>

# Introduction

This repository contains a base project to develop a microservice with FastAPI. The objective of this repository is to structure a base project in FastAPI. This project establishes the necessary folder structure for the domain and services layers, in addition to the tests, in this way, the development stage is simplified so that it focuses on what is really necessary.

# Migrations

To apply migrations execute

```
alembic upgrade head
```

To downgrade the migrations execute

```
alembic downgrade <base | -int>
```
