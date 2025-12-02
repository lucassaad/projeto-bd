"""appointment trigger

Revision ID: b7092c398ef6
Revises: 583c93d81a75
Create Date: 2025-12-02 01:01:01.720891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7092c398ef6'
down_revision: Union[str, Sequence[str], None] = '583c93d81a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE OR REPLACE FUNCTION check_appointment_conflict()
    RETURNS TRIGGER AS $$
    DECLARE
        doctor_name TEXT;
    BEGIN
        SELECT u.name INTO doctor_name
        FROM doctor d
        JOIN "user" u ON d.cpf = u.cpf
        WHERE d.cpf = NEW.doctor_cpf;

        IF EXISTS (
            SELECT 1
            FROM appointment
            WHERE doctor_cpf = NEW.doctor_cpf
              AND appointment_datetime = NEW.appointment_datetime
              AND id <> COALESCE(NEW.id, 0)
        ) THEN
            RAISE EXCEPTION 'Conflict: Doctor % already has an appointment scheduled at %.',
                doctor_name, NEW.appointment_datetime;
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER trg_check_appointment_conflict
    BEFORE INSERT OR UPDATE ON appointment
    FOR EACH ROW
    EXECUTE FUNCTION check_appointment_conflict();
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_check_appointment_conflict ON appointment;")
    op.execute("DROP FUNCTION IF EXISTS check_appointment_conflict();")

