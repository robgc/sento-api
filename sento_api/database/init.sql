/*
 * Copyright (C) 2019 Roberto García Calero (garcalrob@gmail.com)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/


-- Read config from environment
\set sento_user `echo ${SENTO_DB_USER:-sento}`
\set sento_password `echo ${SENTO_DB_PASSWD:-sento}`
\set sento_db_name `echo ${SENTO_DB_NAME:-sento}`

-- Create user and database
CREATE USER :sento_user WITH PASSWORD :'sento_password';
CREATE DATABASE :sento_db_name WITH OWNER :sento_user;

-- Connect to recently created database
\c :sento_db_name

-- Activate PostGIS extension
CREATE EXTENSION postgis;

-- Activate trigram module for text search
CREATE EXTENSION pg_trgm;

-- Connect as sento's db owner
\c :sento_db_name :sento_user

-- Create necessary schemas
BEGIN;
    CREATE SCHEMA IF NOT EXISTS data;
COMMIT;
