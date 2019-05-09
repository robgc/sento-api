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
          data.rankings
        WHERE
          ranking_no BETWEEN 1 AND 10
          AND ranking_ts BETWEEN (now() - interval '12 hours') AND now()
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
          ORDER BY
            ranking_ts desc
          LIMIT 50
        ) trends
        ORDER BY
          ranking_no asc
        """,
        woeid
    )


async def get_trends_evolution_for_location(woeid):
    return await execute_fetch_query(
        """
        WITH ranking_ts_diffs AS (
          SELECT
            ranking_ts,
            ranking_ts - lag(ranking_ts, 1) OVER (ORDER BY ranking_ts ASC)
              AS ts_diff
          FROM
            data.rankings
          WHERE
            woeid = $1
            AND ranking_ts BETWEEN (now() - interval '12 hours') AND now()
          ORDER BY
            ranking_ts ASC
        ), key_ranking_ts AS (
          SELECT
            ranking_ts,
            lead(ranking_ts, 1) OVER (ORDER BY ranking_ts ASC)
              AS ranking_ts_next
          FROM
            ranking_ts_diffs
          WHERE
            ts_diff IS NULL
            OR extract('minute' FROM ts_diff)::int >= 10
        )

        SELECT
          to_char(
            key_timestamps.ranking_ts at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS"Z"'
          ) as ranking_ts,
          json_agg(
            json_build_object(
              'trend', ranking.topic_id,
              'number', ranking.ranking_no
            )
            ORDER BY ranking.ranking_no ASC
          ) AS "ts_ranking"
        FROM
          key_ranking_ts key_timestamps
          JOIN data.rankings ranking ON (
            (ranking.ranking_ts >= key_timestamps.ranking_ts
              AND ranking.ranking_ts < key_timestamps.ranking_ts_next)
            AND (ranking.woeid = $1)
          )
        GROUP BY
          key_timestamps.ranking_ts
        ORDER BY
          key_timestamps.ranking_ts ASC;
        """,
        woeid
    )
