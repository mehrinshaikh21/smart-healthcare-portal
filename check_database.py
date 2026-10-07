import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

print("\n===== DATABASE TABLES =====\n")

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

tables = cursor.fetchall()

for table in tables:
    print("📁", table[0])


print("\n===== REGISTERED PATIENTS =====\n")

cursor.execute("SELECT * FROM patients")

patients = cursor.fetchall()

for patient in patients:
    print(patient)


print("\n===== REGISTERED DOCTORS =====\n")

cursor.execute("SELECT * FROM doctors")

doctors = cursor.fetchall()

for doctor in doctors:
    print(doctor)


print("\n===== APPOINTMENTS =====\n")

cursor.execute("SELECT * FROM appointments")

appointments = cursor.fetchall()

for appointment in appointments:
    print(appointment)


print("\n===== MEDICAL HISTORY TABLE =====\n")

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table' AND name='medical_history'
""")

medical_history_table = cursor.fetchone()

if medical_history_table:
    cursor.execute("SELECT * FROM medical_history")

    history = cursor.fetchall()

    for record in history:
        print(record)

else:
    print("ℹ️ Medical history table does not exist yet.")


connection.close()

print("\n✅ Database Check Completed Successfully!")