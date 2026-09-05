// Application JavaScript for Hospital Management System

let currentRole = 'ADMIN';
let doctorsList = [];
let patientsList = [];
let bedsList = [];
let pharmacyList = [];

// ==========================================
// INITIALIZATION & ROUTING
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    switchView('dashboard');
    loadDropdownOptions();
    checkPharmacyAlerts();
});

function switchView(viewId) {
    // Hide all view sections
    const views = ['dashboard', 'doctors', 'patients', 'appointments', 'beds', 'admissions', 'pharmacy', 'laboratory', 'billing', 'emergency', 'history', 'reports', 'roles'];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        const nav = document.getElementById(`nav-${v}`);
        if (el) el.classList.add('hidden');
        if (nav) {
            nav.classList.remove('bg-sky-600', 'text-white', 'active');
            nav.classList.add('hover:bg-slate-800', 'hover:text-white');
        }
    });

    // Show target view
    const targetEl = document.getElementById(`view-${viewId}`);
    const targetNav = document.getElementById(`nav-${viewId}`);
    if (targetEl) targetEl.classList.remove('hidden');
    if (targetNav) {
        targetNav.classList.add('bg-sky-600', 'text-white', 'active');
        targetNav.classList.remove('hover:bg-slate-800', 'hover:text-white');
    }

    // Update Header Title
    const titleMap = {
        'dashboard': '🏥 Dashboard Overview',
        'doctors': '👨‍⚕️ Doctor Management',
        'patients': '🧑‍🤝‍🧑 Patient Management',
        'appointments': '📅 Appointment Management',
        'beds': '🛏️ Bed Occupancy & Management',
        'admissions': '🏨 IPD Admission & Discharge',
        'pharmacy': '💊 Pharmacy Inventory & Sales',
        'laboratory': '🧪 Laboratory Diagnostics',
        'billing': '💰 Billing & Payments',
        'emergency': '🚑 Emergency Response',
        'history': '📋 Patient Medical History Timeline',
        'reports': '📊 Hospital Reports & Analytics',
        'roles': '🔐 User Security & RBAC'
    };
    document.getElementById('view-title').innerText = titleMap[viewId] || 'Hospital Management';

    // Load view data
    if (viewId === 'dashboard') loadDashboard();
    else if (viewId === 'doctors') loadDoctors();
    else if (viewId === 'patients') loadPatients();
    else if (viewId === 'appointments') loadAppointments();
    else if (viewId === 'beds') loadBeds();
    else if (viewId === 'admissions') loadAdmissions();
    else if (viewId === 'pharmacy') loadPharmacy();
    else if (viewId === 'laboratory') loadLabTests();
    else if (viewId === 'billing') loadBills();
    else if (viewId === 'emergency') loadEmergencies();
    else if (viewId === 'history') loadHistoryPatients();
    else if (viewId === 'reports') loadReports();
}

// ==========================================
// ROLE BASED ACCESS CONTROL (RBAC)
// ==========================================
function changeActiveRole(role) {
    currentRole = role;
    document.getElementById('role-badge').innerText = role;
    
    const roleColors = {
        'ADMIN': 'bg-sky-500/20 text-sky-400 border-sky-500/30',
        'DOCTOR': 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
        'RECEPTIONIST': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
        'PHARMACIST': 'bg-rose-500/20 text-rose-400 border-rose-500/30'
    };
    document.getElementById('role-badge').className = `px-2 py-0.5 rounded text-xs font-bold border ${roleColors[role] || ''}`;
    
    // Update User Name in header
    const names = {
        'ADMIN': { name: 'System Administrator', avatar: 'AD', sub: 'System Superuser' },
        'DOCTOR': { name: 'Dr. Ananya Rao', avatar: 'AR', sub: 'Senior Cardiologist' },
        'RECEPTIONIST': { name: 'Priya Sharma', avatar: 'PS', sub: 'Head Receptionist' },
        'PHARMACIST': { name: 'Ramesh Patel', avatar: 'RP', sub: 'Lead Pharmacist' }
    };
    const info = names[role] || names['ADMIN'];
    document.getElementById('user-name').innerText = info.name;
    document.getElementById('user-avatar').innerText = info.avatar;
    document.getElementById('user-role-sub').innerText = info.sub;

    alert(`Role switched to ${role}. Navigating to role dashboard.`);
    switchView('dashboard');
}

