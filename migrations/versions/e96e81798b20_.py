"""empty message

Revision ID: e96e81798b20
Revises: 306699743816
Create Date: 2022-07-28 11:17:24.094365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e96e81798b20'
down_revision = '306699743816'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=255), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=255), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Venue_search')
    op.drop_table('Artist_search')
    # ### end Alembic commands ###
