"""create common table

Revision ID: c20ccdc8e870
Revises: 
Create Date: 2024-06-16 19:34:42.960835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c20ccdc8e870'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'configuration',
        sa.Column('key', sa.String(length=100), nullable=False, unique=True),
        sa.Column('value', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('key'),
    )


def downgrade() -> None:
    op.drop_table('configuration')