// ==========================================
// 1. DASHBOARD LOAD
// ==========================================
async function loadDashboard() {
    try {
        const res = await fetch('/api/dashboard');
        const data = await res.json();

        // Update KPIs
        document.getElementById('kpi-patients').innerText = data.kpis.total_patients;
        document.getElementById('kpi-appointments').innerText = data.kpis.todays_appointments;
        document.getElementById('kpi-doctors').innerText = data.kpis.available_doctors;
        document.getElementById('kpi-occupied-beds').innerText = `${data.kpis.occupied_beds} / 100`;
        document.getElementById('kpi-available-beds').innerText = data.kpis.available_beds;
        document.getElementById('kpi-pending-bills').innerText = data.kpis.pending_bills;
        document.getElementById('kpi-revenue').innerText = `₹${(data.kpis.todays_revenue / 100000).toFixed(1)}L`;
        document.getElementById('kpi-emergencies').innerText = data.kpis.emergency_cases;

        // Render Today Appointments
        const aptBody = document.getElementById('dash-appointments-body');
        aptBody.innerHTML = data.today_appointments.map(a => `
            <tr class="hover:bg-slate-50">
                <td class="p-3 font-mono font-bold text-sky-600">${a.appointment_id}</td>
                <td class="p-3 font-semibold text-slate-800">${a.patient_name}</td>
                <td class="p-3 text-slate-600">${a.doctor_name}</td>
                <td class="p-3 font-medium text-slate-700">${a.time}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${getStatusClass(a.status)}">${a.status}</span></td>
            </tr>
        `).join('') || '<tr><td colspan="5" class="p-3 text-slate-400 text-center">No appointments today</td></tr>';

        // Render Bed Occupancy Overview Wards
        const bedWardsContainer = document.getElementById('dash-bed-wards');
        bedWardsContainer.innerHTML = data.bed_occupancy.map(b => {
            const pct = Math.round((b.occupied / b.total) * 100);
            return `
                <div>
                    <div class="flex justify-between text-xs font-semibold mb-1">
                        <span class="text-slate-700">${b.ward}</span>
                        <span class="text-slate-500">${b.occupied} / ${b.total} Beds (${pct}%)</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-2">
                        <div class="bg-sky-600 h-2 rounded-full" style="width: ${pct}%"></div>
                    </div>
                </div>
            `;
        }).join('');

        // Render Recent Patients
        const patBody = document.getElementById('dash-patients-body');
        patBody.innerHTML = data.recent_patients.map(p => `
            <tr class="hover:bg-slate-50">
                <td class="p-3 font-mono font-bold text-emerald-600">${p.patient_id}</td>
                <td class="p-3 font-semibold text-slate-800">${p.full_name}</td>
                <td class="p-3 text-slate-600">${p.gender}, ${p.age} yrs</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${p.patient_type}</span></td>
            </tr>
        `).join('');

        // Render Recent Bills
        const billBody = document.getElementById('dash-bills-body');
        billBody.innerHTML = data.recent_bills.map(b => `
            <tr class="hover:bg-slate-50">
                <td class="p-3 font-mono font-bold text-teal-600">${b.bill_id}</td>
                <td class="p-3 font-semibold text-slate-800">${b.patient_name}</td>
                <td class="p-3 font-bold text-slate-900">₹${b.grand_total.toLocaleString()}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${b.payment_status === 'Paid' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${b.payment_status}</span></td>
            </tr>
        `).join('');

    } catch (err) {
        console.error('Error loading dashboard:', err);
    }
}

