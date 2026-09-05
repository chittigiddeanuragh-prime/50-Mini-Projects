// Chart.js Analytics Initializer for Hospital Management System

let revenueChartInstance = null;
let deptChartInstance = null;
let bedChartInstance = null;
let pharmacyChartInstance = null;

function initReportsCharts(data) {
    if (typeof Chart === 'undefined') return;

    // 1. Revenue Monthly Trend Chart
    const ctxRevenue = document.getElementById('revenueChart');
    if (ctxRevenue) {
        if (revenueChartInstance) revenueChartInstance.destroy();
        
        const labels = data.revenue_chart ? data.revenue_chart.map(r => r.month) : ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
        const values = data.revenue_chart ? data.revenue_chart.map(r => r.revenue / 100000) : [14.2, 16.5, 15.8, 17.4, 18.6, 19.2];

        revenueChartInstance = new Chart(ctxRevenue, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Revenue (in ₹ Lakhs)',
                    data: values,
                    borderColor: '#0284c7',
                    backgroundColor: 'rgba(2, 132, 199, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#0369a1',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(context) { return ` Revenue: ₹${context.raw} Lakhs`; }
                        }
                    }
                },
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    }

    // 2. Department Statistics Doughnut Chart
    const ctxDept = document.getElementById('deptChart');
    if (ctxDept) {
        if (deptChartInstance) deptChartInstance.destroy();

        const deptLabels = data.department_stats ? data.department_stats.map(d => d.department) : ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Emergency'];
        const deptValues = data.department_stats ? data.department_stats.map(d => d.patient_count) : [320, 240, 410, 190, 88];

        deptChartInstance = new Chart(ctxDept, {
            type: 'doughnut',
            data: {
                labels: deptLabels,
                datasets: [{
                    data: deptValues,
                    backgroundColor: ['#0284c7', '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' }
                }
            }
        });
    }

    // 3. Top Pharmacy Sales Bar Chart
    const ctxPharma = document.getElementById('pharmacySalesChart');
    if (ctxPharma) {
        if (pharmacyChartInstance) pharmacyChartInstance.destroy();

        const pharmaLabels = data.pharmacy_sales ? data.pharmacy_sales.map(p => p.medicine_name) : ['Paracetamol 650mg', 'Amoxicillin 500mg', 'Metformin 500mg', 'Pantoprazole 40mg', 'Atorvastatin 10mg'];
        const pharmaValues = data.pharmacy_sales ? data.pharmacy_sales.map(p => p.total_qty) : [1450, 890, 1200, 950, 620];

        pharmacyChartInstance = new Chart(ctxPharma, {
            type: 'bar',
            data: {
                labels: pharmaLabels,
                datasets: [{
                    label: 'Units Sold',
                    data: pharmaValues,
                    backgroundColor: '#10b981',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}
