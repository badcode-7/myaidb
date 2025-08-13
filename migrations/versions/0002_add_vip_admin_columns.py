"""Add is_vip and is_admin columns to users table

Revision ID: 0002
Revises: 0001
Create Date: 2025-08-13 14:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', 
        sa.Column('is_vip', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('users',
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('users', 'is_vip')
    op.drop_column('users', 'is_admin')