// ==========================================
// 2. DOCTOR MANAGEMENT
// ==========================================
async function loadDoctors() {
    const search = document.getElementById('doctor-search')?.value || '';
    const spec = document.getElementById('doctor-spec-filter')?.value || '';

    const res = await fetch(`/api/doctors?search=${encodeURIComponent(search)}&specialization=${encodeURIComponent(spec)}`);
    doctorsList = await res.json();

    const grid = document.getElementById('doctors-grid');
    grid.innerHTML = doctorsList.map(d => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4 hover:shadow-md transition">
            <div class="flex items-start justify-between">
                <div>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-50 text-sky-600 border border-sky-100 font-mono">${d.doctor_id}</span>
                    <h3 class="font-bold text-slate-900 text-base mt-1">${d.name}</h3>
                    <p class="text-xs font-semibold text-sky-600">${d.specialization} (${d.department})</p>
                </div>
                <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-bold">
                    <i class="fa-solid fa-user-doctor"></i>
                </div>
            </div>
            <div class="text-xs text-slate-600 space-y-1.5 border-t border-b border-slate-100 py-3">
                <div><i class="fa-solid fa-graduation-cap text-slate-400 w-4"></i> ${d.qualification} (${d.experience} yrs exp)</div>
                <div><i class="fa-solid fa-phone text-slate-400 w-4"></i> ${d.phone}</div>
                <div><i class="fa-solid fa-door-open text-slate-400 w-4"></i> Room: <span class="font-bold text-slate-800">${d.room_number}</span></div>
                <div><i class="fa-solid fa-clock text-slate-400 w-4"></i> ${d.availability}</div>
            </div>
            <div class="flex items-center justify-between">
                <span class="text-sm font-extrabold text-slate-900">Fee: ₹${d.fee}</span>
                <div class="flex gap-1">
                    <button onclick="deleteDoctor('${d.doctor_id}')" class="px-2 py-1 text-xs bg-rose-50 text-rose-600 rounded hover:bg-rose-100 font-semibold"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
        </div>
    `).join('') || '<div class="col-span-3 text-center py-8 text-slate-400 text-xs">No doctors found matching filters.</div>';
}

async function handleDoctorSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const res = await fetch('/api/doctors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(data.message);
        closeModal('modal-doctor');
        e.target.reset();
        loadDoctors();
        loadDropdownOptions();
    }
}

async function deleteDoctor(id) {
    if (!confirm('Are you sure you want to remove this doctor?')) return;
    await fetch(`/api/doctors/${id}`, { method: 'DELETE' });
    loadDoctors();
}

// ==========================================
// 3. PATIENT MANAGEMENT
// ==========================================
async function loadPatients() {
    const search = document.getElementById('patient-search')?.value || '';
    const ptype = document.getElementById('patient-type-filter')?.value || '';

    const res = await fetch(`/api/patients?search=${encodeURIComponent(search)}&patient_type=${encodeURIComponent(ptype)}`);
    patientsList = await res.json();

    const tbody = document.getElementById('patients-table-body');
    tbody.innerHTML = patientsList.map(p => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-emerald-600">${p.patient_id}</td>
            <td class="p-3 font-bold text-slate-800">${p.full_name}</td>
            <td class="p-3 text-slate-600">${p.gender}, ${p.age} yrs</td>
            <td class="p-3"><span class="px-2 py-0.5 text-[10px] font-bold bg-rose-50 text-rose-600 rounded border border-rose-100">${p.blood_group}</span></td>
            <td class="p-3 text-slate-600">${p.phone}</td>
            <td class="p-3 text-slate-700 font-medium">${p.doctor_name || 'Unassigned'}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.patient_type === 'Emergency' ? 'bg-red-100 text-red-700' : p.patient_type === 'IPD' ? 'bg-sky-100 text-sky-700' : 'bg-slate-100 text-slate-700'}">${p.patient_type}</span></td>
            <td class="p-3 text-right">
                <button onclick="viewPatientProfile('${p.patient_id}')" class="px-2 py-1 bg-sky-600 text-white rounded text-[11px] font-bold hover:bg-sky-700">Profile & History</button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="8" class="p-4 text-center text-slate-400">No patients found.</td></tr>';
}

async function handlePatientSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const res = await fetch('/api/patients', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`Patient Registered! ID: ${data.patient_id}`);
        closeModal('modal-patient');
        e.target.reset();
        loadPatients();
        loadDropdownOptions();
    }
}

// ==========================================
// 4. APPOINTMENT MANAGEMENT
// ==========================================
async function loadAppointments() {
    const search = document.getElementById('apt-search')?.value || '';
    const status = document.getElementById('apt-status-filter')?.value || '';

    const res = await fetch(`/api/appointments?search=${encodeURIComponent(search)}&status=${encodeURIComponent(status)}`);
    const appointments = await res.json();

    const tbody = document.getElementById('appointments-table-body');
    tbody.innerHTML = appointments.map(a => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-indigo-600">${a.appointment_id}</td>
            <td class="p-3 font-bold text-slate-800">${a.patient_name} <span class="text-[10px] text-slate-400 font-normal">(${a.patient_id})</span></td>
            <td class="p-3 font-medium text-slate-700">${a.doctor_name} <span class="text-[10px] text-slate-400 block">${a.department}</span></td>
            <td class="p-3 text-slate-700">${a.date} at ${a.time}</td>
            <td class="p-3 text-slate-600">${a.reason}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${getStatusClass(a.status)}">${a.status}</span></td>
            <td class="p-3 text-right space-x-1">
                ${a.status !== 'Completed' ? `<button onclick="updateAppointmentStatus('${a.appointment_id}', 'Completed')" class="px-2 py-1 bg-emerald-600 text-white rounded text-[10px] font-bold hover:bg-emerald-700">Complete</button>` : ''}
                ${a.status !== 'Cancelled' && a.status !== 'Completed' ? `<button onclick="updateAppointmentStatus('${a.appointment_id}', 'Cancelled')" class="px-2 py-1 bg-rose-50 text-rose-600 rounded text-[10px] font-bold hover:bg-rose-100">Cancel</button>` : ''}
            </td>
        </tr>
    `).join('') || '<tr><td colspan="7" class="p-4 text-center text-slate-400">No appointments scheduled.</td></tr>';
}

