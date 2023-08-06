CREATE TABLE IF NOT EXISTS patient_table (
	patient_uid TEXT NOT NULL,
	age TEXT,
	gender TEXT,
	weight INTEGER,
    patient_name TEXT,
    bmi INTEGER,
    patient_size FLOAT,
    PRIMARY KEY (patient_uid)
);
