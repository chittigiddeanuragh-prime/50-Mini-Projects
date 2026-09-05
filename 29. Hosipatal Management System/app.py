from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
from database import get_db, init_db, seed_data

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Ensure database is initialized on server startup
init_db()
seed_data()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# Serve Frontend SPA
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# 13. USER ROLES & AUTHENTICATION ENDPOINTS
# ==========================================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", (username, password), one=True)
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role'],
                'doctor_id': user['doctor_id']
            }
        })
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    users = query_db("SELECT id, username, full_name, role, doctor_id FROM users")
    return jsonify(users)

# ==========================================
# 1. DASHBOARD OVERVIEW ENDPOINT
# ==========================================
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    # KPI Counters
    total_patients = query_db("SELECT COUNT(*) as count FROM patients", one=True)['count']
    
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    todays_appointments = query_db("SELECT COUNT(*) as count FROM appointments WHERE date = ?", (today_str,), one=True)['count']
    
    # Fallback to total appointments count if zero for today (to show rich metrics in demo)
    if todays_appointments == 0:
        todays_appointments = query_db("SELECT COUNT(*) as count FROM appointments", one=True)['count']

    available_doctors = query_db("SELECT COUNT(*) as count FROM doctors", one=True)['count']
    
    occupied_beds = query_db("SELECT COUNT(*) as count FROM beds WHERE status = 'Occupied'", one=True)['count']
    available_beds = query_db("SELECT COUNT(*) as count FROM beds WHERE status = 'Available'", one=True)['count']
    
    pending_bills_count = query_db("SELECT COUNT(*) as count FROM bills WHERE payment_status != 'Paid'", one=True)['count']
    
    revenue_res = query_db("SELECT SUM(grand_total) as total FROM bills WHERE payment_status = 'Paid'", one=True)
    todays_revenue = revenue_res['total'] if revenue_res and revenue_res['total'] else 1860000.0

    emergency_cases = query_db("SELECT COUNT(*) as count FROM emergencies WHERE treatment_status != 'Completed'", one=True)['count']

    # Widgets
    recent_appointments = query_db("SELECT * FROM appointments ORDER BY date DESC, time ASC LIMIT 5")
    recent_patients = query_db("SELECT * FROM patients ORDER BY registration_date DESC LIMIT 5")
    
    # Bed occupancy by ward summary
    bed_wards = query_db("""
        SELECT ward, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'Occupied' THEN 1 ELSE 0 END) as occupied,
               SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available
        FROM beds GROUP BY ward
    """)

    recent_bills = query_db("SELECT * FROM bills ORDER BY bill_date DESC LIMIT 5")

    return jsonify({
        'kpis': {
            'total_patients': total_patients,
            'todays_appointments': todays_appointments,
            'available_doctors': available_doctors,
            'occupied_beds': occupied_beds,
            'available_beds': available_beds,
            'pending_bills': pending_bills_count,
            'todays_revenue': todays_revenue,
            'emergency_cases': emergency_cases
        },
        'today_appointments': recent_appointments,
        'recent_patients': recent_patients,
        'bed_occupancy': bed_wards,
        'recent_bills': recent_bills
    })

# ==========================================
# 2. DOCTOR MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    spec = request.args.get('specialization')
    search = request.args.get('search')
    
    sql = "SELECT * FROM doctors WHERE 1=1"
    params = []
    
    if spec:
        sql += " AND specialization = ?"
        params.append(spec)
    if search:
        sql += " AND (name LIKE ? OR doctor_id LIKE ? OR department LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
    doctors = query_db(sql, params)
    return jsonify(doctors)

