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
        medico_nome TEXT;
    BEGIN
        SELECT nome INTO medico_nome
        FROM medico
        WHERE cpf = NEW.cpf_medico;

        IF EXISTS (
            SELECT 1
            FROM appointment
            WHERE cpf_medico = NEW.cpf_medico
              AND data_hora = NEW.data_hora
              AND NOT (
                  cpf_paciente = COALESCE(OLD.cpf_paciente, '')
                  AND cnes_ubs = COALESCE(OLD.cnes_ubs, '')
                  AND data_hora = COALESCE(OLD.data_hora, '1900-01-01')
                  AND cpf_medico = COALESCE(OLD.cpf_medico, '')
              )
        ) THEN
            RAISE EXCEPTION 'Conflict: Doctor % already has an appointment scheduled at %.',
                medico_nome, NEW.data_hora;
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
