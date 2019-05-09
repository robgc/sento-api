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


async def get_sentiment_data(woeid, trend_id, timestamp):
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
          ORDER BY
            ranking_ts ASC
        ), key_ranking_ts AS (
          SELECT
            ranking_ts,
            coalesce(
              lead(ranking_ts, 1) OVER (ORDER BY ranking_ts ASC),
              now() AT TIME ZONE 'UTC'
            ) AS ranking_ts_next
          FROM
            ranking_ts_diffs
          WHERE
            ts_diff IS NULL
            OR extract('minute' FROM ts_diff)::int >= 10
        ), key_ranking_ts_limit AS (
          SELECT
            ranking_ts_next AS "limit"
          FROM
            key_ranking_ts
          WHERE
            date_trunc('second', ranking_ts) = date_trunc(
                'second', $3::timestamp without time zone)
        )

        SELECT
          sts.sentiment,
          count(sts.sentiment) AS total_count
        FROM
          data.statuses sts
          JOIN key_ranking_ts_limit key_ts_limit ON (
            sts.wrote_at <= key_ts_limit. "limit"
          )
        WHERE
          sts.woeid = $1
          AND topic_id = $2
        GROUP BY
          sts.sentiment
        """,
        woeid,
        trend_id,
        timestamp
    )
