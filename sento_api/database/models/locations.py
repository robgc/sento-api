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

from geoalchemy2 import Geometry
from sqlalchemy import Column, Index, Integer, Text, Float

from sento_api.database.models.base import SCHEMAS, Base
from sento_api.database.operations.procedure import Procedure
from sento_api.database.operations.trigger import Trigger


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = (
        Index('idx_locations_the_geom', 'the_geom', postgresql_using='gist'),
        Index('idx_locations_coords', 'coords', postgresql_using='gist'),
        {'schema': SCHEMAS['data']}
    )
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    osm_name = Column(Text)
    the_geom = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False),
        nullable=False
    )
    coords = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        nullable=False
    )
    bounding_circle_coords = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        nullable=False
    )
    bounding_circle_radius = Column(Float, nullable=False)


# create view tmp1 as
# select
#   min_circle."id",
#   min_circle.name,
#   min_circle.center,
#   ST_DistanceSphere(min_circle.center, min_circle.perimeter_point) as distance,
#   min_circle.the_geom
# from (
#   SELECT
#     "id",
#     "name",
#     ST_MakeValid(ST_MinimumBoundingCircle(the_geom)) AS the_geom,
#     ST_Centroid(ST_MakeValid(ST_MinimumBoundingCircle(the_geom))) as center,
#   	ST_PointN(ST_Boundary(ST_MakeValid(ST_MinimumBoundingCircle(the_geom))), 1) as perimeter_point
#   FROM "data"."locations"
# ) As "min_circle"

# TODO: FINISH PROCEDURE

bounding_circle_plgsql = """
DECLARE
    center geometry;
    radius double precision;
BEGIN
    SELECT INTO center FROM SELECT
END;
"""


Procedure(
    name='calculate_location_bounding_circle',
    return_type='trigger',
    function_decl=bounding_circle_plgsql
)

Trigger()
