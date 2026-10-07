from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# ===========================
# Create Medical Records Table
# ===========================

def create_medical_records_table():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_date TEXT,
            blood_pressure TEXT,
            blood_sugar TEXT,
            symptoms TEXT,
            diagnosis TEXT,
            treatment TEXT,
            doctor_name TEXT
        )
    """)

    connection.commit()
    connection.close()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE email=? AND password=?",
            (email, password)
        )

        patient = cursor.fetchone()

        connection.close()

        if patient:

            session['patient_id'] = patient[0]
            session['patient_name'] = patient[1]
            session['patient_email'] = patient[2]

            return redirect(url_for('patient_dashboard'))

        else:
            return "❌ Invalid Email or Password"

    return render_template("patient_login.html")

# ===========================
# Doctor Login
# ===========================

@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM doctors WHERE email=? AND password=?",
            (email, password)
        )

        doctor = cursor.fetchone()

        connection.close()

        if doctor:

            session['doctor_id'] = doctor[0]
            session['doctor_name'] = doctor[1]
            session['doctor_email'] = doctor[2]

            return redirect(url_for('doctor_dashboard'))

        else:
            return "❌ Invalid Doctor Email or Password"

    return render_template("doctor_login.html")

# ===========================
# Admin Login
# ===========================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM admins WHERE email=? AND password=?",
            (email, password)
        )

        admin = cursor.fetchone()

        connection.close()

        if admin:

            session['admin_id'] = admin[0]
            session['admin_name'] = admin[1]
            session['admin_email'] = admin[2]

            return redirect(url_for('admin_dashboard'))

        else:
            return "❌ Invalid Admin Email or Password"

    return render_template("admin_login.html")

# ===========================
# Admin Dashboard
# ===========================

@app.route('/admin-dashboard')
def admin_dashboard():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template(
        "admin_dashboard.html",
        admin_name=session.get('admin_name')
    )

# ===========================
# Admin - Manage Doctors
# ===========================

@app.route('/admin-doctors')
def admin_doctors():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, full_name, email, mobile, specialization
        FROM doctors
        ORDER BY id DESC
    """)

    doctors = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_doctors.html",
        doctors=doctors
    )

# ===========================
# Admin - Add Doctor
# ===========================

@app.route('/admin-add-doctor', methods=['GET', 'POST'])
def admin_add_doctor():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        mobile = request.form['mobile']
        specialization = request.form['specialization']
        password = request.form['password']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO doctors
            (full_name, email, mobile, specialization, password)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            mobile,
            specialization,
            password
        ))

        connection.commit()
        connection.close()

        return redirect(url_for('admin_doctors'))

    return render_template("admin_add_doctor.html")

# ===========================
# Admin - Edit Doctor
# ===========================

@app.route('/admin-edit-doctor/<int:doctor_id>', methods=['GET', 'POST'])
def admin_edit_doctor(doctor_id):

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get doctor details
    cursor.execute("""
        SELECT id, full_name, email, mobile, specialization, password
        FROM doctors
        WHERE id = ?
    """, (doctor_id,))

    doctor = cursor.fetchone()

    if doctor is None:
        connection.close()
        return "❌ Doctor not found"

    # Update doctor
    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        mobile = request.form['mobile']
        specialization = request.form['specialization']
        password = request.form['password']

        if password.strip():

            cursor.execute("""
                UPDATE doctors
                SET full_name = ?,
                    email = ?,
                    mobile = ?,
                    specialization = ?,
                    password = ?
                WHERE id = ?
            """, (
                full_name,
                email,
                mobile,
                specialization,
                password,
                doctor_id
            ))

        else:

            cursor.execute("""
                UPDATE doctors
                SET full_name = ?,
                    email = ?,
                    mobile = ?,
                    specialization = ?
                WHERE id = ?
            """, (
                full_name,
                email,
                mobile,
                specialization,
                doctor_id
            ))

        connection.commit()
        connection.close()

        return redirect(url_for('admin_doctors'))

    connection.close()

    return render_template(
        "admin_edit_doctor.html",
        doctor=doctor
    )

# ===========================
# Admin - Delete Doctor
# ===========================

