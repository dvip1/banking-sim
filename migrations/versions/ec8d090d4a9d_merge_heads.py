"""merge heads

Revision ID: ec8d090d4a9d
Revises: 7b3b60fa3b2e, 8656d6e81d5a
Create Date: 2026-02-21 17:29:29.992202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec8d090d4a9d'
down_revision: Union[str, Sequence[str], None] = ('7b3b60fa3b2e', '8656d6e81d5a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
