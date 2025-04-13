"""new new

Revision ID: efc2d2b3a635
Revises: 16fae346a794
Create Date: 2025-03-15 00:04:36.756689

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "efc2d2b3a635"
down_revision: Union[str, None] = "16fae346a794"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
