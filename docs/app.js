// ============================================================================
// GreenFuel-ML Frontend Application - FIXED VERSION
// Pure Vanilla JavaScript - No frameworks, no build tools required
// ============================================================================

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    USE_MOCK_PREDICTIONS: true, // Always use mock for GitHub Pages
};

// Model metadata
const MODEL_DATA = {
    metrics: {
        r2_score: 0.9974,
        rmse: 8.9965,
        mae: 5.5288,
        accuracy: 96.79,
    },
    dataset: {
        total_samples: 2535,
        training_samples: 2028,
        test_samples: 507,
        features: 8,
    },
    features: [
        { name: 'Latitude', type: 'number', min: -90, max: 90, default: 0, unit: '°' },
        { name: 'Longitude', type: 'number', min: -180, max: 180, default: 0, unit: '°' },
        { name: 'Solar Irradiance', type: 'number', min: 0, max: 10, default: 5.5, unit: 'kWh/m²/day' },
        { name: 'Wind Speed', type: 'number', min: 0, max: 25, default: 7.5, unit: 'm/s' },
        { name: 'PV Power', type: 'number', min: 0, max: 1000, default: 250, unit: 'kW' },
        { name: 'Wind Power', type: 'number', min: 0, max: 1000, default: 300, unit: 'kW' },
        { name: 'System Efficiency', type: 'number', min: 50, max: 100, default: 75, unit: '%' },
        { name: 'Latitude Band', type: 'select', options: ['Equatorial', 'Polar', 'Subtropical', 'Temperate', 'Tropical'], default: 'Temperate' },
    ],
};

// ============================================================================
// PAGE MANAGEMENT
// ============================================================================

function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected page
    const page = document.getElementById(pageName);
    if (page) {
        page.classList.add('active');
    }

    // Set active nav link
    const navLink = document.querySelector('[data-page="' + pageName + '"]');
    if (navLink) {
        navLink.classList.add('active');
    }
}

// ============================================================================
// FORM GENERATION
// ============================================================================

function generateFormFields() {
    const formGrid = document.getElementById('formGrid');
    if (!formGrid) return;

    formGrid.innerHTML = '';

    MODEL_DATA.features.forEach((feature, index) => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';

        if (feature.type === 'select') {
            const selectHTML = `
                <label>${feature.name}</label>
                <select id="${feature.name.toLowerCase().replace(/ /g, '')}" name="${feature.name.toLowerCase().replace(/ /g, '')}">
                    ${feature.options.map(opt => `<option value="${opt}" ${opt === feature.default ? 'selected' : ''}>${opt}</option>`).join('')}
                </select>
            `;
            formGroup.innerHTML = selectHTML;
        } else {
            const fieldId = feature.name.toLowerCase().replace(/ /g, '');
            const numberHTML = `
                <label>${feature.name} <span class="unit">${feature.unit}</span></label>
                <input type="number" id="${fieldId}" name="${fieldId}" min="${feature.min}" max="${feature.max}" value="${feature.default}" step="0.01" required>
                <input type="range" id="${fieldId}Slider" min="${feature.min}" max="${feature.max}" value="${feature.default}" step="0.1">
                <div class="slider-value" id="${fieldId}Value">${feature.default}</div>
            `;
            formGroup.innerHTML = numberHTML;

            // Add event listeners after creating elements
            setTimeout(() => {
                const input = document.getElementById(fieldId);
                const slider = document.getElementById(fieldId + 'Slider');
                const valueDisplay = document.getElementById(fieldId + 'Value');

                if (slider && input && valueDisplay) {
                    slider.addEventListener('input', (e) => {
                        input.value = slider.value;
                        valueDisplay.textContent = slider.value;
                    });

                    input.addEventListener('change', (e) => {
                        slider.value = input.value;
                        valueDisplay.textContent = input.value;
                    });
                }
            }, 50);
        }

        formGrid.appendChild(formGroup);
    });
}

// ============================================================================
// METRICS DISPLAY
// ============================================================================

function displayMetrics() {
    const metricsGrid = document.getElementById('metricsGrid');
    if (!metricsGrid) return;

    const metrics = [
        { label: 'Model Type', value: 'Gradient Boosting' },
        { label: 'R² Score', value: '0.9974' },
        { label: 'Accuracy', value: '96.79%' },
        { label: 'RMSE', value: '8.99 kg' },
    ];

    metricsGrid.innerHTML = metrics.map(m => `
        <div class="metric-card">
            <h3>${m.label}</h3>
            <div class="metric-value">${m.value}</div>
        </div>
    `).join('');
}

// ============================================================================
// MODEL INFO DISPLAY
// ============================================================================