async function handleAppointmentSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    // find patient & doctor names
    const pat = patientsList.find(p => p.patient_id === body.patient_id);
    const doc = doctorsList.find(d => d.doctor_id === body.doctor_id);

    body.patient_name = pat ? pat.full_name : 'Patient';
    body.doctor_name = doc ? doc.name : 'Doctor';
    body.department = doc ? doc.department : 'General';

    const res = await fetch('/api/appointments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`Appointment Scheduled! ID: ${data.appointment_id}`);
        closeModal('modal-appointment');
        e.target.reset();
        loadAppointments();
    }
}

async function updateAppointmentStatus(id, status) {
    await fetch(`/api/appointments/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: status, date: new Date().toISOString().split('T')[0], time: '10:00 AM' })
    });
    loadAppointments();
}

// ==========================================
// 5. BED MANAGEMENT
// ==========================================
async function loadBeds(wardFilter = '') {
    const res = await fetch(`/api/beds${wardFilter ? '?ward=' + encodeURIComponent(wardFilter) : ''}`);
    const data = await res.json();
    bedsList = data.beds;

    // Update KPI stats
    if (data.stats) {
        document.getElementById('bed-stat-available').innerText = data.stats.available;
        document.getElementById('bed-stat-occupied').innerText = data.stats.occupied;
        document.getElementById('bed-stat-reserved').innerText = data.stats.reserved;
        document.getElementById('bed-stat-maint').innerText = data.stats.cleaning + data.stats.maintenance;
    }

    const grid = document.getElementById('beds-grid');
    grid.innerHTML = bedsList.map(b => {
        let statusStyle = 'bed-available';
        if (b.status === 'Occupied') statusStyle = 'bed-occupied';
        else if (b.status === 'Reserved') statusStyle = 'bed-reserved';
        else if (b.status === 'Cleaning') statusStyle = 'bed-cleaning';
        else if (b.status === 'Maintenance') statusStyle = 'bed-maintenance';

        return `
            <div onclick="toggleBedStatus('${b.bed_id}', '${b.status}')" class="bed-card p-3 rounded-xl ${statusStyle} cursor-pointer flex flex-col justify-between text-left">
                <div class="flex items-center justify-between">
                    <span class="text-[10px] font-bold uppercase tracking-wider">${b.bed_id}</span>
                    <i class="fa-solid fa-bed text-xs"></i>
                </div>
                <div class="my-2">
                    <h5 class="font-bold text-xs leading-tight">${b.room_number}</h5>
                    <p class="text-[10px] opacity-80">${b.bed_type}</p>
                </div>
                <div class="text-[10px] font-extrabold flex items-center justify-between pt-1 border-t border-current/10">
                    <span>${b.status}</span>
                    ${b.patient_name ? `<span class="truncate max-w-[60px]" title="${b.patient_name}">${b.patient_name}</span>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function filterBeds(ward) {
    document.querySelectorAll('.bed-ward-btn').forEach(btn => {
        btn.classList.remove('bg-slate-800', 'text-white');
        btn.classList.add('bg-white', 'text-slate-700');
    });
    event.target.classList.add('bg-slate-800', 'text-white');
    event.target.classList.remove('bg-white', 'text-slate-700');
    loadBeds(ward);
}

async function toggleBedStatus(bedId, currentStatus) {
    const nextStatusMap = {
        'Available': 'Occupied',
        'Occupied': 'Cleaning',
        'Cleaning': 'Available',
        'Reserved': 'Available',
        'Maintenance': 'Available'
    };
    const nextStatus = nextStatusMap[currentStatus] || 'Available';

    await fetch(`/api/beds/${bedId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus })
    });
    loadBeds();
}

