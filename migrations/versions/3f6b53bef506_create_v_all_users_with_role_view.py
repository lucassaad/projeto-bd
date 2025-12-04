from alembic import op
from typing import Union, Sequence

# revision identifiers, used by Alembic.
revision: str = '3f6b53bef506'
down_revision: Union[str, Sequence[str], None] = '50df9a68b449'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


op.execute("""
        CREATE VIEW v_all_users_with_role AS
        SELECT
            u.cpf,
            u.name,
            u.email,
            u.phone_number,
            CASE
                WHEN EXISTS (
                    SELECT 1 
                    FROM doctor d 
                    WHERE d.cpf = u.cpf
                ) THEN 'Doctor'
                WHEN EXISTS (
                    SELECT 1
                    FROM patient p
                    WHERE p.cpf = u.cpf
                ) THEN 'Patient'
                ELSE 'Unknown'
            END AS role,
            (
                SELECT s.name
                FROM doctor_specialty ds
                JOIN specialty s ON s.code = ds.specialty_code
                WHERE ds.doctor_cpf = u.cpf
                LIMIT 1
            ) AS specialty_name
        FROM "user" u;
    """)


def downgrade():
    op.execute("DROP VIEW IF EXISTS v_all_users_with_role;")