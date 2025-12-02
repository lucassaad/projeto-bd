from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.exam import ExamIn, ExamUpdate


def create_exam(exam: ExamIn, session: Session):

    existing_exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE 
                appointment_id = :appointment_id
            AND 
                exam_type = :exam_type
        """),
            {'appointment_id': exam.appointment_id, 'exam_type': exam.exam_type},
        )
        .mappings()
        .first()
    )

    if existing_exam is not None:
        return None

    session.execute(
        text("""
            INSERT INTO "exam"
            (appointment_id, exam_date, exam_type)
            VALUES
            (:appointment_id, :exam_date, :exam_type)
        """),
        exam.model_dump(),
    )

    session.commit()

    db_exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE 
                appointment_id = :appointment_id
            AND 
                exam_type = :exam_type
        """),
            {'appointment_id': exam.appointment_id, 'exam_type': exam.exam_type},
        ).mappings().first()
    )

    return db_exam


def select_exam(id: str, session: Session):
    exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE id = :id
        """),
            {'id': id},
        ).mappings().first()
    )

    if exam is None:
        return None

    return dict(exam)


def select_all_exams(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "exams"
        """)
        ).mappings().fetchall()
    )

    exams = [dict(row) for row in result]

    return exams


def update_exam(exam_info: ExamUpdate, id: int, session: Session):

    exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE id = :id
        """),
            {'id': id},
        ).mappings().first()
    )

    if exam is None:
        return None

    session.execute(
        text("""
            UPDATE "exam" SET
                exam_date = :exam_date,
                exam_type = :exam_type
            WHERE id = :id
        """),
        {**exam_info.model_dump(), 'id': id, 'appointment_id': exam.appointment_id},
    )

    session.commit()

    updated_exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_exam


def delete_exam_db(id: int, session: Session):

    exam = (
        session.execute(
            text("""
            SELECT * FROM "exam"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if exam is None:
        return None

    session.execute(
        text("""
            DELETE FROM "exam"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(exam)
