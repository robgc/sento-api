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
from sqlalchemy import Column, Float, Index, Integer, Text

from sento_api.database.models.base import SCHEMAS, Base


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = (
        Index('idx_locations_the_geom', 'the_geom', postgresql_using='gist'),
        Index('idx_locations_the_geom_point',
              'the_geom_point', postgresql_using='gist'),
        Index('idx_locations_the_geom_bcircle_centroid',
              'the_geom_bcircle_centroid', postgresql_using='gist'),
        {'schema': SCHEMAS['data']}
    )
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    osm_name = Column(Text)
    the_geom = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False),
        nullable=False
    )
    the_geom_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        nullable=False
    )
    the_geom_bcircle_centroid = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False),
        nullable=False
    )
    bcircle_radius = Column(Float, nullable=False)
