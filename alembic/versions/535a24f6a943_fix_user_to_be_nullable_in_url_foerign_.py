"""fix user to be nullable in url foerign key

Revision ID: 535a24f6a943
Revises: bbb1582444ca
Create Date: 2022-02-17 18:02:14.782050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '535a24f6a943'
down_revision = 'bbb1582444ca'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('urls', 'user_id', nullable=True)
    pass


def downgrade():
    op.alter_column('urls', 'user_id', nullable=False)
    pass
