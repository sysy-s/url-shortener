"""create all tables

Revision ID: bbb1582444ca
Revises: 
Create Date: 2022-02-17 17:33:58.670981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbb1582444ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    
    op.create_table('urls',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('long', sa.String(), nullable=False),
                    sa.Column('short', sa.String(), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column('last_clicked', sa.TIMESTAMP(timezone=True)),
                    sa.Column('click_count', sa.Integer(), nullable=False, default=0),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    
    op.create_table('visits',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('client_host', sa.String()),
                    sa.Column('headers', sa.String()),
                    sa.Column('time', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
                    sa.Column('url_id', sa.Integer(), sa.ForeignKey('urls.id', ondelete='CASCADE')),
                    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade():
    op.drop_table('users')
    op.drop_table('urls')
    op.drop_table('visits')
    pass
