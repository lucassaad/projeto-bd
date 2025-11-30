CREATE OR REPLACE PROCEDURE create_appointment(
    IN p_doctor_cpf  VARCHAR(11),
    IN p_patient_cpf VARCHAR(11),
    IN p_ubs_cnes    VARCHAR(7),
    IN p_datetime    TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se o médico existe
    IF NOT EXISTS (SELECT 1 FROM doctor WHERE cpf = p_doctor_cpf) THEN
        RAISE EXCEPTION 'Médico com CPF % não existe.', p_doctor_cpf;
    END IF;

    -- Verificar se o paciente existe
    IF NOT EXISTS (SELECT 1 FROM patient WHERE cpf = p_patient_cpf) THEN
        RAISE EXCEPTION 'Paciente com CPF % não existe.', p_patient_cpf;
    END IF;

    -- Verificar se a UBS existe
    IF NOT EXISTS (SELECT 1 FROM ubs WHERE cnes = p_ubs_cnes) THEN
        RAISE EXCEPTION 'UBS com CNES % não existe.', p_ubs_cnes;
    END IF;

    -- Inserir o appointment
    INSERT INTO appointment (
        doctor_cpf,
        patient_cpf,
        ubs_cnes,
        appointment_datetime
    )
    VALUES (
        p_doctor_cpf,
        p_patient_cpf,
        p_ubs_cnes,
        p_datetime
    );

END;
$$;
