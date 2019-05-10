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

from dateutil import parser
from starlette.responses import JSONResponse
from starlette.routing import Router

from sento_api import utils
from sento_api.reports import model

app = Router()


@app.route('/sentiment/{woeid:int}/{trend_id}/{timestamp}')
async def get_sentiment_report_by_location_and_trend(request):
    woeid, err_resp = await utils.process_req_woeid(request)
    if err_resp:
        return err_resp

    trend_id, trend_err_resp = await utils.process_req_trend(request)
    if trend_err_resp:
        return trend_err_resp

    req_timestamp = request.path_params.get('timestamp', None)

    timestamp_utc = (parser
                     .parse(req_timestamp)
                     .replace(tzinfo=None))

    sentiment_data = await model.get_sentiment_data(
        woeid, trend_id, timestamp_utc
    )

    return JSONResponse({row[0]: row[1] for row in sentiment_data})


@app.route('/trend/{trend_id}/{woeid:int}')
async def get_trend_metadata(request):
    woeid, err_resp = await utils.process_req_woeid(request)
    if err_resp:
        return err_resp

    trend_id, trend_err_resp = await utils.process_req_trend(request)
    if trend_err_resp:
        return trend_err_resp

    trend_metadata = await model.get_trend_metadata(woeid, trend_id)

    return JSONResponse(dict(trend_metadata))