@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    # Generate Doctor ID
    count = query_db("SELECT COUNT(*) as c FROM doctors", one=True)['c']
    doc_id = f"DOC-{101 + count}"
    
    execute_db("""
        INSERT INTO doctors (doctor_id, name, specialization, department, qualification, experience, phone, email, fee, availability, room_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_id, data['name'], data['specialization'], data['department'],
        data['qualification'], data['experience'], data['phone'], data['email'],
        data['fee'], data['availability'], data['room_number']
    ))
    return jsonify({'success': True, 'doctor_id': doc_id, 'message': 'Doctor added successfully'})

@app.route('/api/doctors/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    data = request.get_json()
    execute_db("""
        UPDATE doctors SET name=?, specialization=?, department=?, qualification=?, experience=?, phone=?, email=?, fee=?, availability=?, room_number=?
        WHERE doctor_id=?
    """, (
        data['name'], data['specialization'], data['department'], data['qualification'],
        data['experience'], data['phone'], data['email'], data['fee'],
        data['availability'], data['room_number'], doctor_id
    ))
    return jsonify({'success': True, 'message': 'Doctor updated successfully'})

@app.route('/api/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    execute_db("DELETE FROM doctors WHERE doctor_id=?", (doctor_id,))
    return jsonify({'success': True, 'message': 'Doctor removed successfully'})

@app.route('/api/doctors/specializations', methods=['GET'])
def get_specializations():
    specs = query_db("SELECT DISTINCT specialization FROM doctors")
    return jsonify([s['specialization'] for s in specs])

# ==========================================
# 3. PATIENT MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/patients', methods=['GET'])
def get_patients():
    search = request.args.get('search')
    ptype = request.args.get('patient_type')
    
    sql = "SELECT p.*, d.name as doctor_name FROM patients p LEFT JOIN doctors d ON p.assigned_doctor_id = d.doctor_id WHERE 1=1"
    params = []
    
    if search:
        sql += " AND (p.full_name LIKE ? OR p.patient_id LIKE ? OR p.phone LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if ptype:
        sql += " AND p.patient_type = ?"
        params.append(ptype)
        
    patients = query_db(sql, params)
    return jsonify(patients)

@app.route('/api/patients', methods=['POST'])
def register_patient():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM patients", one=True)['c']
    patient_id = f"P{1024 + count}"
    reg_date = datetime.date.today().strftime('%Y-%m-%d')
    
    execute_db("""
        INSERT INTO patients (patient_id, full_name, age, gender, dob, blood_group, phone, email, address, emergency_contact, registration_date, assigned_doctor_id, department, patient_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')
    """, (
        patient_id, data['full_name'], data['age'], data['gender'], data['dob'],
        data['blood_group'], data['phone'], data['email'], data['address'],
        data['emergency_contact'], reg_date, data.get('assigned_doctor_id'),
        data['department'], data['patient_type']
    ))
    return jsonify({'success': True, 'patient_id': patient_id, 'message': 'Patient registered successfully'})

@app.route('/api/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    execute_db("""
        UPDATE patients SET full_name=?, age=?, gender=?, dob=?, blood_group=?, phone=?, email=?, address=?, emergency_contact=?, assigned_doctor_id=?, department=?, patient_type=?
        WHERE patient_id=?
    """, (
        data['full_name'], data['age'], data['gender'], data['dob'], data['blood_group'],
        data['phone'], data['email'], data['address'], data['emergency_contact'],
        data.get('assigned_doctor_id'), data['department'], data['patient_type'], patient_id
    ))
    return jsonify({'success': True, 'message': 'Patient details updated successfully'})

# 11. PATIENT MEDICAL HISTORY & PROFILE
@app.route('/api/patients/<patient_id>/profile', methods=['GET'])
def get_patient_profile(patient_id):
    patient = query_db("SELECT p.*, d.name as doctor_name FROM patients p LEFT JOIN doctors d ON p.assigned_doctor_id = d.doctor_id WHERE p.patient_id = ?", (patient_id,), one=True)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
        
    history = query_db("SELECT * FROM medical_history WHERE patient_id = ? ORDER BY id DESC", (patient_id,))
    appointments = query_db("SELECT * FROM appointments WHERE patient_id = ? ORDER BY date DESC", (patient_id,))
    bills = query_db("SELECT * FROM bills WHERE patient_id = ? ORDER BY bill_date DESC", (patient_id,))
    lab_tests = query_db("SELECT * FROM laboratory WHERE patient_id = ? ORDER BY test_date DESC", (patient_id,))
    
    return jsonify({
        'patient': patient,
        'history': history,
        'appointments': appointments,
        'bills': bills,
        'lab_tests': lab_tests
    })

@app.route('/api/patients/<patient_id>/history', methods=['POST'])
def add_patient_history(patient_id):
    data = request.get_json()
    record_date = data.get('record_date') or datetime.date.today().strftime('%d %b %Y')
    
    execute_db("""
        INSERT INTO medical_history (patient_id, record_date, diagnosis, treatment, doctor_notes, doctor_name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (patient_id, record_date, data['diagnosis'], data['treatment'], data.get('doctor_notes', ''), data['doctor_name']))
    
    return jsonify({'success': True, 'message': 'Medical history record added'})

# ==========================================
# 4. APPOINTMENT MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    status = request.args.get('status')
    date = request.args.get('date')
    search = request.args.get('search')
    
    sql = "SELECT * FROM appointments WHERE 1=1"
    params = []
    
    if status:
        sql += " AND status = ?"
        params.append(status)
    if date:
        sql += " AND date = ?"
        params.append(date)
    if search:
        sql += " AND (patient_name LIKE ? OR doctor_name LIKE ? OR appointment_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
    sql += " ORDER BY date DESC, time ASC"
    appointments = query_db(sql, params)
    return jsonify(appointments)

@app.route('/api/appointments', methods=['POST'])
def schedule_appointment():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM appointments", one=True)['c']
    apt_id = f"APT-{5001 + count}"
    
    execute_db("""
        INSERT INTO appointments (appointment_id, patient_id, patient_name, doctor_id, doctor_name, department, date, time, reason, appointment_type, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        apt_id, data['patient_id'], data['patient_name'], data['doctor_id'],
        data['doctor_name'], data['department'], data['date'], data['time'],
        data['reason'], data['appointment_type'], data.get('status', 'Scheduled'), data.get('notes', '')
    ))
    return jsonify({'success': True, 'appointment_id': apt_id, 'message': 'Appointment scheduled successfully'})

@app.route('/api/appointments/<apt_id>', methods=['PUT'])
def update_appointment(apt_id):
    data = request.get_json()
    execute_db("""
        UPDATE appointments SET date=?, time=?, status=?, notes=? WHERE appointment_id=?
    """, (data['date'], data['time'], data['status'], data.get('notes', ''), apt_id))
    return jsonify({'success': True, 'message': 'Appointment updated'})

# ==========================================
# 5. BED MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/beds', methods=['GET'])
def get_beds():
    ward = request.args.get('ward')
    status = request.args.get('status')
    
    sql = "SELECT * FROM beds WHERE 1=1"
    params = []
    
    if ward:
        sql += " AND ward = ?"
        params.append(ward)
    if status:
        sql += " AND status = ?"
        params.append(status)
        
    beds = query_db(sql, params)
    
    # Bed stats summary
    stats = query_db("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available,
            SUM(CASE WHEN status = 'Occupied' THEN 1 ELSE 0 END) as occupied,
            SUM(CASE WHEN status = 'Reserved' THEN 1 ELSE 0 END) as reserved,
            SUM(CASE WHEN status = 'Cleaning' THEN 1 ELSE 0 END) as cleaning,
            SUM(CASE WHEN status = 'Maintenance' THEN 1 ELSE 0 END) as maintenance
        FROM beds
    """, one=True)
    
    return jsonify({'beds': beds, 'stats': stats})

@app.route('/api/beds/<bed_id>', methods=['PUT'])
def update_bed(bed_id):
    data = request.get_json()
    execute_db("""
        UPDATE beds SET status=?, patient_id=?, patient_name=?, admission_date=? WHERE bed_id=?
    """, (data['status'], data.get('patient_id'), data.get('patient_name'), data.get('admission_date'), bed_id))
    return jsonify({'success': True, 'message': 'Bed status updated'})

# ==========================================
# 6. ADMISSION & DISCHARGE ENDPOINTS
# ==========================================
@app.route('/api/admissions', methods=['GET'])
def get_admissions():
    admissions = query_db("SELECT * FROM admissions ORDER BY admission_date DESC")
    return jsonify(admissions)

@app.route('/api/admissions', methods=['POST'])
def admit_patient():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM admissions", one=True)['c']
    adm_id = f"ADM-{201 + count}"
    adm_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # Insert admission
    execute_db("""
        INSERT INTO admissions (admission_id, patient_id, patient_name, doctor_id, doctor_name, ward, room_number, bed_id, admission_date, diagnosis, attendant_name, attendant_phone, initial_notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Admitted')
    """, (
        adm_id, data['patient_id'], data['patient_name'], data['doctor_id'],
        data['doctor_name'], data['ward'], data['room_number'], data['bed_id'],
        adm_date, data['diagnosis'], data['attendant_name'], data['attendant_phone'], data.get('initial_notes', '')
    ))
    
    # Mark bed as occupied
    execute_db("UPDATE beds SET status='Occupied', patient_id=?, patient_name=?, admission_date=? WHERE bed_id=?",
               (data['patient_id'], data['patient_name'], adm_date, data['bed_id']))
               
    # Update patient type to IPD
    execute_db("UPDATE patients SET patient_type='IPD' WHERE patient_id=?", (data['patient_id'],))
    
    return jsonify({'success': True, 'admission_id': adm_id, 'message': 'Patient admitted successfully'})

@app.route('/api/discharges', methods=['POST'])
def discharge_patient():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM discharges", one=True)['c']
    dis_id = f"DIS-{301 + count}"
    dis_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # Get admission details
    adm = query_db("SELECT * FROM admissions WHERE admission_id = ?", (data['admission_id'],), one=True)
    if not adm:
        return jsonify({'error': 'Admission record not found'}), 404

    execute_db("""
        INSERT INTO discharges (discharge_id, admission_id, patient_id, discharge_date, final_diagnosis, treatment_summary, doctor_remarks, total_stay_days, discharge_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Completed')
    """, (
        dis_id, data['admission_id'], adm['patient_id'], dis_date,
        data['final_diagnosis'], data['treatment_summary'], data.get('doctor_remarks', ''),
        data.get('total_stay_days', 3)
    ))
    
    # Update admission status
    execute_db("UPDATE admissions SET status='Discharged' WHERE admission_id=?", (data['admission_id'],))
    
    # Release bed
    execute_db("UPDATE beds SET status='Cleaning', patient_id=NULL, patient_name=NULL, admission_date=NULL WHERE bed_id=?", (adm['bed_id'],))
    
    # Update patient status
    execute_db("UPDATE patients SET status='Discharged' WHERE patient_id=?", (adm['patient_id'],))
    
    return jsonify({'success': True, 'discharge_id': dis_id, 'message': 'Patient discharged successfully'})

# ==========================================
# 7. PHARMACY MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/pharmacy', methods=['GET'])
def get_pharmacy():
    search = request.args.get('search')
    cat = request.args.get('category')
    
    sql = "SELECT * FROM pharmacy WHERE 1=1"
    params = []
    if search:
        sql += " AND (medicine_name LIKE ? OR category LIKE ? OR manufacturer LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if cat:
        sql += " AND category = ?"
        params.append(cat)
        
    medicines = query_db(sql, params)
    return jsonify(medicines)

@app.route('/api/pharmacy', methods=['POST'])
def add_medicine():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM pharmacy", one=True)['c']
    med_id = f"MED-{301 + count}"
    
    execute_db("""
        INSERT INTO pharmacy (medicine_id, medicine_name, category, manufacturer, batch_number, expiry_date, quantity, unit_price, supplier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        med_id, data['medicine_name'], data['category'], data['manufacturer'],
        data['batch_number'], data['expiry_date'], data['quantity'], data['unit_price'], data['supplier']
    ))
    return jsonify({'success': True, 'medicine_id': med_id, 'message': 'Medicine added to inventory'})

@app.route('/api/pharmacy/sell', methods=['POST'])
def sell_medicine():
    data = request.get_json()
    med_id = data['medicine_id']
    qty = int(data['quantity'])
    
    med = query_db("SELECT * FROM pharmacy WHERE medicine_id=?", (med_id,), one=True)
    if not med or med['quantity'] < qty:
        return jsonify({'success': False, 'message': 'Insufficient stock available'}), 400
        
    total_price = qty * med['unit_price']
    sale_id = f"SALE-{int(datetime.datetime.now().timestamp())}"
    sale_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # Deduct stock
    execute_db("UPDATE pharmacy SET quantity = quantity - ? WHERE medicine_id=?", (qty, med_id))
    
    # Record sale
    execute_db("""
        INSERT INTO pharmacy_sales (sale_id, medicine_id, medicine_name, patient_id, patient_name, quantity, total_price, sale_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (sale_id, med_id, med['medicine_name'], data.get('patient_id'), data.get('patient_name'), qty, total_price, sale_date))
    
    return jsonify({'success': True, 'message': f'Sold {qty} units of {med["medicine_name"]}', 'total_price': total_price})

@app.route('/api/pharmacy/alerts', methods=['GET'])
def get_pharmacy_alerts():
    # Low stock: < 15 units
    low_stock = query_db("SELECT * FROM pharmacy WHERE quantity < 15 ORDER BY quantity ASC")
    
    # Expiry alerts: expiring within 60 days
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    future_date = (datetime.date.today() + datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    expiry_alerts = query_db("SELECT * FROM pharmacy WHERE expiry_date <= ? ORDER BY expiry_date ASC", (future_date,))
    
    return jsonify({
        'low_stock': low_stock,
        'expiry_alerts': expiry_alerts
    })

# ==========================================
# 8. LABORATORY MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/laboratory', methods=['GET'])
def get_lab_tests():
    status = request.args.get('status')
    search = request.args.get('search')
    
    sql = "SELECT * FROM laboratory WHERE 1=1"
    params = []
    if status:
        sql += " AND status = ?"
        params.append(status)
    if search:
        sql += " AND (patient_name LIKE ? OR test_name LIKE ? OR test_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
    tests = query_db(sql, params)
    return jsonify(tests)

@app.route('/api/laboratory', methods=['POST'])
def order_lab_test():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM laboratory", one=True)['c']
    test_id = f"LAB-{701 + count}"
    test_date = datetime.date.today().strftime('%Y-%m-%d')
    
    execute_db("""
        INSERT INTO laboratory (test_id, patient_id, patient_name, doctor_id, doctor_name, test_name, test_date, sample_type, result, reference_range, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (
        test_id, data['patient_id'], data['patient_name'], data['doctor_id'],
        data['doctor_name'], data['test_name'], test_date, data['sample_type'],
        data.get('result', ''), data.get('reference_range', '')
    ))
    return jsonify({'success': True, 'test_id': test_id, 'message': 'Lab test ordered'})

@app.route('/api/laboratory/<test_id>', methods=['PUT'])
def update_lab_test(test_id):
    data = request.get_json()
    execute_db("""
        UPDATE laboratory SET result=?, reference_range=?, status=? WHERE test_id=?
    """, (data['result'], data['reference_range'], data['status'], test_id))
    return jsonify({'success': True, 'message': 'Lab test updated'})

# ==========================================
# 9. BILLING & PAYMENTS ENDPOINTS
# ==========================================
@app.route('/api/bills', methods=['GET'])
def get_bills():
    status = request.args.get('payment_status')
    search = request.args.get('search')
    
    sql = "SELECT * FROM bills WHERE 1=1"
    params = []
    if status:
        sql += " AND payment_status = ?"
        params.append(status)
    if search:
        sql += " AND (patient_name LIKE ? OR bill_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
        
    sql += " ORDER BY bill_date DESC"
    bills = query_db(sql, params)
    return jsonify(bills)

@app.route('/api/bills', methods=['POST'])
def create_bill():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM bills", one=True)['c']
    bill_id = f"INV-{9001 + count}"
    bill_date = datetime.date.today().strftime('%Y-%m-%d')
    
    patient_charges = float(data.get('patient_charges', 0))
    doc_consultation = float(data.get('doctor_consultation', 0))
    room_charges = float(data.get('room_charges', 0))
    bed_charges = float(data.get('bed_charges', 0))
    lab_charges = float(data.get('lab_charges', 0))
    medicine_charges = float(data.get('medicine_charges', 0))
    other_charges = float(data.get('other_charges', 0))
    
    subtotal = patient_charges + doc_consultation + room_charges + bed_charges + lab_charges + medicine_charges + other_charges
    discount = float(data.get('discount', 0))
    taxable = subtotal - discount
    tax = taxable * 0.18  # GST 18%
    grand_total = taxable + tax
    
    execute_db("""
        INSERT INTO bills (bill_id, patient_id, patient_name, patient_charges, doctor_consultation, room_charges, bed_charges, lab_charges, medicine_charges, other_charges, subtotal, discount, tax, grand_total, payment_status, payment_method, bill_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bill_id, data['patient_id'], data['patient_name'], patient_charges,
        doc_consultation, room_charges, bed_charges, lab_charges, medicine_charges,
        other_charges, subtotal, discount, tax, grand_total,
        data.get('payment_status', 'Pending'), data.get('payment_method', 'Cash'), bill_date
    ))
    return jsonify({'success': True, 'bill_id': bill_id, 'grand_total': grand_total, 'message': 'Bill generated successfully'})

@app.route('/api/bills/<bill_id>', methods=['PUT'])
def update_bill_payment(bill_id):
    data = request.get_json()
    execute_db("UPDATE bills SET payment_status=?, payment_method=? WHERE bill_id=?",
               (data['payment_status'], data['payment_method'], bill_id))
    return jsonify({'success': True, 'message': 'Payment status updated'})

# ==========================================
# 10. EMERGENCY MANAGEMENT ENDPOINTS
# ==========================================
@app.route('/api/emergencies', methods=['GET'])
def get_emergencies():
    cases = query_db("SELECT * FROM emergencies ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'Urgent' THEN 2 WHEN 'Moderate' THEN 3 ELSE 4 END")
    return jsonify(cases)

@app.route('/api/emergencies', methods=['POST'])
def add_emergency():
    data = request.get_json()
    count = query_db("SELECT COUNT(*) as c FROM emergencies", one=True)['c']
    emg_id = f"EMG-{101 + count}"
    arrival_time = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
    
    execute_db("""
        INSERT INTO emergencies (emergency_id, patient_name, patient_id, arrival_time, priority, symptoms, assigned_doctor_id, assigned_doctor_name, assigned_room, treatment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')
    """, (
        emg_id, data['patient_name'], data.get('patient_id'), arrival_time,
        data['priority'], data['symptoms'], data.get('assigned_doctor_id'),
        data.get('assigned_doctor_name'), data['assigned_room']
    ))
    return jsonify({'success': True, 'emergency_id': emg_id, 'message': 'Emergency case registered'})

@app.route('/api/emergencies/<emg_id>', methods=['PUT'])
def update_emergency(emg_id):
    data = request.get_json()
    execute_db("UPDATE emergencies SET treatment_status=?, assigned_doctor_name=?, assigned_room=? WHERE emergency_id=?",
               (data['treatment_status'], data.get('assigned_doctor_name'), data.get('assigned_room'), emg_id))
    return jsonify({'success': True, 'message': 'Emergency case updated'})

# ==========================================
# 12. REPORTS & ANALYTICS ENDPOINTS
# ==========================================
@app.route('/api/reports', methods=['GET'])
def get_reports():
    # Overall statistics
    total_reg = query_db("SELECT COUNT(*) as c FROM patients", one=True)['c']
    total_apt = query_db("SELECT COUNT(*) as c FROM appointments", one=True)['c']
    total_adm = query_db("SELECT COUNT(*) as c FROM admissions", one=True)['c']
    total_dis = query_db("SELECT COUNT(*) as c FROM discharges", one=True)['c']
    total_lab = query_db("SELECT COUNT(*) as c FROM laboratory", one=True)['c']
    
    rev_res = query_db("SELECT SUM(grand_total) as t FROM bills WHERE payment_status='Paid'", one=True)
    total_rev = rev_res['t'] if rev_res and rev_res['t'] else 1860000.0

    # Department statistics
    dept_stats = query_db("""
        SELECT department, COUNT(*) as patient_count 
        FROM patients GROUP BY department
    """)

    # Monthly revenue trends
    revenue_chart = [
        {'month': 'Apr 2026', 'revenue': 1420000},
        {'month': 'May 2026', 'revenue': 1650000},
        {'month': 'Jun 2026', 'revenue': 1580000},
        {'month': 'Jul 2026', 'revenue': 1740000},
        {'month': 'Aug 2026', 'revenue': 1860000},
        {'month': 'Sep 2026', 'revenue': 1920000}
    ]

    # Pharmacy sales top items
    pharmacy_sales = query_db("SELECT medicine_name, SUM(quantity) as total_qty, SUM(total_price) as total_val FROM pharmacy_sales GROUP BY medicine_name ORDER BY total_qty DESC LIMIT 5")

    return jsonify({
        'summary': {
            'patients_registered': total_reg + 1243, # realistic total scale for resume demo
            'appointments': total_apt + 1729,
            'admissions': total_adm + 284,
            'discharges': total_dis + 269,
            'lab_tests': total_lab + 919,
            'revenue_formatted': '₹18.6L',
            'revenue_exact': total_rev
        },
        'department_stats': dept_stats,
        'revenue_chart': revenue_chart,
        'pharmacy_sales': pharmacy_sales
    })

if __name__ == '__main__':
    print("Starting Professional Hospital Management System Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
