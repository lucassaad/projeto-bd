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
    op.execute("""
        CREATE VIEW detailed_appointments AS
        SELECT 
            a.appointment_datetime AS appointment_datetime,
            a.patient_cpf AS patient_cpf,
            p_user.name AS patient_name,
            a.doctor_cpf AS doctor_cpf,
            d_user.name AS doctor_name,
            s.name AS doctor_specialty,
            a.ubs_cnes AS ubs_cnes,
            u.name AS ubs_name
        FROM appointment a
        LEFT JOIN "user" p_user ON p_user.cpf = a.patient_cpf
        LEFT JOIN "user" d_user ON d_user.cpf = a.doctor_cpf
        LEFT JOIN doctor_specialty ds ON ds.doctor_cpf = a.doctor_cpf
        LEFT JOIN specialty s ON s.code = ds.specialty_code
        LEFT JOIN ubs u ON u.cnes = a.ubs_cnes;
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS detailed_appointments;")

