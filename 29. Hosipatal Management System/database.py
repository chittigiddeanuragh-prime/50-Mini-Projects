import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Users table (for Auth & Roles)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL, -- ADMIN, DOCTOR, RECEPTIONIST, PHARMACIST
        doctor_id TEXT
    );
    """)

    # 2. Doctors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        department TEXT NOT NULL,
        qualification TEXT NOT NULL,
        experience INTEGER NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        fee REAL NOT NULL,
        availability TEXT NOT NULL,
        room_number TEXT NOT NULL
    );
    """)

    # 3. Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        dob TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        emergency_contact TEXT NOT NULL,
        registration_date TEXT NOT NULL,
        assigned_doctor_id TEXT,
        department TEXT NOT NULL,
        patient_type TEXT NOT NULL, -- OPD, IPD, Emergency
        status TEXT NOT NULL DEFAULT 'Active', -- Active, Discharged
        FOREIGN KEY(assigned_doctor_id) REFERENCES doctors(doctor_id)
    );
    """)

    # 4. Appointments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id TEXT PRIMARY KEY,
        patient_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        doctor_id TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        department TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        reason TEXT NOT NULL,
        appointment_type TEXT NOT NULL, -- New, Follow-up, Routine
        status TEXT NOT NULL, -- Scheduled, Confirmed, Completed, Cancelled, No Show
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
    );
    """)

    # 5. Beds table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds (
        bed_id TEXT PRIMARY KEY,
        ward TEXT NOT NULL, -- ICU Ward, General Ward, Deluxe Ward, Emergency Ward
        room_number TEXT NOT NULL,
        bed_type TEXT NOT NULL, -- Standard, ICU Ventilator, Deluxe, Electric
        patient_id TEXT,
        patient_name TEXT,
        admission_date TEXT,
        status TEXT NOT NULL -- Available, Occupied, Reserved, Cleaning, Maintenance
    );
    """)

    # 6. Admissions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admissions (
        admission_id TEXT PRIMARY KEY,
        patient_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        doctor_id TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        ward TEXT NOT NULL,
        room_number TEXT NOT NULL,
        bed_id TEXT NOT NULL,
        admission_date TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        attendant_name TEXT NOT NULL,
        attendant_phone TEXT NOT NULL,
        initial_notes TEXT,
        status TEXT NOT NULL DEFAULT 'Admitted', -- Admitted, Discharged
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id),
        FOREIGN KEY(bed_id) REFERENCES beds(bed_id)
    );
    """)

    # Discharges table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discharges (
        discharge_id TEXT PRIMARY KEY,
        admission_id TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        discharge_date TEXT NOT NULL,
        final_diagnosis TEXT NOT NULL,
        treatment_summary TEXT NOT NULL,
        doctor_remarks TEXT,
        total_stay_days INTEGER NOT NULL,
        discharge_status TEXT NOT NULL DEFAULT 'Completed',
        FOREIGN KEY(admission_id) REFERENCES admissions(admission_id)
    );
    """)

    # 7. Pharmacy table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pharmacy (
        medicine_id TEXT PRIMARY KEY,
        medicine_name TEXT NOT NULL,
        category TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        batch_number TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        supplier TEXT NOT NULL
    );
    """)

    # Pharmacy Sales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pharmacy_sales (
        sale_id TEXT PRIMARY KEY,
        medicine_id TEXT NOT NULL,
        medicine_name TEXT NOT NULL,
        patient_id TEXT,
        patient_name TEXT,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY(medicine_id) REFERENCES pharmacy(medicine_id)
    );
    """)

    # 8. Laboratory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laboratory (
        test_id TEXT PRIMARY KEY,
        patient_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        doctor_id TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        test_name TEXT NOT NULL,
        test_date TEXT NOT NULL,
        sample_type TEXT NOT NULL, -- Blood, Urine, Swab, Imaging
        result TEXT,
        reference_range TEXT,
        status TEXT NOT NULL -- Pending, Processing, Completed
    );
    """)

    # 9. Billing table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        bill_id TEXT PRIMARY KEY,
        patient_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        patient_charges REAL NOT NULL DEFAULT 0.0,
        doctor_consultation REAL NOT NULL DEFAULT 0.0,
        room_charges REAL NOT NULL DEFAULT 0.0,
        bed_charges REAL NOT NULL DEFAULT 0.0,
        lab_charges REAL NOT NULL DEFAULT 0.0,
        medicine_charges REAL NOT NULL DEFAULT 0.0,
        other_charges REAL NOT NULL DEFAULT 0.0,
        subtotal REAL NOT NULL,
        discount REAL NOT NULL DEFAULT 0.0,
        tax REAL NOT NULL DEFAULT 0.0,
        grand_total REAL NOT NULL,
        payment_status TEXT NOT NULL, -- Paid, Partially Paid, Pending
        payment_method TEXT NOT NULL, -- Cash, UPI, Card, Net Banking
        bill_date TEXT NOT NULL
    );
    """)

    # 10. Emergency table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergencies (
        emergency_id TEXT PRIMARY KEY,
        patient_name TEXT NOT NULL,
        patient_id TEXT,
        arrival_time TEXT NOT NULL,
        priority TEXT NOT NULL, -- Critical, Urgent, Moderate, Stable
        symptoms TEXT NOT NULL,
        assigned_doctor_id TEXT,
        assigned_doctor_name TEXT,
        assigned_room TEXT NOT NULL,
        treatment_status TEXT NOT NULL -- Active, Under Treatment, Stabilized, Transferred
    );
    """)

    # 11. Patient Medical History table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT NOT NULL,
        record_date TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        treatment TEXT NOT NULL,
        doctor_notes TEXT,
        doctor_name TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    );
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    # Check if doctors exist
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    print("Seeding sample hospital data...")

    # Seed Users
    users_data = [
        ('admin', 'admin123', 'System Administrator', 'ADMIN', None),
        ('dr_ananya', 'doc123', 'Dr. Ananya Rao', 'DOCTOR', 'DOC-101'),
        ('dr_rajesh', 'doc123', 'Dr. Rajesh Kumar', 'DOCTOR', 'DOC-102'),
        ('receptionist', 'rec123', 'Priya Sharma (Receptionist)', 'RECEPTIONIST', None),
        ('pharmacist', 'pharma123', 'Ramesh Patel (Pharmacist)', 'PHARMACIST', None),
    ]
    cursor.executemany("INSERT INTO users (username, password, full_name, role, doctor_id) VALUES (?, ?, ?, ?, ?)", users_data)

    # Seed Doctors
    doctors_data = [
        ('DOC-101', 'Dr. Ananya Rao', 'Cardiology', 'Cardiology', 'MD, DM (Cardiology)', 14, '+91 98765 43210', 'ananya.rao@cityhospital.com', 1200.0, 'Mon - Fri (09:00 AM - 02:00 PM)', 'OPD-102'),
        ('DOC-102', 'Dr. Rajesh Kumar', 'Neurology', 'Neurology', 'MBBS, MCh (Neurosurgery)', 18, '+91 98765 43211', 'rajesh.kumar@cityhospital.com', 1500.0, 'Mon - Sat (10:00 AM - 04:00 PM)', 'OPD-205'),
        ('DOC-103', 'Dr. Sunita Patel', 'Pediatrics', 'Pediatrics', 'MD (Pediatrics)', 9, '+91 98765 43212', 'sunita.patel@cityhospital.com', 800.0, 'Mon - Sat (09:00 AM - 01:00 PM)', 'OPD-108'),
        ('DOC-104', 'Dr. Vikram Malhotra', 'Orthopedics', 'Orthopedics', 'MS (Orthopedics), FRCS', 16, '+91 98765 43213', 'vikram.m@cityhospital.com', 1100.0, 'Tue - Sun (11:00 AM - 05:00 PM)', 'OPD-301'),
        ('DOC-105', 'Dr. Kavita Reddy', 'Gynecology', 'Obstetrics & Gynae', 'MD, DNB (OBGYN)', 12, '+91 98765 43214', 'kavita.reddy@cityhospital.com', 1000.0, 'Mon - Fri (10:00 AM - 03:00 PM)', 'OPD-115'),
        ('DOC-106', 'Dr. Arvind Swamy', 'Emergency Medicine', 'Emergency', 'MD (Emergency Medicine)', 11, '+91 98765 43215', 'arvind.swamy@cityhospital.com', 900.0, '24x7 Shift Rotation', 'ER-01')
    ]
    cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", doctors_data)

    # Seed Patients
    patients_data = [
        ('P1024', 'Rahul Sharma', 34, 'Male', '1992-05-14', 'O+', '+91 91234 56789', 'rahul.s@gmail.com', 'Flat 402, Sunshine Apts, MG Road, Mumbai', '+91 98765 11111', '2026-08-10', 'DOC-101', 'Cardiology', 'OPD', 'Active'),
        ('P1025', 'Anita Verma', 45, 'Female', '1981-11-22', 'A+', '+91 91234 56790', 'anita.v@gmail.com', '12 Park Avenue, Koramangala, Bengaluru', '+91 98765 22222', '2026-08-15', 'DOC-102', 'Neurology', 'IPD', 'Active'),
        ('P1026', 'Suresh Gupta', 62, 'Male', '1964-03-08', 'B+', '+91 91234 56791', 'suresh.g@gmail.com', '88 Sector 15, Gurgaon, Haryana', '+91 98765 33333', '2026-08-20', 'DOC-104', 'Orthopedics', 'IPD', 'Active'),
        ('P1027', 'Meena Kumari', 28, 'Female', '1998-09-30', 'AB+', '+91 91234 56792', 'meena.k@gmail.com', '5-A Lakeview Enclave, Hyderabad', '+91 98765 44444', '2026-09-01', 'DOC-103', 'Pediatrics', 'OPD', 'Active'),
        ('P1028', 'Vikash Singh', 50, 'Male', '1976-12-18', 'O-', '+91 91234 56793', 'vikash.s@gmail.com', '140 Civil Lines, Jaipur', '+91 98765 55555', '2026-09-05', 'DOC-106', 'Emergency', 'Emergency', 'Active')
    ]
    cursor.executemany("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", patients_data)

    # Seed Appointments
    appointments_data = [
        ('APT-5001', 'P1024', 'Rahul Sharma', 'DOC-101', 'Dr. Ananya Rao', 'Cardiology', '2026-09-06', '10:30 AM', 'Routine Heart Checkup & ECG Review', 'Routine', 'Scheduled', 'Patient reports slight breathlessness on stairs'),
        ('APT-5002', 'P1027', 'Meena Kumari', 'DOC-103', 'Dr. Sunita Patel', 'Pediatrics', '2026-09-06', '11:15 AM', 'Child Vaccination & General Checkup', 'Routine', 'Confirmed', 'Bring immunization card'),
        ('APT-5003', 'P1025', 'Anita Verma', 'DOC-102', 'Dr. Rajesh Kumar', 'Neurology', '2026-09-06', '02:00 PM', 'Migraine Follow-up', 'Follow-up', 'Scheduled', 'MRI Brain report attached'),
        ('APT-5004', 'P1026', 'Suresh Gupta', 'DOC-104', 'Dr. Vikram Malhotra', 'Orthopedics', '2026-09-05', '03:30 PM', 'Knee Joint Pain Consultation', 'New', 'Completed', 'Advised X-Ray Right Knee & Physio'),
        ('APT-5005', 'P1028', 'Vikash Singh', 'DOC-106', 'Dr. Arvind Swamy', 'Emergency', '2026-09-06', '08:00 AM', 'Acute Abdominal Pain', 'Emergency', 'Completed', 'Transferred to ER Ward')
    ]
    cursor.executemany("INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", appointments_data)

    # Seed Beds (100 total beds initialized: 38 Available, 54 Occupied, 5 Reserved, 3 Maintenance)
    beds_data = []
    # ICU Wards (20 beds)
    for i in range(1, 21):
        bed_id = f"BED-ICU-{i:02d}"
        room = f"ICU-{100 + i}"
        btype = "ICU Ventilator"
        if i <= 14:
            status = "Occupied"
            p_id, p_name, adm_date = "P1025", "Anita Verma", "2026-08-28"
        elif i <= 17:
            status = "Available"
            p_id, p_name, adm_date = None, None, None
        elif i == 18:
            status = "Reserved"
            p_id, p_name, adm_date = None, None, None
        else:
            status = "Cleaning"
            p_id, p_name, adm_date = None, None, None
        beds_data.append((bed_id, "ICU Ward", room, btype, p_id, p_name, adm_date, status))

    # General Ward (50 beds)
    for i in range(1, 51):
        bed_id = f"BED-GEN-{i:02d}"
        room = f"GW-{(i // 5) + 200}"
        btype = "Standard"
        if i <= 30:
            status = "Occupied"
            p_id, p_name, adm_date = "P1026", "Suresh Gupta", "2026-08-30"
        elif i <= 46:
            status = "Available"
            p_id, p_name, adm_date = None, None, None
        elif i <= 48:
            status = "Reserved"
            p_id, p_name, adm_date = None, None, None
        else:
            status = "Maintenance"
            p_id, p_name, adm_date = None, None, None
        beds_data.append((bed_id, "General Ward", room, btype, p_id, p_name, adm_date, status))

    # Deluxe Ward (20 beds)
    for i in range(1, 21):
        bed_id = f"BED-DLX-{i:02d}"
        room = f"SUITE-{300 + i}"
        btype = "Deluxe Electric"
        if i <= 8:
            status = "Occupied"
            p_id, p_name, adm_date = "P1024", "Rahul Sharma", "2026-09-02"
        elif i <= 18:
            status = "Available"
            p_id, p_name, adm_date = None, None, None
        elif i == 19:
            status = "Reserved"
            p_id, p_name, adm_date = None, None, None
        else:
            status = "Maintenance"
            p_id, p_name, adm_date = None, None, None
        beds_data.append((bed_id, "Deluxe Ward", room, btype, p_id, p_name, adm_date, status))

    # Emergency Ward (10 beds)
    for i in range(1, 11):
        bed_id = f"BED-EMG-{i:02d}"
        room = f"ER-BED-{i}"
        btype = "Emergency Stretcher"
        if i <= 2:
            status = "Occupied"
            p_id, p_name, adm_date = "P1028", "Vikash Singh", "2026-09-06"
        elif i <= 9:
            status = "Available"
            p_id, p_name, adm_date = None, None, None
        else:
            status = "Reserved"
            p_id, p_name, adm_date = None, None, None
        beds_data.append((bed_id, "Emergency Ward", room, btype, p_id, p_name, adm_date, status))

    cursor.executemany("INSERT INTO beds VALUES (?, ?, ?, ?, ?, ?, ?, ?)", beds_data)

    # Seed Admissions
    admissions_data = [
        ('ADM-201', 'P1025', 'Anita Verma', 'DOC-102', 'Dr. Rajesh Kumar', 'ICU Ward', 'ICU-102', 'BED-ICU-02', '2026-08-28', 'Severe Migraine with Stroke Ruleout', 'Suresh Verma', '+91 98765 22222', 'Under observation in ICU', 'Admitted'),
        ('ADM-202', 'P1026', 'Suresh Gupta', 'DOC-104', 'Dr. Vikram Malhotra', 'General Ward', 'GW-201', 'BED-GEN-01', '2026-08-30', 'Post-Op Knee Arthroscopy', 'Ramesh Gupta', '+91 98765 33333', 'Post-operative recovery smooth', 'Admitted')
    ]
    cursor.executemany("INSERT INTO admissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", admissions_data)

    # Seed Pharmacy Stock (including low stock items: Paracetamol 12 units, Amoxicillin 8 units, Insulin 5 units)
    pharmacy_data = [
        ('MED-301', 'Paracetamol 650mg', 'Painkiller / Antipyretic', 'Cipla Ltd', 'BAT-2026-88', '2027-05-30', 12, 25.0, 'Apollo Pharma Distributors'),
        ('MED-302', 'Amoxicillin 500mg', 'Antibiotic', 'Sun Pharma', 'BAT-2026-12', '2026-10-15', 8, 85.0, 'MedPlus Wholesale'),
        ('MED-303', 'Human Insulin (10ml)', 'Hormone', 'Novo Nordisk', 'BAT-2026-04', '2026-09-25', 5, 450.0, 'BioCare India'),
        ('MED-304', 'Metformin 500mg', 'Antidiabetic', 'Torrent Pharma', 'BAT-2026-90', '2027-11-20', 150, 18.0, 'Apollo Pharma Distributors'),
        ('MED-305', 'Atorvastatin 10mg', 'Cardiovascular', 'Lupin Pharma', 'BAT-2026-55', '2027-08-14', 90, 110.0, 'Universal Pharma Supply'),
        ('MED-306', 'Pantoprazole 40mg', 'Antacid', 'Alkem Labs', 'BAT-2026-33', '2028-01-10', 200, 45.0, 'MedPlus Wholesale')
    ]
    cursor.executemany("INSERT INTO pharmacy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", pharmacy_data)

    # Seed Lab Tests
    lab_data = [
        ('LAB-701', 'P1024', 'Rahul Sharma', 'DOC-101', 'Dr. Ananya Rao', 'Complete Blood Count (CBC)', '2026-09-05', 'Blood', 'Hb: 14.2 g/dL, WBC: 7,500 /uL, Platelets: 2.5 Lakhs', 'Hb: 13-17 g/dL, WBC: 4000-11000', 'Completed'),
        ('LAB-702', 'P1025', 'Anita Verma', 'DOC-102', 'Dr. Rajesh Kumar', 'MRI Brain (Plain & Contrast)', '2026-09-06', 'Imaging', 'Pending radiologist impression', 'N/A', 'Processing'),
        ('LAB-703', 'P1026', 'Suresh Gupta', 'DOC-104', 'Dr. Vikram Malhotra', 'Serum Electrolytes & Creatinine', '2026-09-06', 'Blood', 'Sodium: 138 mEq/L, Creatinine: 0.9 mg/dL', 'Sodium: 135-145, Creatinine: 0.7-1.2', 'Completed'),
        ('LAB-704', 'P1027', 'Meena Kumari', 'DOC-103', 'Dr. Sunita Patel', 'Dengue NS1 Antigen Test', '2026-09-06', 'Blood', 'Sample collected', 'Negative', 'Pending')
    ]
    cursor.executemany("INSERT INTO laboratory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", lab_data)

    # Seed Bills
    bills_data = [
        ('INV-9001', 'P1024', 'Rahul Sharma', 500.0, 1200.0, 0.0, 0.0, 800.0, 350.0, 150.0, 3000.0, 300.0, 486.0, 3186.0, 'Paid', 'UPI', '2026-09-05'),
        ('INV-9002', 'P1026', 'Suresh Gupta', 2500.0, 2200.0, 12000.0, 4000.0, 3500.0, 1850.0, 950.0, 27000.0, 2000.0, 4500.0, 29500.0, 'Partially Paid', 'Card', '2026-09-06'),
        ('INV-9003', 'P1025', 'Anita Verma', 3000.0, 3000.0, 25000.0, 10000.0, 6500.0, 3200.0, 1500.0, 52200.0, 0.0, 9396.0, 61596.0, 'Pending', 'Net Banking', '2026-09-06')
    ]
    cursor.executemany("INSERT INTO bills VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", bills_data)

    # Seed Emergencies
    emergencies_data = [
        ('EMG-101', 'Vikash Singh', 'P1028', '2026-09-06 07:45 AM', 'Critical', 'Acute Thoracic Chest Pain & Breathlessness', 'DOC-106', 'Dr. Arvind Swamy', 'ER-BED-01', 'Under Treatment'),
        ('EMG-102', 'Rohan Mehta', None, '2026-09-06 08:30 AM', 'Urgent', 'Fracture Right Femur post Bike Slip', 'DOC-104', 'Dr. Vikram Malhotra', 'ER-BED-03', 'Active'),
        ('EMG-103', 'Sneha Kapoor', None, '2026-09-06 09:10 AM', 'Moderate', 'High Fever (103°F) with Dehydration', 'DOC-103', 'Dr. Sunita Patel', 'ER-BED-04', 'Stabilized')
    ]
    cursor.executemany("INSERT INTO emergencies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", emergencies_data)

    # Seed Medical History for Rahul Sharma (P1024) matching exact user prompt timeline!
    history_data = [
        ('P1024', '12 Aug 2026', 'Fever', 'Medication', 'Patient presented with fever. Prescribed antipyretics and rest.', 'Dr. Ananya Rao'),
        ('P1024', '27 Aug 2026', 'Infection', 'Antibiotics', 'Throat infection with cough. Prescribed antibiotic course.', 'Dr. Ananya Rao'),
        ('P1024', '05 Sep 2026', 'Follow-up', 'Observation', 'Blood pressure normal. Continue lifestyle modifications.', 'Dr. Ananya Rao'),
        ('P1025', '15 Aug 2026', 'Migraine Episode', 'Analgesics', 'Severe left-sided headache.', 'Dr. Rajesh Kumar'),
        ('P1026', '20 Aug 2026', 'Knee Joint Stiffness', 'Physiotherapy', 'Joint stiffness reported.', 'Dr. Vikram Malhotra')
    ]
    cursor.executemany("INSERT INTO medical_history (patient_id, record_date, diagnosis, treatment, doctor_notes, doctor_name) VALUES (?, ?, ?, ?, ?, ?)", history_data)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    init_db()
    seed_data()
