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


from sqlalchemy import Column, Text, Index

from sento_api.database.models.base import Base, SCHEMAS


class Topics(Base):
    __tablename__ = 'topics'
    __table_args__ = (
        Index(
            'ix_data_topics_id',
            'id',
            postgresql_using='gist',
            postgresql_ops={'id': 'gist_trgm_ops'}
        ),
        {'schema': SCHEMAS['data']}
    )
    id = Column(Text, primary_key=True)
    url = Column(Text, nullable=False)
    query_str = Column(Text, nullable=False)
