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


-- Connect to the created database as the user
\c sento :sento_user

BEGIN;
    CREATE SCHEMA IF NOT EXISTS data;

    CREATE TABLE IF NOT EXISTS data.topics (
        id bigserial PRIMARY KEY,
        name text NOT NULL,
        url text NOT NULL,
        query_str text NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_data_topics_name ON data.topics (name);

    CREATE TABLE IF NOT EXISTS data.statuses (
        id bigint PRIMARY KEY,
        wrote_at timestamp without time zone NOT NULL,
        fetched_at timestamp without time zone NOT NULL,
        content text NOT NULL,
        topic_id bigint REFERENCES data.topics (id)
    );

    CREATE TABLE IF NOT EXISTS data.rankings (
        ranking_ts timestamp without time zone NOT NULL,
        ranking_no smallint NOT NULL,
        woeid integer NOT NULL,
        tweet_volume integer,
        topic_id bigint REFERENCES data.topics (id)
    );

    CREATE INDEX IF NOT EXISTS idx_data_rankings_rankings_ts
        ON data.rankings (ranking_ts);
COMMIT;
