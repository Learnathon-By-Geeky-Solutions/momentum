"""Updated user table structure

Revision ID: 6d723cc4e39e
Revises: 4e646dc250eb
Create Date: 2025-02-10 11:16:47.253869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d723cc4e39e'
down_revision: Union[str, None] = '4e646dc250eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add 'role' column with a default value for existing rows
    op.add_column('user', sa.Column('role', sa.String(), nullable=False, server_default="Customer"))
    
    # If you need to remove the default constraint later, use this:
    op.execute("ALTER TABLE \"user\" ALTER COLUMN role DROP DEFAULT")

def downgrade():
    # Remove the 'role' column if the migration is rolled back
    op.drop_column('user', 'role')
