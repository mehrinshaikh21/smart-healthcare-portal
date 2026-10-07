import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medical_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER NOT NULL,

    checkup_date TEXT NOT NULL,

    blood_pressure TEXT,

    blood_sugar TEXT,

    weight TEXT,

    doctor_notes TEXT,

    FOREIGN KEY (patient_id) REFERENCES patients(id)

)
""")

connection.commit()
connection.close()

print("✅ Medical History Table Created Successfully!")