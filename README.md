# sento-api

_This project is part of Sento's backend_.

Async API for exposing results of Sento's analytics

# Table of contents

- [Prerequisites](#prerequisites)
- [Setting up the database](#setting-up-the-database)
- [Setting up the API](#setting-up-the-api)
- [License](#license)

# Prerequisites

In order to set up an instance you need a PostgreSQL database initialised
using the instructions available [here](#setting-up-the-database).

# Setting up the database

The best way to set up the database is with Docker container provided
in this repository. You need to do the follwing:

- **Configure environment variables for the database**: create a `db.env` fil
  from a copy of `db.example.env`, configure the different values
  according to your needs. Keep in mind that most of those values
  will be needed by other Sento's components in order to connect to the
  database.

- **Configure Sento API**: create a `config.ini` file from a copy of `config.example.ini`
  and adjust the configuration according to your needs.
  Keep track of the variables set in your `db.env` file.
  Let the default value of `sento-db` in `[postgres].host`, this is a name that
  can be used by the container to reach to the database in the container network.

- **Create a database and a user for Sento**: run `docker-compose up -d postgres`,
  this will create PostgreSQL + PostGIS container without any kind of structure.
  After that run `docker-compose exec postgres psql -U postgres -f /src/init.sql`,
  this will create a user and a database for Sento, this step uses the
  configuration values written in `db.env` file.

- **Create the tables from the models**: run
  `docker-compose run --rm --use-aliases sento-api pipenv run alembic upgrade head`.
  This will create the necessary tables in the database using Alembic.

After that you will be all set!

# Setting up the API

**WIP: Section under construction**

# License

The source code of this project is licensed under the GNU Affero General
Public License v3.0.
