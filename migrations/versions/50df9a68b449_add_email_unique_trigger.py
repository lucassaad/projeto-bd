"""add email unique trigger

Revision ID: 50df9a68b449
Revises: adad021050f5
Create Date: 2025-12-04 13:40:10.293443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50df9a68b449'
down_revision: Union[str, Sequence[str], None] = 'adad021050f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    -- Função que valida se o e-mail já existe antes de inserir um usuário
    CREATE OR REPLACE FUNCTION check_email_uniqueness()
    RETURNS trigger AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "user" WHERE email = NEW.email) THEN
            RAISE EXCEPTION 'E-mail % já está em uso.', NEW.email;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Trigger que chama a função antes de inserir um novo usuário
    CREATE TRIGGER trg_check_email_uniqueness
    BEFORE INSERT ON "user"
    FOR EACH ROW
    EXECUTE FUNCTION check_email_uniqueness();
    """)


def downgrade():
    op.execute("""
    DROP TRIGGER IF EXISTS trg_check_email_uniqueness ON users;
    DROP FUNCTION IF EXISTS check_email_uniqueness();
    """)