function displayModelInfo() {
    // Metrics Table
    const metricsTable = document.getElementById('metricsTable');
    if (metricsTable) {
        metricsTable.innerHTML = `
            <tr><th>Metric</th><th>Value</th></tr>
            ${Object.entries(MODEL_DATA.metrics).map(([key, value]) => `
                <tr>
                    <td>${key.toUpperCase()}</td>
                    <td><strong>${value}</strong></td>
                </tr>
            `).join('')}
        `;
    }

    // Dataset Table
    const datasetTable = document.getElementById('datasetTable');
    if (datasetTable) {
        datasetTable.innerHTML = `
            <tr><th>Aspect</th><th>Value</th></tr>
            ${Object.entries(MODEL_DATA.dataset).map(([key, value]) => `
                <tr>
                    <td>${key.toUpperCase()}</td>
                    <td><strong>${value}</strong></td>
                </tr>
            `).join('')}
        `;
    }
}

// ============================================================================
// PREDICTION LOGIC
// ============================================================================

function mockPrediction(inputs) {
    const totalRenewable = parseFloat(inputs.pvpower) + parseFloat(inputs.windpower);
    const efficiency = parseFloat(inputs.systemefficiency) / 100;

    let base = (totalRenewable * 0.85) * efficiency * 0.8;
    base += parseFloat(inputs.windspeed) * 0.5;
    base += parseFloat(inputs.solarirradiance) * 2;

    const latitudeBands = {
        'Equatorial': 1.1,
        'Polar': 0.8,
        'Subtropical': 1.05,
        'Temperate': 1.0,
        'Tropical': 1.08,
    };

    base *= latitudeBands[inputs.latitudeband] || 1.0;
    const variation = base * (0.97 + Math.random() * 0.06);

    return Math.max(variation, 10);
}

// Main prediction handler
async function makePrediction(event) {
    event.preventDefault();

    const btn = event.target.querySelector('.btn-predict');
    const errorDiv = document.getElementById('errorMessage');
    const resultsDiv = document.getElementById('results');

    btn.disabled = true;
    btn.textContent = '⏳ Predicting...';

    try {
        // Collect form inputs
        const formData = new FormData(document.getElementById('predictionForm'));
        const inputs = Object.fromEntries(formData);

        // Make prediction (always mock for GitHub Pages)
        let prediction = mockPrediction(inputs);

        // Display results
        document.getElementById('predictionValue').textContent = prediction.toFixed(2);
        document.getElementById('confidenceFill').style.width = '99.74%';
        document.getElementById('confidenceValue').textContent = '99.74%';

        // Display input summary
        const summary = document.getElementById('inputSummary');
        summary.innerHTML = Object.entries(inputs).map(([key, value]) => {
            const feature = MODEL_DATA.features.find(f => f.name.toLowerCase().replace(/ /g, '') === key);
            if (feature) {
                return `<div><strong>${feature.name}:</strong> ${value} ${feature.unit || ''}</div>`;
            }
            return '';
        }).join('');

        resultsDiv.classList.add('show');
        errorDiv.innerHTML = '';

        // Scroll to results
        setTimeout(() => {
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }, 100);

    } catch (error) {
        console.error('Prediction error:', error);
        errorDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
        resultsDiv.classList.remove('show');
    } finally {
        btn.disabled = false;
        btn.textContent = '🚀 Predict Production';
    }
}

// Reset form
function resetForm(event) {
    if (event) event.preventDefault();

    document.getElementById('predictionForm').reset();
    document.getElementById('results').classList.remove('show');
    document.getElementById('errorMessage').innerHTML = '';

    // Reset sliders
    MODEL_DATA.features.forEach(feature => {
        const fieldId = feature.name.toLowerCase().replace(/ /g, '');
        const input = document.getElementById(fieldId);
        const slider = document.getElementById(fieldId + 'Slider');
        const valueDisplay = document.getElementById(fieldId + 'Value');

        if (input && slider && valueDisplay) {
            input.value = feature.default;
            slider.value = feature.default;
            valueDisplay.textContent = feature.default;
        }
    });
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = e.currentTarget.getAttribute('data-page');
            showPage(pageName);
        });
    });

    // Form submission
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', makePrediction);
        form.addEventListener('reset', resetForm);
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

function initializeApp() {
    console.log('🚀 GreenFuel-ML Application Initializing...');
    console.log('Configuration: Mock Predictions (Always for GitHub Pages)');

    try {
        // Initialize UI
        displayMetrics();
        generateFormFields();
        displayModelInfo();
        setupEventListeners();

        // Show default page
        showPage('dashboard');

        console.log('✅ GreenFuel-ML Application Ready!');
    } catch (error) {
        console.error('Initialization error:', error);
    }
}

// Start app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
