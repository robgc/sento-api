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

import json

from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Router

from sento_api import utils
from sento_api.trends import model

app = Router()


@app.route('/top')
async def get_top_trends(request):
    query_results = await model.get_top_trends()
    return JSONResponse([row.get('topic_id') for row in query_results])


@app.route('/{woeid:int}')
async def get_trends_for_location(request):
    woeid, err_resp = await utils.process_req_woeid(request)
    if err_resp:
        return err_resp

    trends_rows = await model.get_current_trends_for_location(woeid)
    return JSONResponse(
        [dict(row) for row in trends_rows]
    )


@app.route('/evolution/{woeid:int}')
async def get_trends_evolution_in_location(request):
    woeid, err_resp = await utils.process_req_woeid(request)
    if err_resp:
        return err_resp

    evol_rows = await model.get_trends_evolution_in_location(woeid)
    return JSONResponse(
        [dict(timestamp=row[0], positions=json.loads(row[1]))
         for row in evol_rows]
    )


@app.route('/evolution/{woeid:int}/{trend_id}')
async def get_trend_evolution_in_location(request):
    woeid, err_resp = await utils.process_req_woeid(request)
    if err_resp:
        return err_resp

    trend_id, trend_err_resp = await utils.process_req_trend(request)
    if trend_err_resp:
        return trend_err_resp

    evol_data = await model.get_trend_evolution_in_location(trend_id, woeid)

    return PlainTextResponse(evol_data[0], media_type='application/json')


@app.route('/search/{trend_name}')
async def search_trends_by_name(request):
    trend_name = request.path_params.get('trend_name')

    search_rows = await model.search_trends_by_name(trend_name)

    if len(search_rows):
        return JSONResponse([dict(row) for row in search_rows])
    else:
        return JSONResponse(dict(), status_code=404)
