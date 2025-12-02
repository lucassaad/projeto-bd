"""add detailed_appointments view

Revision ID: 583c93d81a75
Revises: ee6d85022b55
Create Date: 2025-12-02 00:17:27.049967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '583c93d81a75'
down_revision: Union[str, Sequence[str], None] = 'ee6d85022b55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""CREATE VIEW detailed_appointments AS
    SELECT 
    a.id AS appointment_id,
    a.date AS "date",
    a.time AS "time",
    a.status AS status,

    p.id AS patient_id,
    p.name AS patient_name,
    p.cpf AS patient_cpf,

    d.id AS doctor_id,
    d.name AS doctor_name,
    ds.speciality AS doctor_specialty,

    n.id AS nurse_id,
    n.name AS nurse_name,

    u.cnes AS ubs_cnes,
    u.name AS ubs_name

FROM appointment a
LEFT JOIN patient p ON p.cpf = a.patient_cpf
LEFT JOIN doctor d ON d.cpf = a.doctor_cpf
LEFT JOIN doctor_speciality ds ON ds.doctor_cpf = d.cpf
LEFT JOIN nurse n ON n.cpf = a.nurse_cpf
LEFT JOIN ubs u ON u.cnes = a.ubs_cnes;
""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW  IF EXISTS detailed_appointments;")