// ==========================================
// 6. ADMISSION & DISCHARGE
// ==========================================
async function loadAdmissions() {
    const res = await fetch('/api/admissions');
    const admissions = await res.json();

    const tbody = document.getElementById('admissions-table-body');
    tbody.innerHTML = admissions.map(a => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-teal-600">${a.admission_id}</td>
            <td class="p-3 font-bold text-slate-800">${a.patient_name}</td>
            <td class="p-3 font-medium text-slate-700">${a.doctor_name}</td>
            <td class="p-3 text-slate-600">${a.ward} / <span class="font-bold">${a.room_number}</span> (${a.bed_id})</td>
            <td class="p-3 text-slate-600">${a.admission_date}</td>
            <td class="p-3 text-slate-600">${a.diagnosis}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${a.status === 'Admitted' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'}">${a.status}</span></td>
            <td class="p-3 text-right">
                ${a.status === 'Admitted' ? `<button onclick="processDischarge('${a.admission_id}')" class="px-2 py-1 bg-rose-600 text-white rounded text-[11px] font-bold hover:bg-rose-700">Discharge Patient</button>` : ''}
            </td>
        </tr>
    `).join('') || '<tr><td colspan="8" class="p-4 text-center text-slate-400">No current admissions.</td></tr>';
}

async function handleAdmissionSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const pat = patientsList.find(p => p.patient_id === body.patient_id);
    const doc = doctorsList.find(d => d.doctor_id === body.doctor_id);
    const bed = bedsList.find(b => b.bed_id === body.bed_id);

    body.patient_name = pat ? pat.full_name : 'Patient';
    body.doctor_name = doc ? doc.name : 'Doctor';
    body.ward = bed ? bed.ward : 'General Ward';
    body.room_number = bed ? bed.room_number : '101';

    const res = await fetch('/api/admissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`Patient Admitted to ${body.ward} (${body.bed_id})!`);
        closeModal('modal-admission');
        e.target.reset();
        loadAdmissions();
        loadBeds();
    }
}

async function processDischarge(admId) {
    const summary = prompt('Enter Discharge Treatment Summary & Final Diagnosis:');
    if (!summary) return;

    const res = await fetch('/api/discharges', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            admission_id: admId,
            final_diagnosis: summary,
            treatment_summary: 'Medication and recovery complete',
            total_stay_days: 3
        })
    });
    const data = await res.json();
    if (data.success) {
        alert('Patient Discharged successfully! Bed sent for cleaning.');
        loadAdmissions();
        loadBeds();
    }
}

// ==========================================
// 7. PHARMACY MANAGEMENT
// ==========================================
async function loadPharmacy() {
    const search = document.getElementById('med-search')?.value || '';
    const res = await fetch(`/api/pharmacy?search=${encodeURIComponent(search)}`);
    pharmacyList = await res.json();

    const tbody = document.getElementById('pharmacy-table-body');
    tbody.innerHTML = pharmacyList.map(m => `
        <tr class="hover:bg-slate-50 ${m.quantity < 15 ? 'bg-amber-50/50' : ''}">
            <td class="p-3 font-mono font-bold text-rose-600">${m.medicine_id}</td>
            <td class="p-3 font-bold text-slate-800">${m.medicine_name}</td>
            <td class="p-3 text-slate-600">${m.category}</td>
            <td class="p-3 text-slate-600">${m.manufacturer}</td>
            <td class="p-3 text-slate-600">${m.expiry_date}</td>
            <td class="p-3"><span class="font-extrabold ${m.quantity < 15 ? 'text-amber-600' : 'text-slate-900'}">${m.quantity} units ${m.quantity < 15 ? '⚠ LOW' : ''}</span></td>
            <td class="p-3 font-bold text-slate-900">₹${m.unit_price}</td>
            <td class="p-3 text-right">
                <button onclick="quickSell('${m.medicine_id}')" class="px-2 py-1 bg-emerald-600 text-white rounded text-[10px] font-bold hover:bg-emerald-700">Sell</button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="8" class="p-4 text-center text-slate-400">No medicines in inventory.</td></tr>';
}

async function checkPharmacyAlerts() {
    const res = await fetch('/api/pharmacy/alerts');
    const data = await res.json();

    const alertList = document.getElementById('low-stock-list');
    if (alertList) {
        const lowItems = data.low_stock.map(m => `<span class="font-bold">${m.medicine_name}</span>: ${m.quantity} units left`).join(' | ');
        alertList.innerHTML = lowItems || 'All stock levels optimal.';
    }
}

async function handleMedicineSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const res = await fetch('/api/pharmacy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert('Medicine added to inventory!');
        closeModal('modal-medicine');
        e.target.reset();
        loadPharmacy();
        checkPharmacyAlerts();
    }
}

async function handleSellMedicineSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const res = await fetch('/api/pharmacy/sell', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`${data.message}. Total Amount: ₹${data.total_price}`);
        closeModal('modal-sell-medicine');
        e.target.reset();
        loadPharmacy();
        checkPharmacyAlerts();
    } else {
        alert(data.message);
    }
}

