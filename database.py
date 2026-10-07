import sqlite3

# Database se connect karo (agar database nahi hai to automatically ban jayegi)
connection = sqlite3.connect("hospital.db")

# Cursor banao
cursor = connection.cursor()

# Patients table create karo
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    mobile TEXT NOT NULL,

    dob TEXT NOT NULL,

    gender TEXT NOT NULL,

    address TEXT NOT NULL,

    password TEXT NOT NULL

)
""")

# Appointments table create karo
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_name TEXT NOT NULL,

    doctor TEXT NOT NULL,

    department TEXT NOT NULL,

    appointment_date TEXT NOT NULL,

    appointment_time TEXT NOT NULL,

    reason TEXT NOT NULL,

    status TEXT DEFAULT 'Pending'

)
""")

# Changes save karo
connection.commit()

# Connection close karo
connection.close()

print("✅ Database Created Successfully!")