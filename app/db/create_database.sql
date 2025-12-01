CREATE TABLE ubs (
    cnes CHAR(7) PRIMARY KEY,
    nome VARCHAR(100),
    endereco VARCHAR(200)
);

CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    cpf CHAR(11) UNIQUE NOT NULL,
    nome VARCHAR(100),
    telefone VARCHAR(20),
    data_nascimento DATE
);

CREATE TABLE medic (
    cpf CHAR(11) PRIMARY KEY REFERENCES usuario(cpf),
    crm CHAR(6) UNIQUE NOT NULL
);

CREATE TABLE nurse (
    cpf CHAR(11) PRIMARY KEY REFERENCES usuario(cpf),
    coren CHAR(8) UNIQUE NOT NULL
);

CREATE TABLE pacient (
    cpf CHAR(11) PRIMARY KEY REFERENCES usuario(cpf)
);

CREATE TABLE appointment (
    data_hora TIMESTAMP,
    cpf_medico CHAR(11) REFERENCES medico(cpf),
    cpf_paciente CHAR(11) REFERENCES paciente(cpf),
    cnes_ubs CHAR(7) REFERENCES ubs(cnes),
    PRIMARY KEY (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
);

CREATE TABLE exam (
    data_agendamento TIMESTAMP,
    tipo INT,
    data_hora TIMESTAMP,
    cpf_medico CHAR(11),
    cpf_paciente CHAR(11),
    cnes_ubs CHAR(7),
    PRIMARY KEY (tipo, data_hora, cpf_medico, cpf_paciente, cnes_ubs),
    FOREIGN KEY (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
        REFERENCES consulta (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
);

CREATE TABLE prescription (
    data DATE,
    descricao TEXT,
    data_hora TIMESTAMP,
    cpf_medico CHAR(11),
    cpf_paciente CHAR(11),
    cnes_ubs CHAR(7),
    PRIMARY KEY (data_hora, cpf_medico, cpf_paciente, cnes_ubs),
    FOREIGN KEY (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
        REFERENCES consulta (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
);

CREATE TABLE specialty (
    tipo INT PRIMARY KEY
);

CREATE TABLE vaccine (
    nome_vacina VARCHAR(100),
    fabricante VARCHAR(100),
    descricao TEXT,
    cpf_paciente CHAR(11) REFERENCES paciente(cpf),
    cpf_enfermeiro CHAR(11) REFERENCES enfermeiro(cpf),
    PRIMARY KEY (nome_vacina, cpf_paciente)
);

CREATE TABLE medication (
    codigo_anvisa INT PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT
);

CREATE TABLE doctor_ubs (
    cpf_medico CHAR(11) REFERENCES medico(cpf),
    cnes_ubs CHAR(7) REFERENCES ubs(cnes),
    PRIMARY KEY (cpf_medico, cnes_ubs)
);

CREATE TABLE nurse_ubs (
    cpf_enfermeiro CHAR(11) REFERENCES enfermeiro(cpf),
    cnes_ubs CHAR(7) REFERENCES ubs(cnes),
    PRIMARY KEY (cpf_enfermeiro, cnes_ubs)
);

CREATE TABLE pacient_ubs (
    cpf_paciente CHAR(11) REFERENCES paciente(cpf),
    cnes_ubs CHAR(7) REFERENCES ubs(cnes),
    PRIMARY KEY (cpf_paciente, cnes_ubs)
);

CREATE TABLE medication_prescription (
    codigo_anvisa INT REFERENCES medicamento(codigo_anvisa),
    data_hora TIMESTAMP,
    cpf_medico CHAR(11),
    cpf_paciente CHAR(11),
    cnes_ubs CHAR(7),
    PRIMARY KEY (codigo_anvisa, data_hora, cpf_medico, cpf_paciente, cnes_ubs),
    FOREIGN KEY (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
        REFERENCES prescricao (data_hora, cpf_medico, cpf_paciente, cnes_ubs)
);

CREATE TABLE nurse_specialty (
    cpf CHAR(11) REFERENCES enfermeiro(cpf),
    tipo INT REFERENCES especialidade(tipo),
    PRIMARY KEY (cpf, tipo)
);

CREATE TABLE especialidade_medico (
    tipo INT REFERENCES especialidade(tipo),
    cpf CHAR(11) REFERENCES medico(cpf),
    PRIMARY KEY (tipo, cpf)
);