function quickSell(medId) {
    openModal('modal-sell-medicine');
    document.getElementById('pos-medicine-select').value = medId;
}

// ==========================================
// 8. LABORATORY MANAGEMENT
// ==========================================
async function loadLabTests() {
    const search = document.getElementById('lab-search')?.value || '';
    const res = await fetch(`/api/laboratory?search=${encodeURIComponent(search)}`);
    const tests = await res.json();

    const tbody = document.getElementById('lab-table-body');
    tbody.innerHTML = tests.map(t => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-purple-600">${t.test_id}</td>
            <td class="p-3 font-bold text-slate-800">${t.patient_name}</td>
            <td class="p-3 font-medium text-slate-700">${t.doctor_name}</td>
            <td class="p-3 font-semibold text-purple-900">${t.test_name}</td>
            <td class="p-3 text-slate-600">${t.sample_type}</td>
            <td class="p-3 text-xs text-slate-700 max-w-xs">${t.result || 'Pending Result'}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${t.status === 'Completed' ? 'bg-emerald-100 text-emerald-800' : 'bg-purple-100 text-purple-800'}">${t.status}</span></td>
            <td class="p-3 text-right">
                ${t.status !== 'Completed' ? `<button onclick="updateLabResult('${t.test_id}')" class="px-2 py-1 bg-purple-600 text-white rounded text-[10px] font-bold hover:bg-purple-700">Enter Result</button>` : ''}
            </td>
        </tr>
    `).join('') || '<tr><td colspan="8" class="p-4 text-center text-slate-400">No lab tests ordered.</td></tr>';
}

async function handleLabTestSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const pat = patientsList.find(p => p.patient_id === body.patient_id);
    const doc = doctorsList.find(d => d.doctor_id === body.doctor_id);

    body.patient_name = pat ? pat.full_name : 'Patient';
    body.doctor_name = doc ? doc.name : 'Doctor';

    const res = await fetch('/api/laboratory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert('Lab test ordered successfully!');
        closeModal('modal-lab-test');
        e.target.reset();
        loadLabTests();
    }
}

async function updateLabResult(testId) {
    const result = prompt('Enter Lab Test Results / Impression:');
    if (!result) return;

    await fetch(`/api/laboratory/${testId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ result: result, reference_range: 'Normal Range', status: 'Completed' })
    });
    loadLabTests();
}

// ==========================================
// 9. BILLING & PAYMENTS
// ==========================================
async function loadBills() {
    const search = document.getElementById('bill-search')?.value || '';
    const res = await fetch(`/api/bills?search=${encodeURIComponent(search)}`);
    const bills = await res.json();

    const tbody = document.getElementById('billing-table-body');
    tbody.innerHTML = bills.map(b => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-teal-600">${b.bill_id}</td>
            <td class="p-3 font-bold text-slate-800">${b.patient_name}</td>
            <td class="p-3 text-slate-600">${b.bill_date}</td>
            <td class="p-3 font-extrabold text-slate-900">₹${b.grand_total.toLocaleString()}</td>
            <td class="p-3 text-slate-700 font-medium">${b.payment_method}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${b.payment_status === 'Paid' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${b.payment_status}</span></td>
            <td class="p-3 text-right space-x-1">
                <button onclick="printInvoice('${b.bill_id}')" class="px-2 py-1 bg-slate-800 text-white rounded text-[10px] font-bold hover:bg-slate-900"><i class="fa-solid fa-print"></i> Print</button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="7" class="p-4 text-center text-slate-400">No billing records.</td></tr>';
}

async function handleBillSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const pat = patientsList.find(p => p.patient_id === body.patient_id);
    body.patient_name = pat ? pat.full_name : 'Patient';

    const res = await fetch('/api/bills', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`Invoice Generated! Total: ₹${data.grand_total}`);
        closeModal('modal-create-bill');
        e.target.reset();
        loadBills();
    }
}

