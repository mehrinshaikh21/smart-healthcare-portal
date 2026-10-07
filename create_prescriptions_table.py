import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prescriptions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER NOT NULL,

    medicine_name TEXT NOT NULL,

    dosage TEXT NOT NULL,

    morning INTEGER DEFAULT 0,

    afternoon INTEGER DEFAULT 0,

    night INTEGER DEFAULT 0,

    duration TEXT,

    instructions TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id) REFERENCES patients(id)

)
""")

connection.commit()
connection.close()

print("✅ Prescriptions Table Created Successfully!")