@app.route('/admin-delete-doctor/<int:doctor_id>', methods=['POST'])
def admin_delete_doctor(doctor_id):

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM doctors
        WHERE id = ?
    """, (doctor_id,))

    connection.commit()
    connection.close()

    return redirect(url_for('admin_doctors'))

# ===========================
# Public - View Doctors
# ===========================

@app.route('/doctors')
def public_doctors():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT full_name, specialization
        FROM doctors
        ORDER BY id ASC
    """)

    doctors = cursor.fetchall()

    connection.close()

    return render_template(
        "doctors.html",
        doctors=doctors
    )

# ===========================
# Admin - Manage Patients
# ===========================

@app.route('/admin-patients')
def admin_patients():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, full_name, email, mobile, dob, gender, address
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_patients.html",
        patients=patients
    )

# ===========================
# Admin - Manage Appointments
# ===========================

@app.route('/admin-appointments')
def admin_appointments():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM appointments
        ORDER BY appointment_date DESC
    """)

    appointments = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_appointments.html",
        appointments=appointments
    )

# ===========================
# Doctor Dashboard
# ===========================

@app.route('/doctor-dashboard')
def doctor_dashboard():

    # Check if doctor is logged in
    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    return render_template(
        "doctor_dashboard.html",
        doctor_name=session['doctor_name']
    )

# ===========================
# Doctor Today's Appointments
# ===========================

@app.route('/doctor-appointments')
def doctor_appointments():

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    doctor_name = session['doctor_name']
    today = date.today().isoformat()

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM appointments
    WHERE doctor = ?
    AND appointment_date = ?
    ORDER BY appointment_time
    """, (
        doctor_name,
        today
    ))

    appointments = cursor.fetchall()

    connection.close()

    return render_template(
        "doctor_appointments.html",
        appointments=appointments,
        doctor_name=doctor_name
    )

# ===========================
# Doctor Blood Test Requests
# ===========================

@app.route('/doctor-blood-tests')
def doctor_blood_tests():

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        blood_test_requests.id,
        patients.full_name,
        blood_test_requests.test_name,
        blood_test_requests.collection_type,
        blood_test_requests.appointment_date,
        blood_test_requests.appointment_time,
        blood_test_requests.address,
        blood_test_requests.status
    FROM blood_test_requests
    JOIN patients
    ON blood_test_requests.patient_id = patients.id
    ORDER BY
        blood_test_requests.appointment_date,
        blood_test_requests.appointment_time
    """)

    requests = cursor.fetchall()

    connection.close()

    return render_template(
        "doctor_blood_tests.html",
        requests=requests
    )

# ===========================
# Accept Blood Test Request
# ===========================

@app.route('/accept-blood-test/<int:request_id>')
def accept_blood_test(request_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE blood_test_requests
    SET status = 'Accepted'
    WHERE id = ?
    """, (request_id,))

    connection.commit()
    connection.close()

    return redirect(url_for('doctor_blood_tests'))

# ===========================
# Complete Blood Test Request
# ===========================

@app.route('/complete-blood-test/<int:request_id>')
def complete_blood_test(request_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE blood_test_requests
    SET status = 'Completed'
    WHERE id = ?
    """, (request_id,))

    connection.commit()
    connection.close()

    return redirect(url_for('doctor_blood_tests'))

# ===========================
# Doctor My Patients
# ===========================

@app.route('/doctor-patients')
def doctor_patients():

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, full_name, email, mobile, dob, gender
    FROM patients
    ORDER BY full_name
    """)

    patients = cursor.fetchall()

    connection.close()

    return render_template(
        "doctor_patients.html",
        patients=patients
    )

# ===========================
# Patient Medical History
# ===========================