async function printInvoice(billId) {
    const res = await fetch(`/api/bills?search=${encodeURIComponent(billId)}`);
    const bills = await res.json();
    const bill = bills.find(b => b.bill_id === billId);

    if (bill) {
        document.getElementById('inv-id').innerText = bill.bill_id;
        document.getElementById('inv-date').innerText = `Date: ${bill.bill_date}`;
        document.getElementById('inv-patient-name').innerText = bill.patient_name;
        document.getElementById('inv-patient-id').innerText = `ID: ${bill.patient_id}`;
        document.getElementById('inv-status').innerText = bill.payment_status.toUpperCase();
        document.getElementById('inv-method').innerText = bill.payment_method;

        document.getElementById('inv-items-body').innerHTML = `
            <tr><td class="py-1">Doctor Consultation Fee</td><td class="py-1 text-right">₹${bill.doctor_consultation.toLocaleString()}</td></tr>
            <tr><td class="py-1">Patient Charges</td><td class="py-1 text-right">₹${bill.patient_charges.toLocaleString()}</td></tr>
            <tr><td class="py-1">Room / Bed Charges</td><td class="py-1 text-right">₹${(bill.room_charges + bill.bed_charges).toLocaleString()}</td></tr>
            <tr><td class="py-1">Laboratory Diagnostic Charges</td><td class="py-1 text-right">₹${bill.lab_charges.toLocaleString()}</td></tr>
            <tr><td class="py-1">Pharmacy & Medication</td><td class="py-1 text-right">₹${bill.medicine_charges.toLocaleString()}</td></tr>
        `;

        document.getElementById('inv-subtotal').innerText = `₹${bill.subtotal.toLocaleString()}`;
        document.getElementById('inv-discount').innerText = `-₹${bill.discount.toLocaleString()}`;
        document.getElementById('inv-tax').innerText = `+₹${bill.tax.toLocaleString()}`;
        document.getElementById('inv-grandtotal').innerText = `₹${bill.grand_total.toLocaleString()}`;

        openModal('modal-printable-invoice');
    }
}

// ==========================================
// 10. EMERGENCY MANAGEMENT
// ==========================================
async function loadEmergencies() {
    const res = await fetch('/api/emergencies');
    const cases = await res.json();

    const tbody = document.getElementById('emergency-table-body');
    tbody.innerHTML = cases.map(e => `
        <tr class="hover:bg-slate-50">
            <td class="p-3 font-mono font-bold text-red-600">${e.emergency_id}</td>
            <td class="p-3 font-bold text-slate-800">${e.patient_name}</td>
            <td class="p-3 text-slate-600 text-xs">${e.arrival_time}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${getPriorityClass(e.priority)}">${e.priority}</span></td>
            <td class="p-3 text-slate-700 font-medium">${e.symptoms}</td>
            <td class="p-3 text-slate-700">${e.assigned_doctor_name} <span class="text-xs font-bold text-slate-900">(${e.assigned_room})</span></td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${e.treatment_status}</span></td>
            <td class="p-3 text-right">
                <button onclick="updateEmergencyStatus('${e.emergency_id}')" class="px-2 py-1 bg-red-600 text-white rounded text-[10px] font-bold hover:bg-red-700">Update Case</button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="8" class="p-4 text-center text-slate-400">No active emergency cases.</td></tr>';
}

async function handleEmergencySubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    const doc = doctorsList.find(d => d.doctor_id === body.assigned_doctor_id);
    body.assigned_doctor_name = doc ? doc.name : 'Dr. Duty Doctor';

    const res = await fetch('/api/emergencies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        alert(`Emergency Triage Logged! ID: ${data.emergency_id}`);
        closeModal('modal-emergency');
        e.target.reset();
        loadEmergencies();
    }
}

async function updateEmergencyStatus(id) {
    const status = prompt('Update Emergency Status (e.g. Under Treatment, Stabilized, Transferred, Completed):');
    if (!status) return;

    await fetch(`/api/emergencies/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ treatment_status: status })
    });
    loadEmergencies();
}

// ==========================================
// 11. PATIENT MEDICAL HISTORY TIMELINE
// ==========================================
async function loadHistoryPatients() {
    const res = await fetch('/api/patients');
    const patients = await res.json();

    const select = document.getElementById('history-patient-select');
    select.innerHTML = '<option value="">Select Patient...</option>' + patients.map(p => `
        <option value="${p.patient_id}">${p.full_name} (${p.patient_id}) - ${p.department}</option>
    `).join('');

    // Pre-select Rahul Sharma (P1024) to match prompt example!
    select.value = 'P1024';
    loadPatientProfile('P1024');
}

async function viewPatientProfile(patientId) {
    switchView('history');
    document.getElementById('history-patient-select').value = patientId;
    loadPatientProfile(patientId);
}

