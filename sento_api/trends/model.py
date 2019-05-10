# Copyright (C) 2019 Roberto García Calero (garcalrob@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sento_api.utils import execute_fetch_query


async def get_top_trends():
    return await execute_fetch_query(
        """
        SELECT DISTINCT
          topic_id,
          ranking_no
        FROM
          data.rankings rankings
        WHERE
          ranking_no BETWEEN 1 AND 10
          AND ranking_ts >= (
            (SELECT MAX(ranking_ts) FROM data.rankings)
            - interval '12 hours'
          )
        ORDER BY
          ranking_no DESC
        LIMIT 15
        """
    )


async def get_current_trends_for_location(woeid):
    return await execute_fetch_query(
        """
        SELECT
          to_char(
            ranking_ts at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"'
          ) as ranking_ts,
          ranking_no,
          tweet_volume,
          topic_id
        FROM (
          SELECT *
          FROM
            data.rankings
          WHERE
            woeid = $1
            AND ranking_ts >= (
              (SELECT MAX(ranking_ts) FROM data.rankings)
              - interval '12 hours'
            )
          ORDER BY
            ranking_ts desc
          LIMIT 50
        ) trends
        ORDER BY
          ranking_no asc
        """,
        woeid
    )


async def get_trends_evolution_in_location(woeid):
    return await execute_fetch_query(
        """
        SELECT
          to_char(ranking_ts, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') as "timestamp",
          json_agg(
            json_build_object(
              'trend', topic_id,
              'number', ranking_no
            )
            ORDER BY ranking_no ASC
          ) AS "trendsPositions"
        FROM
          data.rankings
        WHERE
          woeid = $1
          AND ranking_ts >= (
            (SELECT MAX(ranking_ts) FROM data.rankings)
            - interval '12 hours'
          )
        GROUP BY
          ranking_ts
        """,
        woeid
    )


async def get_trend_evolution_in_location(trend_id, woeid):
    return await execute_fetch_query(
        """
        SELECT
          json_agg(
            json_build_object(
              'timestamp', to_char(ranking_ts, 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
              'number', ranking_no
            )
            ORDER BY ranking_ts ASC
          )
        FROM
          data.rankings
        WHERE
          topic_id = $1
          AND woeid = $2
        GROUP BY
          topic_id,
          woeid
        """,
        trend_id,
        woeid,
        fetch_row=True
    )


async def search_trends_by_name(trend_name):
    return await execute_fetch_query(
        """
        SELECT
          id AS trend,
          id <-> $1 AS distance
        FROM
          data.topics
        ORDER BY
          distance ASC
        LIMIT 20
        """,
        trend_name
    )