@app.route('/patient-medical-history/<int:patient_id>')
def patient_medical_history(patient_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get patient details
    cursor.execute("""
    SELECT id, full_name, email, mobile, dob, gender, address
    FROM patients
    WHERE id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    # Get medical history
    cursor.execute("""
    SELECT id, checkup_date, blood_pressure, blood_sugar, weight, doctor_notes
    FROM medical_history
    WHERE patient_id = ?
    ORDER BY checkup_date DESC
    """, (patient_id,))

    history = cursor.fetchall()

    # Get prescriptions
    cursor.execute("""
    SELECT id, medicine_name, dosage, morning, afternoon, night, duration, instructions
    FROM prescriptions
    WHERE patient_id = ?
    ORDER BY id DESC
    """, (patient_id,))

    prescriptions = cursor.fetchall()

    connection.close()

    if patient is None:
        return "❌ Patient not found"

    return render_template(
        "patient_medical_history.html",
        patient=patient,
        history=history,
        prescriptions=prescriptions
    )
    

# ===========================
# Add Medical Record
# ===========================

@app.route('/add-medical-record/<int:patient_id>', methods=['GET', 'POST'])
def add_medical_record(patient_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get patient details
    cursor.execute("""
    SELECT id, full_name
    FROM patients
    WHERE id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    if patient is None:
        connection.close()
        return "❌ Patient not found"

    if request.method == 'POST':

        checkup_date = request.form['checkup_date']
        blood_pressure = request.form['blood_pressure']
        blood_sugar = request.form['blood_sugar']
        weight = request.form['weight']
        doctor_notes = request.form['doctor_notes']

        cursor.execute("""
        INSERT INTO medical_history
        (
            patient_id,
            checkup_date,
            blood_pressure,
            blood_sugar,
            weight,
            doctor_notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            checkup_date,
            blood_pressure,
            blood_sugar,
            weight,
            doctor_notes
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for(
                'patient_medical_history',
                patient_id=patient_id
            )
        )

    connection.close()

    return render_template(
        "add_medical_record.html",
        patient=patient
    )

# ===========================
# Edit Medical Record
# ===========================

@app.route('/edit-medical-record/<int:record_id>', methods=['GET', 'POST'])
def edit_medical_record(record_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get existing medical record
    cursor.execute("""
    SELECT *
    FROM medical_history
    WHERE id = ?
    """, (record_id,))

    record = cursor.fetchone()

    if record is None:
        connection.close()
        return "❌ Medical record not found"

    if request.method == 'POST':

        checkup_date = request.form['checkup_date']
        blood_pressure = request.form['blood_pressure']
        blood_sugar = request.form['blood_sugar']
        weight = request.form['weight']
        doctor_notes = request.form['doctor_notes']

        cursor.execute("""
        UPDATE medical_history
        SET
            checkup_date = ?,
            blood_pressure = ?,
            blood_sugar = ?,
            weight = ?,
            doctor_notes = ?
        WHERE id = ?
        """, (
            checkup_date,
            blood_pressure,
            blood_sugar,
            weight,
            doctor_notes,
            record_id
        ))

        connection.commit()

        patient_id = record[1]

        connection.close()

        return redirect(
            url_for(
                'patient_medical_history',
                patient_id=patient_id
            )
        )

    connection.close()

    return render_template(
        "edit_medical_record.html",
        record=record
    )

# ===========================
# Delete Medical Record
# ===========================

@app.route('/delete-medical-record/<int:record_id>', methods=['POST'])
def delete_medical_record(record_id):

    if 'doctor_id' not in session:
        return redirect(url_for('doctor_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get patient ID before deleting
    cursor.execute("""
    SELECT patient_id
    FROM medical_history
    WHERE id = ?
    """, (record_id,))

    record = cursor.fetchone()

    if record is None:
        connection.close()
        return "❌ Medical record not found"

    patient_id = record[0]

    # Delete record
    cursor.execute("""
    DELETE FROM medical_history
    WHERE id = ?
    """, (record_id,))

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            'patient_medical_history',
            patient_id=patient_id
        )
    )

@app.route('/patient-register', methods=['GET', 'POST'])
def patient_register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        mobile = request.form['mobile']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO patients
        (full_name, email, mobile, dob, gender, address, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            mobile,
            dob,
            gender,
            address,
            password
        ))

        connection.commit()
        connection.close()

        return redirect(url_for('patient_login'))

    return render_template('patient_register.html')


@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    if request.method == 'POST':

        patient_name = request.form['patient_name']
        doctor = request.form['doctor']
        department = request.form['department']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        reason = request.form['reason']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO appointments
        (patient_name, doctor, department, appointment_date, appointment_time, reason)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_name,
            doctor,
            department,
            appointment_date,
            appointment_time,
            reason
        ))

        connection.commit()
        connection.close()

        return render_template(
            "appointment_success.html",
            patient_name=patient_name,
            doctor=doctor,
            department=department,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

    return render_template("book_appointment.html")


@app.route('/patient-dashboard')
def patient_dashboard():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    return render_template(
        "patient_dashboard.html",
        patient_name=session['patient_name']
    )

@app.route("/my-prescriptions")
def my_prescriptions():

    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    patient_id = session["patient_id"]

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            medicine_name,
            dosage,
            morning,
            afternoon,
            night,
            duration,
            instructions
        FROM prescriptions
        WHERE patient_id = ?
        ORDER BY id DESC
    """, (patient_id,))

    prescriptions = cursor.fetchall()

    connection.close()

    return render_template(
        "my_prescriptions.html",
        prescriptions=prescriptions
    )

# ===========================
# Blood Test Home Service
# ===========================

@app.route('/blood-test', methods=['GET', 'POST'])
def blood_test():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    if request.method == 'POST':

        test_name = request.form['test_name']
        collection_type = request.form['collection_type']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        address = request.form['address']

        connection = sqlite3.connect("hospital.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO blood_test_requests
        (
            patient_id,
            test_name,
            collection_type,
            appointment_date,
            appointment_time,
            address
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session['patient_id'],
            test_name,
            collection_type,
            appointment_date,
            appointment_time,
            address
        ))

        connection.commit()
        connection.close()

        return render_template(
            "blood_test_success.html",
            test_name=test_name,
            collection_type=collection_type,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

    return render_template("blood_test.html")

# ===========================
# Admin - Blood Test Requests
# ===========================

@app.route('/admin-blood-tests')
def admin_blood_tests():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            blood_test_requests.id,
            patients.full_name,
            blood_test_requests.test_name,
            blood_test_requests.collection_type,
            blood_test_requests.appointment_date,
            blood_test_requests.appointment_time,
            blood_test_requests.address
        FROM blood_test_requests
        LEFT JOIN patients
        ON blood_test_requests.patient_id = patients.id
        ORDER BY blood_test_requests.id DESC
    """)

    requests = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_blood_tests.html",
        requests=requests
    )

# ===========================
# Admin - Medical Records
# ===========================

@app.route('/admin-medical-records')
def admin_medical_records():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            medical_history.id,
            patients.full_name,
            medical_history.checkup_date,
            medical_history.blood_pressure,
            medical_history.blood_sugar,
            medical_history.weight,
            medical_history.doctor_notes
        FROM medical_history
        JOIN patients
        ON medical_history.patient_id = patients.id
        ORDER BY medical_history.checkup_date DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_medical_records.html",
        records=records
    )

# ===========================
# My Profile
# ===========================

@app.route('/my-profile')
def my_profile():

    # Check if patient is logged in
    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (session['patient_id'],)
    )

    patient = cursor.fetchone()

    connection.close()

    return render_template(
        "my_profile.html",
        patient=patient
    )

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():

    if 'patient_id' not in session:
        return redirect('/patient-login')

    connection = sqlite3.connect('hospital.db')
    cursor = connection.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        mobile = request.form['mobile']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']

        cursor.execute("""
            UPDATE patients
            SET full_name = ?,
                email = ?,
                mobile = ?,
                dob = ?,
                gender = ?,
                address = ?
            WHERE id = ?
        """, (
            full_name,
            email,
            mobile,
            dob,
            gender,
            address,
            session['patient_id']
        ))

        connection.commit()
        connection.close()

        session['patient_name'] = full_name
        session['patient_email'] = email

        return redirect('/my-profile')

    cursor.execute(
        "SELECT * FROM patients WHERE id = ?",
        (session['patient_id'],)
    )

    patient = cursor.fetchone()
    connection.close()

    return render_template('edit_profile.html', patient=patient)

# ===========================
# My Appointments
# ===========================

@app.route('/my-appointments')
def my_appointments():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM appointments
    ORDER BY appointment_date, appointment_time
    """)

    appointments = cursor.fetchall()

    connection.close()

    return render_template(
        "my_appointments.html",
        appointments=appointments
    )

# ===========================
# Logout
# ===========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))

@app.route("/add-prescription/<int:patient_id>", methods=["GET", "POST"])
def add_prescription(patient_id):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if not patient:
        connection.close()
        return "Patient not found"

    if request.method == "POST":

        medicine_names = request.form.getlist("medicine_name[]")
        dosages = request.form.getlist("dosage[]")
        durations = request.form.getlist("duration[]")
        instructions = request.form.getlist("instructions[]")

        for index in range(len(medicine_names)):

            medicine_name = medicine_names[index]
            dosage = dosages[index]

            duration = ""
            if index < len(durations):
                duration = durations[index]

            instruction = ""
            if index < len(instructions):
                instruction = instructions[index]


            # Check timing for this particular medicine

            morning = 1 if request.form.get(
                f"medicine_{index}_morning"
            ) else 0

            afternoon = 1 if request.form.get(
                f"medicine_{index}_afternoon"
            ) else 0

            night = 1 if request.form.get(
                f"medicine_{index}_night"
            ) else 0


            cursor.execute("""
                INSERT INTO prescriptions
                (
                    patient_id,
                    medicine_name,
                    dosage,
                    morning,
                    afternoon,
                    night,
                    duration,
                    instructions
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id,
                medicine_name,
                dosage,
                morning,
                afternoon,
                night,
                duration,
                instruction
            ))


        connection.commit()
        connection.close()

        return redirect(
            url_for(
                "patient_medical_history",
                patient_id=patient_id
            )
        )


    connection.close()

    return render_template(
        "add_prescription.html",
        patient=patient)

# ===========================
# Admin - System Overview
# ===========================

@app.route('/admin-overview')
def admin_overview():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Total Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    # Total Doctors
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]

    # Total Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    # Total Blood Test Requests
    cursor.execute("SELECT COUNT(*) FROM blood_test_requests")
    total_blood_tests = cursor.fetchone()[0]

    # Total Medical Records
    cursor.execute("SELECT COUNT(*) FROM medical_history")
    total_records = cursor.fetchone()[0]

    # Completed Blood Test Reports
    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM blood_test_requests
            WHERE status = 'Completed'
        """)

        completed_reports = cursor.fetchone()[0]

    except sqlite3.OperationalError:

        completed_reports = 0

    connection.close()

    return render_template(
        "admin_overview.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_blood_tests=total_blood_tests,
        total_records=total_records,
        completed_reports=completed_reports
    )

# ===========================
# Blood Test Report Fields
# ===========================

def setup_blood_test_reports():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    columns = [
        ("result", "TEXT"),
        ("normal_range", "TEXT"),
        ("impression", "TEXT"),
        ("technician_name", "TEXT"),
        ("technician_qualification", "TEXT"),
        ("laboratory_name", "TEXT")
    ]

    for column_name, column_type in columns:

        try:
            cursor.execute(
                f"ALTER TABLE blood_test_requests ADD COLUMN {column_name} {column_type}"
            )
        except sqlite3.OperationalError:
            pass

    connection.commit()
    connection.close()


setup_blood_test_reports()

# ===========================
# Lab Technician Login
# ===========================

@app.route('/lab-login', methods=['GET', 'POST'])
def lab_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if email == 'nayeem@healthcarelab.com' and password == 'lab123':

            session['lab_technician'] = True
            session['lab_name'] = 'Nayeem Shaikh'

            return redirect(url_for('lab_dashboard'))

        else:
            return "❌ Invalid Lab Technician Email or Password"

    return render_template("lab_login.html")


# ===========================
# Lab Technician Dashboard
# ===========================

@app.route('/lab-dashboard')
def lab_dashboard():

    if 'lab_technician' not in session:
        return redirect(url_for('lab_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            blood_test_requests.id,
            patients.full_name,
            blood_test_requests.test_name,
            blood_test_requests.collection_type,
            blood_test_requests.appointment_date,
            blood_test_requests.appointment_time,
            blood_test_requests.address,
            blood_test_requests.status
        FROM blood_test_requests
        JOIN patients
        ON blood_test_requests.patient_id = patients.id
        ORDER BY
            blood_test_requests.appointment_date,
            blood_test_requests.appointment_time
    """)

    requests = cursor.fetchall()

    connection.close()

    return render_template(
        "lab_dashboard.html",
        requests=requests,
        lab_name=session.get('lab_name')
    )


# ===========================
# Lab Technician Logout
# ===========================

@app.route('/lab-logout')
def lab_logout():

    session.pop('lab_technician', None)
    session.pop('lab_name', None)

    return redirect(url_for('login'))

    # ===========================
# Enter Blood Test Report
# ===========================

@app.route('/lab-report/<int:request_id>', methods=['GET', 'POST'])
def lab_report(request_id):

    if 'lab_technician' not in session:
        return redirect(url_for('lab_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    if request.method == 'POST':

        result = request.form['result']
        normal_range = request.form['normal_range']
        impression = request.form['impression']

        cursor.execute("""
            UPDATE blood_test_requests
            SET
                result = ?,
                normal_range = ?,
                impression = ?,
                technician_name = ?,
                technician_qualification = ?,
                laboratory_name = ?,
                status = 'Completed'
            WHERE id = ?
        """, (
            result,
            normal_range,
            impression,
            'Nayeem Shaikh',
            'B.Sc. Chem., C.M.L.T., D.M.L.T.',
            'Healthcare Clinical Laboratory',
            request_id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for('lab_dashboard'))

    cursor.execute("""
        SELECT
            blood_test_requests.id,
            patients.full_name,
            blood_test_requests.test_name,
            blood_test_requests.collection_type,
            blood_test_requests.appointment_date,
            blood_test_requests.appointment_time,
            blood_test_requests.address,
            blood_test_requests.status
        FROM blood_test_requests
        JOIN patients
        ON blood_test_requests.patient_id = patients.id
        WHERE blood_test_requests.id = ?
    """, (request_id,))

    request_data = cursor.fetchone()

    connection.close()

    if not request_data:
        return "Blood test request not found"

    return render_template(
        "lab_report.html",
        request_data=request_data
    )

# ===========================
# Patient Blood Test Reports
# ===========================

@app.route('/my-blood-test-reports')
def my_blood_test_reports():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            test_name,
            collection_type,
            appointment_date,
            appointment_time,
            address,
            result,
            normal_range,
            impression,
            technician_name,
            technician_qualification,
            laboratory_name,
            status
        FROM blood_test_requests
        WHERE patient_id = ?
        AND status = 'Completed'
        ORDER BY id DESC
    """, (session['patient_id'],))

    reports = cursor.fetchall()

    connection.close()

    return render_template(
        "my_blood_test_reports.html",
        reports=reports
    )

# ===========================
# View Full Blood Test Report
# ===========================

@app.route('/blood-test-report/<int:request_id>')
def blood_test_report(request_id):

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            blood_test_requests.id,
            patients.full_name,
            patients.gender,
            patients.dob,
            patients.mobile,
            blood_test_requests.test_name,
            blood_test_requests.collection_type,
            blood_test_requests.appointment_date,
            blood_test_requests.appointment_time,
            blood_test_requests.address,
            blood_test_requests.result,
            blood_test_requests.normal_range,
            blood_test_requests.impression,
            blood_test_requests.technician_name,
            blood_test_requests.technician_qualification,
            blood_test_requests.laboratory_name,
            blood_test_requests.status
        FROM blood_test_requests
        JOIN patients
        ON blood_test_requests.patient_id = patients.id
        WHERE blood_test_requests.id = ?
        AND blood_test_requests.patient_id = ?
    """, (request_id, session['patient_id']))

    report = cursor.fetchone()

    connection.close()

    if not report:
        return "Blood test report not found."

    return render_template(
        "blood_test_report.html",
        report=report
    )

# ===========================
# Patient Medical Records
# ===========================

@app.route('/patient-medical-records')
def patient_medical_records():

    if 'patient_id' not in session:
        return redirect(url_for('patient_login'))

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            record_date,
            blood_pressure,
            blood_sugar,
            symptoms,
            diagnosis,
            treatment,
            doctor_name
        FROM medical_records
        WHERE patient_id = ?
        ORDER BY id DESC
    """, (session['patient_id'],))

    records = cursor.fetchall()

    connection.close()

    return render_template(
        "patient_medical_records.html",
        records=records
    )

# ===========================
# Admin - Lab Technician
# ===========================

@app.route('/admin-lab-technician')
def admin_lab_technician():

    technician = {
        'name': 'Nayeem Shaikh',
        'qualification': 'B.Sc. Chem., C.M.L.T., D.M.L.T.',
        'laboratory': 'Healthcare Clinical Laboratory',
        'email': 'nayeem@healthcarelab.com',
        'role': 'Laboratory Technician'
    }

    return render_template(
        'admin_lab_technician.html',
        technician=technician
    )

# ===========================
# Public - About
# ===========================

@app.route('/about')
def about():
    return render_template("about.html")

# ===========================
# Public - Contact
# ===========================

@app.route('/contact')
def contact():
    return render_template("contact.html")

# ===========================
# Public - Learn More
# ===========================

@app.route('/learn-more')
def learn_more():
    return render_template("learn_more.html")

if __name__ == '__main__':

    create_medical_records_table()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)