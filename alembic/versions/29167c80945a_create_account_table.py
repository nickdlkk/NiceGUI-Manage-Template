"""create account table

Revision ID: 29167c80945a
Revises: 799396eac938
Create Date: 2024-06-23 23:29:08.704809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29167c80945a'
down_revision: Union[str, None] = '799396eac938'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
