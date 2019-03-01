"""baseline

Revision ID: 2af73696b043
Revises:
Create Date: 2019-03-01 20:46:45.782933+00:00

"""

# flake8: noqa

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from sento_api.database.operations.procedure import Procedure
from sento_api.database.operations.trigger import Trigger

# revision identifiers, used by Alembic.
revision = '2af73696b043'
down_revision = None
branch_labels = None
depends_on = None

bounding_circle_plgsql = """
DECLARE
    bounding_circle geometry;
BEGIN
    bounding_circle := ST_MakeValid(ST_MinimumBoundingCircle(NEW.the_geom));
    NEW.the_geom_bcircle_centroid := ST_Centroid(bounding_circle);
    NEW.bcircle_radius := ST_DistanceSphere(
        NEW.the_geom_bcircle_centroid,
        ST_PointN(ST_Boundary(bounding_circle), 1)
    );
    RETURN NEW;
END;
"""

bounding_circle_proc = Procedure(
    name='calculate_bcircle_cols',
    return_type='trigger',
    function_decl=bounding_circle_plgsql
)

bounding_circle_trigger = Trigger(
    name='trigger_calculate_bcircle_cols',
    when='BEFORE',
    event='INSERT OR UPDATE',
    table_name='data.locations',
    additional_opts='FOR EACH ROW',
    function_type='FUNCTION',
    function_name='calculate_bcircle_cols',
    function_args=list()
)


def upgrade():
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('osm_name', sa.Text(), nullable=True),
    sa.Column('the_geom', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False), nullable=False),
    sa.Column('the_geom_point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, spatial_index=False), nullable=False),
    sa.Column('the_geom_bcircle_centroid', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, spatial_index=False), nullable=False),
    sa.Column('bcircle_radius', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='data'
    )

    op.create_procedure(bounding_circle_proc)
    op.create_trigger(bounding_circle_trigger)

    op.create_index('idx_locations_the_geom', 'locations', ['the_geom'], unique=False, schema='data', postgresql_using='gist')
    op.create_index('idx_locations_the_geom_bcircle_centroid', 'locations', ['the_geom_bcircle_centroid'], unique=False, schema='data', postgresql_using='gist')
    op.create_index('idx_locations_the_geom_point', 'locations', ['the_geom_point'], unique=False, schema='data', postgresql_using='gist')
    op.create_table('rankings',
    sa.Column('ranking_ts', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('ranking_no', sa.SmallInteger(), nullable=False),
    sa.Column('woeid', sa.Integer(), nullable=False),
    sa.Column('tweet_volume', sa.Integer(), nullable=True),
    sa.Column('topic_id', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('ranking_ts', 'ranking_no', 'topic_id'),
    schema='data'
    )

    op.create_index(op.f('ix_data_rankings_woeid'), 'rankings', ['woeid'], unique=False, schema='data')
    op.create_table('statuses',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('wrote_at', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('fetched_at', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('topic_id', sa.Text(), nullable=False),
    sa.Column('woeid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'topic_id', 'woeid'),
    schema='data'
    )

    op.create_index(op.f('ix_data_statuses_wrote_at'), 'statuses', ['wrote_at'], unique=False, schema='data')
    op.create_table('topics',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('query_str', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='data'
    )


def downgrade():
    op.drop_table('topics', schema='data')

    op.drop_index(op.f('ix_data_statuses_wrote_at'), table_name='statuses', schema='data')
    op.drop_table('statuses', schema='data')

    op.drop_index(op.f('ix_data_rankings_woeid'), table_name='rankings', schema='data')
    op.drop_table('rankings', schema='data')

    op.drop_index('idx_locations_the_geom_point', table_name='locations', schema='data')
    op.drop_index('idx_locations_the_geom_bcircle_centroid', table_name='locations', schema='data')
    op.drop_index('idx_locations_the_geom', table_name='locations', schema='data')
    op.drop_trigger(bounding_circle_trigger)
    op.drop_procedure(bounding_circle_proc)
    op.drop_table('locations', schema='data')
