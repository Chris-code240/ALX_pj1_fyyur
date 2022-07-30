"""empty message

Revision ID: ed1d7abf25bb
Revises: e96e81798b20
Create Date: 2022-07-28 16:21:15.436258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed1d7abf25bb'
down_revision = 'e96e81798b20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist_search', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Artist_search', 'Artist', ['artist_id'], ['id'])
    op.add_column('Venue_search', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Venue_search', 'Venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue_search', type_='foreignkey')
    op.drop_column('Venue_search', 'venue_id')
    op.drop_constraint(None, 'Artist_search', type_='foreignkey')
    op.drop_column('Artist_search', 'artist_id')
    # ### end Alembic commands ###