async function loadPatientProfile(patientId) {
    if (!patientId) {
        document.getElementById('patient-profile-card').classList.add('hidden');
        return;
    }

    const res = await fetch(`/api/patients/${patientId}/profile`);
    const data = await res.json();
    const p = data.patient;

    document.getElementById('patient-profile-card').classList.remove('hidden');
    document.getElementById('prof-name').innerText = p.full_name;
    document.getElementById('prof-id').innerText = p.patient_id;
    document.getElementById('prof-blood').innerText = p.blood_group;
    document.getElementById('prof-doctor').innerText = p.doctor_name || 'Dr. Ananya Rao';
    document.getElementById('prof-contact').innerText = p.emergency_contact;

    const timeline = document.getElementById('prof-timeline');
    timeline.innerHTML = data.history.map(h => `
        <div class="relative timeline-item space-y-1">
            <div class="text-xs font-bold text-sky-600">${h.record_date}</div>
            <div class="text-sm font-bold text-slate-800">Diagnosis: <span class="text-slate-900">${h.diagnosis}</span></div>
            <div class="text-xs font-medium text-emerald-700">Treatment: ${h.treatment}</div>
            ${h.doctor_notes ? `<div class="text-xs text-slate-500 italic bg-white p-2 rounded border border-slate-200">${h.doctor_notes}</div>` : ''}
            <div class="text-[10px] text-slate-400 font-semibold">Attending: ${h.doctor_name}</div>
        </div>
    `).join('') || '<div class="text-slate-400 text-xs">No medical history timeline recorded.</div>';
}

// ==========================================
// 12. REPORTS & ANALYTICS
// ==========================================
async function loadReports() {
    const res = await fetch('/api/reports');
    const data = await res.json();

    document.getElementById('rep-patients').innerText = data.summary.patients_registered.toLocaleString();
    document.getElementById('rep-appointments').innerText = data.summary.appointments.toLocaleString();
    document.getElementById('rep-admissions').innerText = data.summary.admissions.toLocaleString();
    document.getElementById('rep-discharges').innerText = data.summary.discharges.toLocaleString();
    document.getElementById('rep-lab').innerText = data.summary.lab_tests.toLocaleString();
    document.getElementById('rep-revenue').innerText = data.summary.revenue_formatted;

    initReportsCharts(data);
}

// ==========================================
// UTILITY FUNCTIONS & DROPDOWNS
// ==========================================
async function loadDropdownOptions() {
    const [docsRes, patsRes, bedsRes, medsRes] = await Promise.all([
        fetch('/api/doctors'),
        fetch('/api/patients'),
        fetch('/api/beds?status=Available'),
        fetch('/api/pharmacy')
    ]);

    doctorsList = await docsRes.json();
    patientsList = await patsRes.json();
    bedsList = await bedsRes.json();
    pharmacyList = await medsRes.json();

    // Populate Doctor dropdowns
    const docOptions = doctorsList.map(d => `<option value="${d.doctor_id}">${d.name} (${d.specialization})</option>`).join('');
    ['patient-doc-select', 'apt-doctor-select', 'adm-doctor-select', 'lab-doctor-select', 'emg-doctor-select'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = docOptions;
    });

    // Populate Patient dropdowns
    const patOptions = patientsList.map(p => `<option value="${p.patient_id}">${p.full_name} (${p.patient_id})</option>`).join('');
    ['apt-patient-select', 'adm-patient-select', 'lab-patient-select', 'bill-patient-select'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = patOptions;
    });

    // Populate Available Beds
    const bedSelect = document.getElementById('adm-bed-select');
    if (bedSelect) bedSelect.innerHTML = bedsList.map(b => `<option value="${b.bed_id}">${b.ward} - ${b.room_number} (${b.bed_id})</option>`).join('');

    // Populate POS Medicines
    const posSelect = document.getElementById('pos-medicine-select');
    if (posSelect) posSelect.innerHTML = pharmacyList.map(m => `<option value="${m.medicine_id}">${m.medicine_name} - ₹${m.unit_price} (${m.quantity} in stock)</option>`).join('');
}

function openModal(modalId) {
    document.getElementById(modalId)?.classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId)?.classList.add('hidden');
}

function getStatusClass(status) {
    const map = {
        'Scheduled': 'bg-sky-100 text-sky-800',
        'Confirmed': 'bg-indigo-100 text-indigo-800',
        'Completed': 'bg-emerald-100 text-emerald-800',
        'Cancelled': 'bg-rose-100 text-rose-800',
        'No Show': 'bg-slate-100 text-slate-700'
    };
    return map[status] || 'bg-slate-100 text-slate-700';
}

function getPriorityClass(prio) {
    const map = {
        'Critical': 'priority-critical',
        'Urgent': 'priority-urgent',
        'Moderate': 'priority-moderate',
        'Stable': 'priority-stable'
    };
    return map[prio] || 'priority-stable';
}

function handleGlobalSearch(query) {
    if (!query) return;
    console.log('Global search query:', query);
}
