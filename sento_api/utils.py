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

from starlette.responses import JSONResponse

from sento_api.db_connection import get_conn_pool


async def execute_fetch_query(sql_str, *args, fetch_row=False):
    result = None
    pool = await get_conn_pool()
    async with pool.acquire() as conn:
        if fetch_row:
            result = await conn.fetchrow(sql_str, *args)
        else:
            result = await conn.fetch(sql_str, *args)
    return result


async def check_location_existence(woeid):
    return await execute_fetch_query(
        """
        SELECT
          exists(
            SELECT 1
            FROM data.locations
            WHERE
              id = $1
          )
        AS "exists"
        """,
        woeid,
        fetch_row=True
    )


async def check_trend_existence(trend_id):
    return await execute_fetch_query(
        """
        SELECT
          exists(
            SELECT 1
            FROM data.topics
            WHERE
              id = $1
          )
        AS "exists"
        """,
        trend_id,
        fetch_row=True
    )


async def process_location(woeid):
    exists_qry_res = await check_location_existence(woeid)
    location_exists = exists_qry_res.get('exists')

    if not location_exists:
        return JSONResponse(
            {'errorDescription': 'The location could not be found'},
            status_code=404
        )
    else:
        return None


async def process_trend(trend_id):
    exists_qry_res = await check_trend_existence(trend_id)
    trend_exists = exists_qry_res.get('exists')

    if not trend_exists:
        return JSONResponse(
            {'errorDescription': 'The trend could not be found'},
            status_code=404
        )
    else:
        return None


async def process_req_woeid(request):
    woeid = request.path_params.get('woeid', None)

    non_existent_woeid_resp = await process_location(woeid)

    if non_existent_woeid_resp:
        return woeid, non_existent_woeid_resp

    return woeid, None


async def process_req_trend(request):
    trend_id = request.path_params.get('trend_id', None)

    non_existent_trend_id_resp = await process_trend(trend_id)

    if non_existent_trend_id_resp:
        return trend_id, non_existent_trend_id_resp

    return trend_id, None
