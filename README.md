# sento-api

_This project is part of Sento's backend_.

Async API for exposing results of Sento's analytics

# Table of contents

- [Prerequisites](#prerequisites)
  - [Using Docker and Docker Compose](#using-docker-and-docker-compose)
  - [Running locally](#running-locally)
- [Setting up the database](#setting-up-the-database)
- [Setting up the API](#setting-up-the-api)
- [License](#license)

# Prerequisites

## Using Docker and Docker Compose

For this type of installation you will need:

- Docker Engine 17.12.0 or higher.
- Docker Compose 1.18.0 or higher.

## Running locally

These are the software requirements of each component if you want to run it
locally:

- Database
  - PostgreSQL 9.6 or higher (older versions have not been tested).
  - PostGIS 2.3.0 or higher.
  - `pg_trgm` extension activated.

- API
  - Python 3.7 or higher.
  - Pipenv (package manager).

In order to set up an instance you need a PostgreSQL database initialised
using the instructions available [here](#setting-up-the-database).

# Setting up the database

The best way to set up the database is with Docker container provided
in this repository, but you can also use an existing DBMS.
You need to do the following:

- **Configure variables for the database**:
  - **Using the Docker Container**:
    1. Create a `db.env` file from a copy of `db.example.env`.
    2. Configure the different values in `db.env` according to your needs.
      Keep in mind that most of those values will be needed by other Sento's components
      in order to connect to the database.
  - **Using an existing PostgreSQL instance**: If you have an existing PostgreSQL database
    that matches the requirements, you can create a database for sento using the SQL script
    located at `sento_api/database/init.sql`. Substitute the different variables at the start
    of that script with the values that best suit you.

- **Configure Sento API database connection**:
  1. Create a `config.ini` file from a copy of `config.example.ini`
  2. Adjust the configuration in `config.ini` according to your needs. Keep track of the variables
    set in your `db.env` file or in your customized `init.sql` script. You should leave the default
    value of `sento-db` in the `host` key inside the `[postgres]` section if you plan to use
    the PostgreSQL container, this is a name that can be used by the container
    to reach to the database in the container network.

- **Create a database and a user for Sento**:
  - **With the Docker Container**:
    1. Run `docker volume create sento-data`, this will create a Docker volume where all database
      data will be stored, useful for making backups and avoiding data loss caused by
      the removal of the database container.
    2. Run `docker-compose up -d sento-db`, this will create a PostgreSQL + PostGIS container
      without any kind of structure.
    3. Run `docker-compose exec sento-db psql -U postgres -f /src/init.sql`, this will
      create a user and a database for Sento, this step uses the configuration values
      written in `db.env` file.
  - **Using an available instance**: run your customized `init.sql` script
    with a tool like `psql` or `pgAdmin`.

- **Create the tables from the models**:
  - **With Docker**:
    1. Build the API container's image with `docker-compose build`.
    2. Run
      `docker-compose run --rm --use-aliases sento-api pipenv run alembic upgrade head`.
      This will create the necessary tables in the database using Alembic.
  - **Locally using pipenv**:
    1. Create a Python virtual environment with the necessary dependencies with `pipenv sync`.
    2. Run `pipenv run alembic upgrade head`.

After that you will be all set!

# Setting up the API

Check the values set in your `config.ini` file (made from a copy of
`config.example.ini`), specifically the values set in the `[api]` section.

- **With Docker**:
  1. Remember that the values set in the `config.ini` file are relative to the container.
    Normally you will not need to change the listening IP and port present
    in the `config.example.ini`, but, if you make any changes you will need to keep them
    in mind for the next step.
  2. Create a `docker-compose.override.yml` file from `docker-compose.override.exammple.yml` file,
    then you can configure the IP and port mapping between your host and the container.
    You can also override other container configurations if you need.
  3. If you built the image for the API container previously, you can run
    `docker-compose up -d sento-api`.
- **Running locally**:
  1. Create a Python virtual environment with the necessary dependencies with `pipenv sync`,
    if you have not created it previously.
  2. Run the following command `pipenv run sento_api/main.py`.

If you have followed the previous steps you should have an
instance of the API waiting for requests.

# License

The source code of this project is licensed under the GNU Affero General
Public License v3.0.
