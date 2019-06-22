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

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from sento_api.map.routes import app as map_routes
from sento_api.reports.routes import app as reports_routes
from sento_api.settings import get_config
from sento_api.trends.routes import app as trends_routes

app_settings = get_config()
app = Starlette(debug=app_settings.DEBUG_MODE)

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])

base_path = '/api/v1'

app.mount(f'{base_path}/map', map_routes)
app.mount(f'{base_path}/trends', trends_routes)
app.mount(f'{base_path}/reports', reports_routes)


@app.route(f'{base_path}')
def index(request):
    return PlainTextResponse('Sento API v1')


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app_settings.LISTEN_HOST,
        port=app_settings.LISTEN_PORT
    )
