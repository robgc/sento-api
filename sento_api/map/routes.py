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

from starlette.responses import PlainTextResponse
from starlette.routing import Router

from sento_api.map import model
from sento_api import utils

app = Router()


@app.route('/active')
async def active_locations(request):
    query_results = await model.get_active_locations()
    return PlainTextResponse(query_results[0], media_type='application/json')


@app.route('/{trend_id}')
async def locations_by_trend(request):
    trend_id, trend_err_resp = await utils.process_req_trend(request)
    if trend_err_resp:
        return trend_err_resp

    locations_data = await model.get_locations_by_trend(trend_id)

    return PlainTextResponse(locations_data[0], media_type='application/json')
