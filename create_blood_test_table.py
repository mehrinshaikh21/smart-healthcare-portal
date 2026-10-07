import sqlite3


connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS blood_test_requests (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER NOT NULL,

    test_name TEXT NOT NULL,

    collection_type TEXT NOT NULL,

    appointment_date TEXT NOT NULL,

    appointment_time TEXT NOT NULL,

    address TEXT NOT NULL,

    status TEXT DEFAULT 'Pending',

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id) REFERENCES patients(id)

)
""")


connection.commit()
connection.close()


print("✅ Blood Test Requests Table Created Successfully!")