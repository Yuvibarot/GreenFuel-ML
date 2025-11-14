// ============================================================================
// GreenFuel-ML Frontend Application
// Pure Vanilla JavaScript - No frameworks, no build tools required
// ============================================================================

// Configuration
const CONFIG = {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000',
    API_TIMEOUT: process.env.REACT_APP_API_TIMEOUT || 30000,
    USE_MOCK_PREDICTIONS: process.env.REACT_APP_USE_MOCK_PREDICTIONS === 'true',
};

// Model metadata
const MODEL_DATA = {
    metrics: {
        r2_score: 0.9974,
        rmse: 8.9965,
        mae: 5.5288,
        mape: 3.93,
        accuracy: 96.79,
        cv_score: 0.9957,
        cv_std: 0.0019,
    },
    dataset: {
        total_samples: 2535,
        training_samples: 2028,
        test_samples: 507,
        features: 8,
    },
    features: [
        { name: 'Latitude', type: 'number', min: -90, max: 90, default: 0, unit: '°', description: 'Geographic latitude' },
        { name: 'Longitude', type: 'number', min: -180, max: 180, default: 0, unit: '°', description: 'Geographic longitude' },
        { name: 'Solar Irradiance', type: 'number', min: 0, max: 10, default: 5.5, unit: 'kWh/m²/day', description: 'Average solar irradiance' },
        { name: 'Wind Speed', type: 'number', min: 0, max: 25, default: 7.5, unit: 'm/s', description: 'Average wind speed' },
        { name: 'PV Power', type: 'number', min: 0, max: 1000, default: 250, unit: 'kW', description: 'Solar PV power capacity' },
        { name: 'Wind Power', type: 'number', min: 0, max: 1000, default: 300, unit: 'kW', description: 'Wind turbine power capacity' },
        { name: 'System Efficiency', type: 'number', min: 50, max: 100, default: 75, unit: '%', description: 'PEM electrolyzer efficiency' },
        { name: 'Latitude Band', type: 'select', options: ['Equatorial', 'Polar', 'Subtropical', 'Temperate', 'Tropical'], default: 'Temperate', description: 'Climate zone classification' },
    ],
    featureImportance: [
        { feature: 'Total Renewable Power', importance: 45.23 },
        { feature: 'Wind Power', importance: 31.56 },
        { feature: 'Efficiency Factor', importance: 12.34 },
        { feature: 'System Efficiency', importance: 7.89 },
        { feature: 'Wind Speed', importance: 2.34 },
        { feature: 'Other Features', importance: 0.64 },
    ],
};

// ============================================================================
// Page Management
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
    const navLink = document.querySelector(`[data-page="${pageName}"]`);
    if (navLink) {
        navLink.classList.add('active');
    }
}

// ============================================================================
// Form Generation
// ============================================================================

function generateFormFields() {
    const formGrid = document.getElementById('formGrid');
    if (!formGrid) return;

    formGrid.innerHTML = '';

    MODEL_DATA.features.forEach((feature, index) => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';

        if (feature.type === 'select') {
            formGroup.innerHTML = `
                <label>
                    ${feature.name}
                    <span class="unit">${feature.unit || ''}</span>
                </label>
                <select id="${feature.name.toLowerCase().replace(/ /g, '')}" name="${feature.name.toLowerCase().replace(/ /g, '')}">
                    ${feature.options.map(opt => `<option value="${opt}" ${opt === feature.default ? 'selected' : ''}>${opt}</option>`).join('')}
                </select>
                <div class="description">${feature.description}</div>
            `;
        } else {
            const fieldId = feature.name.toLowerCase().replace(/ /g, '');
            formGroup.innerHTML = `
                <label>
                    ${feature.name}
                    <span class="unit">${feature.unit}</span>
                </label>
                <input type="number" id="${fieldId}" name="${fieldId}" min="${feature.min}" max="${feature.max}" value="${feature.default}" step="0.01" required>
                <div class="slider-value" id="${fieldId}Value">${feature.default}</div>
                <input type="range" id="${fieldId}Slider" min="${feature.min}" max="${feature.max}" value="${feature.default}" step="0.1">
                <div class="description">${feature.description}</div>
            `;

            setTimeout(() => {
                const input = document.getElementById(fieldId);
                const slider = document.getElementById(`${fieldId}Slider`);
                const valueDisplay = document.getElementById(`${fieldId}Value`);

                if (slider && input && valueDisplay) {
                    slider.addEventListener('input', () => {
                        input.value = slider.value;
                        valueDisplay.textContent = slider.value;
                    });

                    input.addEventListener('change', () => {
                        slider.value = input.value;
                        valueDisplay.textContent = input.value;
                    });
                }
            }, 100);
        }

        formGrid.appendChild(formGroup);
    });
}

// ============================================================================
// Metrics Display
// ============================================================================

