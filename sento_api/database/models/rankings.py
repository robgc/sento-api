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


from sqlalchemy import Column, Integer, SmallInteger, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sento_api.database.models.base import Base, SCHEMAS


class Rankings(Base):
    __tablename__ = 'rankings'
    __table_args__ = {'schema': SCHEMAS['data']}
    ranking_ts = Column(TIMESTAMP, nullable=False, index=True,
                        primary_key=True)
    ranking_no = Column(SmallInteger, nullable=False, primary_key=True)
    woeid = Column(Integer, nullable=False)
    tweet_volume = Column(Integer)
    topic_id = Column(Text, nullable=False, index=True, primary_key=True)
