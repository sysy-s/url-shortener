"""empty message

Revision ID: b54818c96667
Revises: 3311af6249cd
Create Date: 2022-02-17 20:46:08.081519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b54818c96667'
down_revision = '3311af6249cd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('visits', sa.Column('cookies', sa.String()))
    pass


def downgrade():
    op.drop_column('visits', 'cookies')
    pass
