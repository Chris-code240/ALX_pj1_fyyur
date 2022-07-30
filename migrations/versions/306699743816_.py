"""empty message

Revision ID: 306699743816
Revises: b8e04d7bd913
Create Date: 2022-07-27 19:21:31.263549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '306699743816'
down_revision = 'b8e04d7bd913'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
