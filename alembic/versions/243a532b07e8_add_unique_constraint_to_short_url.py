"""add unique constraint to short url

Revision ID: 243a532b07e8
Revises: 535a24f6a943
Create Date: 2022-02-17 18:08:59.833417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243a532b07e8'
down_revision = '535a24f6a943'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('unique_short_url', 'urls', ['short'])
    pass


def downgrade():
    op.drop_constraint('unique_short_url', 'urls', ['short'])
    pass
