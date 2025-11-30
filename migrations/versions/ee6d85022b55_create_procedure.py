"""create_procedure

Revision ID: ee6d85022b55
Revises: 80ff1947312d
Create Date: 2025-11-30 15:46:04.321953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'ee6d85022b55'
down_revision: Union[str, Sequence[str], None] = '80ff1947312d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sql = open("app/db/create_appointment_procedure.sql", "r", encoding="utf-8").read()
    op.execute(text(sql))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP PROCEDURE IF EXISTS criar_appointment;")
