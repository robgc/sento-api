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


async def get_global_sentiment_data(trend_id):
    return await execute_fetch_query(
        """
        SELECT
          CASE
            WHEN sentiment = 1 THEN 'positive'
            WHEN sentiment = 0 THEN 'neutral'
            ELSE 'negative'
          END AS sentiment,
          count(sentiment) AS "tweetCount"
        FROM
          data.statuses
        WHERE
          topic_id = $1
        GROUP BY
          sentiment
        """,
        trend_id
    )


async def get_sentiment_data(trend_id, woeid):
    return await execute_fetch_query(
        """
        SELECT
          CASE
            WHEN sentiment = 1 THEN 'positive'
            WHEN sentiment = 0 THEN 'neutral'
            ELSE 'negative'
          END AS sentiment,
          count(sentiment) AS "tweetCount"
        FROM
          data.statuses
        WHERE
          woeid = $1
          AND topic_id = $2
        GROUP BY
          sentiment
        """,
        woeid,
        trend_id,
    )


async def get_sentiment_data_at_timestamp(trend_id, woeid, timestamp):
    return await execute_fetch_query(
        """
        WITH key_ranking_stamps AS (
          SELECT
            ranking_ts,
            coalesce(
              lead(ranking_ts, 1) OVER (ORDER BY ranking_ts ASC),
              now() at time zone 'UTC'
            ) AS ranking_ts_next
          FROM
            data.rankings
          WHERE
            woeid = $1
          GROUP BY
            ranking_ts
          ORDER BY
            ranking_ts ASC
        )

        SELECT
          CASE
            WHEN statuses.sentiment = 1 THEN 'positive'
            WHEN statuses.sentiment = 0 THEN 'neutral'
            ELSE 'negative'
          END AS sentiment,
          count(statuses.sentiment) AS total_count
        FROM
          data.statuses statuses
          JOIN key_ranking_stamps key_stamps ON (
            key_stamps.ranking_ts = $3
            AND statuses.wrote_at < key_stamps.ranking_ts_next
          )
        WHERE
          statuses.woeid = $1
          AND topic_id = $2
        GROUP BY
          statuses.sentiment
        """,
        woeid,
        trend_id,
        timestamp
    )


async def get_trend_metadata(trend_id, woeid):
    return await execute_fetch_query(
        """
        WITH statuses_metadata AS (
          SELECT
            count(*) AS "processedTweets"
          FROM
            data.statuses
          WHERE
            topic_id = $2
            AND woeid = $1
        ), trends_metadata AS (
          SELECT
            tweet_volume AS "lastTweetVolume",
            to_char(
              ranking_ts,
              'YYYY-MM-DD"T"HH24:MI:SS"Z"'
            ) AS "lastTrendCaptureTimestamp"
          FROM
            data.rankings
          WHERE
            topic_id = $2
            AND woeid = $1
          ORDER BY
            ranking_ts DESC
          LIMIT 1
        )

        SELECT
          sm."processedTweets",
          tm."lastTweetVolume",
          tm."lastTrendCaptureTimestamp"
        FROM
          statuses_metadata sm
          JOIN trends_metadata tm ON TRUE
        """,
        woeid,
        trend_id,
        fetch_row=True
    )
