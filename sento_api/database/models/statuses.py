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


from sqlalchemy import Integer, BigInteger, Column, Text, SmallInteger, Index
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sento_api.database.models.base import Base, SCHEMAS


class Statuses(Base):
    __tablename__ = 'statuses'
    __table_args__ = (
        Index(
            'ix_gist_data_statuses_topic_id',
            'topic_id',
            postgresql_using='gist',
            postgresql_ops={'topic_id': 'gist_trgm_ops'}
        ),
        {'schema': SCHEMAS['data']}
    )
    id = Column(BigInteger, primary_key=True)
    wrote_at = Column(TIMESTAMP, nullable=False, index=True)
    fetched_at = Column(TIMESTAMP, nullable=False)
    content = Column(Text, nullable=False)
    # -1: Negative || 0: Neutral || 1: Positive || NULL: Not analyzed
    sentiment = Column(SmallInteger, nullable=True, index=True)
    topic_id = Column(Text, primary_key=True, index=True)
    woeid = Column(Integer, primary_key=True, index=True)