function displayMetrics() {
    const metricsGrid = document.getElementById('metricsGrid');
    if (!metricsGrid) return;

    const metrics = [
        { label: 'Model Type', value: 'Gradient Boosting' },
        { label: 'Accuracy', value: '96.79%' },
        { label: 'R² Score', value: '0.9974' },
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
// Model Info Display
// ============================================================================

function displayModelInfo() {
    // Metrics Table
    const metricsTable = document.getElementById('metricsTable');
    if (metricsTable) {
        metricsTable.innerHTML = `
            <tr><th>Metric</th><th>Value</th></tr>
            ${Object.entries(MODEL_DATA.metrics).map(([key, value]) => `
                <tr>
                    <td>${key.replace(/_/g, ' ').toUpperCase()}</td>
                    <td><strong>${typeof value === 'number' ? value.toFixed(4) : value}</strong></td>
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
                    <td>${key.replace(/_/g, ' ').toUpperCase()}</td>
                    <td><strong>${value}</strong></td>
                </tr>
            `).join('')}
        `;
    }

    // Feature Importance
    const featureImportance = document.getElementById('featureImportance');
    if (featureImportance) {
        featureImportance.innerHTML = MODEL_DATA.featureImportance.map(fi => `
            <div class="importance-bar">
                <div class="importance-label">${fi.feature}</div>
                <div class="importance-visual">
                    <div class="importance-fill" style="width: ${fi.importance}%"></div>
                </div>
                <div class="importance-value">${fi.importance.toFixed(2)}%</div>
            </div>
        `).join('');
    }
}

// ============================================================================
// Prediction Logic
// ============================================================================

// Mock prediction function (for development/testing)
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

    // Add small random variation
    const variation = base * (0.97 + Math.random() * 0.06);
    return Math.max(variation, 10);
}

// Real API prediction function
async function apiPrediction(inputs) {
    const response = await fetch(`${CONFIG.API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            latitude: parseFloat(inputs.latitude),
            longitude: parseFloat(inputs.longitude),
            solarIrradiance: parseFloat(inputs.solarirradiance),
            windSpeed: parseFloat(inputs.windspeed),
            pvPower: parseFloat(inputs.pvpower),
            windPower: parseFloat(inputs.windpower),
            systemEfficiency: parseFloat(inputs.systemefficiency),
            latitudeBand: inputs.latitudeband,
        }),
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return (await response.json()).prediction;
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

        // Make prediction
        let prediction;
        if (CONFIG.USE_MOCK_PREDICTIONS) {
            prediction = mockPrediction(inputs);
        } else {
            prediction = await apiPrediction(inputs);
        }

        // Display results
        document.getElementById('predictionValue').textContent = prediction.toFixed(2);
        document.getElementById('confidenceFill').style.width = '99.74%';
        document.getElementById('confidenceValue').textContent = '99.74%';

        // Display input summary
        const summary = document.getElementById('inputSummary');
        summary.innerHTML = Object.entries(inputs).map(([key, value]) => {
            const feature = MODEL_DATA.features.find(f => f.name.toLowerCase().replace(/ /g, '') === key);
            if (feature) {
                return `<div><strong>${feature.name}:</strong> ${value} ${feature.unit}</div>`;
            }
            return '';
        }).join('');

        resultsDiv.classList.add('show');
        errorDiv.innerHTML = '';

        // Scroll to results
        setTimeout(() => resultsDiv.scrollIntoView({ behavior: 'smooth' }), 100);

    } catch (error) {
        console.error('Prediction error:', error);
        errorDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
        resultsDiv.classList.remove('show');
    } finally {
        btn.disabled = false;
        btn.textContent = '🚀 Predict Hydrogen Production';
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
        const slider = document.getElementById(`${fieldId}Slider`);
        const valueDisplay = document.getElementById(`${fieldId}Value`);

        if (input && slider && valueDisplay) {
            input.value = feature.default;
            slider.value = feature.default;
            valueDisplay.textContent = feature.default;
        }
    });
}

// ============================================================================
// Event Listeners
// ============================================================================

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = e.target.dataset.page;
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
// Initialization
// ============================================================================

function initializeApp() {
    console.log('🚀 GreenFuel-ML Application Initializing...');
    console.log(`Configuration: ${CONFIG.USE_MOCK_PREDICTIONS ? 'Mock' : 'Real'} Predictions`);
    console.log(`API URL: ${CONFIG.API_BASE_URL}`);

    // Initialize UI
    displayMetrics();
    generateFormFields();
    displayModelInfo();
    setupEventListeners();

    // Show default page
    showPage('dashboard');

    console.log('✅ GreenFuel-ML Application Ready!');
}

// Start app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        mockPrediction,
        apiPrediction,
        CONFIG,
        MODEL_DATA,
    };
}
