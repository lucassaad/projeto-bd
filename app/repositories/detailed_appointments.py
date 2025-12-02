from sqlalchemy import text
from sqlalchemy.orm import Session

def get_detailed_appointments(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "detailed_appointments"
        """)
        )
        .mappings()
        .fetchall()
    )

    detailed_appointments = [dict(row) for row in result]

    return detailed_appointments