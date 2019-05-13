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


async def get_active_locations():
    return await execute_fetch_query(
        """
        WITH active_locations as (
          SELECT DISTINCT
            woeid
          FROM
            data.rankings
          WHERE
            ranking_ts >= (
              (SELECT MAX(ranking_ts) FROM data.rankings)
              - interval '12 hours'
            )
        ), active_locations_as_geojson as (
          SELECT
            jsonb_build_object(
              'type', 'Feature',
              'id', locs.id,
              'geometry', ST_AsGeoJSON(locs.the_geom_point)::jsonb,
              'properties', json_build_object(
                'name', locs.name,
                'osm_name', locs.osm_name
              )
            ) AS feature
          FROM
            active_locations al
            JOIN data.locations locs ON al.woeid = locs.id
        )

        SELECT
          jsonb_build_object(
            'type', 'FeatureCollection',
            'features', jsonb_agg(feature)
          )
        FROM
          active_locations_as_geojson
        """,
        fetch_row=True
    )
