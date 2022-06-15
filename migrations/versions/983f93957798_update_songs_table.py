"""Update songs table

Revision ID: 983f93957798
Revises: 4160798edd33
Create Date: 2022-06-15 15:55:38.299426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '983f93957798'
down_revision = '4160798edd33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('valence', sa.Numeric(precision=3, scale=2), nullable=True))
    op.drop_column('songs', 'preview_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('preview_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('songs', 'valence')
    # ### end Alembic commands ###