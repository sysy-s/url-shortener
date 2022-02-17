"""last fix for real

Revision ID: 3311af6249cd
Revises: 243a532b07e8
Create Date: 2022-02-17 18:20:00.364995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3311af6249cd'
down_revision = '243a532b07e8'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('urls', 'created', nullable=False, server_default=sa.func.now())
    pass


def downgrade():
    op.alter_column('urls', 'created', nullable=False)
    pass
