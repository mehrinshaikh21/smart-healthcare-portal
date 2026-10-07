import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

# Doctors table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT UNIQUE NOT NULL,

    email TEXT UNIQUE NOT NULL,

    specialization TEXT NOT NULL,

    mobile TEXT NOT NULL,

    password TEXT NOT NULL

)
""")

# Doctor 1
cursor.execute("""
INSERT OR IGNORE INTO doctors
(full_name, email, specialization, mobile, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "Dr. Amit Sharma",
    "amit.doctor@gmail.com",
    "General Medicine",
    "9876543210",
    "amit123"
))

# Doctor 2
cursor.execute("""
INSERT OR IGNORE INTO doctors
(full_name, email, specialization, mobile, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "Dr. Priya Patil",
    "priya.doctor@gmail.com",
    "Cardiology",
    "9876543211",
    "priya123"
))

# Doctor 3
cursor.execute("""
INSERT OR IGNORE INTO doctors
(full_name, email, specialization, mobile, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "Dr. Rahul Mehta",
    "rahul.doctor@gmail.com",
    "Orthopedics",
    "9876543212",
    "rahul123"
))

# Doctor 4
cursor.execute("""
INSERT OR IGNORE INTO doctors
(full_name, email, specialization, mobile, password)
VALUES (?, ?, ?, ?, ?)
""", (
    "Dr. Neha Khan",
    "neha.doctor@gmail.com",
    "Dermatology",
    "9876543213",
    "neha123"
))

connection.commit()
connection.close()

print("✅ Doctors Table Updated Successfully!")
print("✅ All 4 Doctors Added Successfully!")