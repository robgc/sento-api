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
from starlette.responses import PlainTextResponse

from sento_api.settings import get_config
from sento_api.map.routes import app as map_routes

app_settings = get_config()
app = Starlette(debug=app_settings.DEBUG_MODE)

app.mount('/map', map_routes)


@app.route('/')
def index(request):
    return PlainTextResponse('Sento API v1')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=3000)
