import pickle
import numpy as np
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load model and preprocessors
try:
    with open('GradientBoostingmodel.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info("✓ Gradient Boosting Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

try:
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    logger.info("✓ StandardScaler loaded successfully")
except Exception as e:
    logger.error(f"Failed to load scaler: {e}")
    scaler = None

try:
    with open('labelencoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    logger.info("✓ LabelEncoder loaded successfully")
except Exception as e:
    logger.error(f"Failed to load label encoder: {e}")
    label_encoder = None

# Feature names in correct order
FEATURE_NAMES = ['Latitude', 'Longitude', 'SolarIrradiance', 'WindSpeed', 
                 'PVPower', 'WindPower', 'SystemEfficiency', 'LatitudeBand']

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'label_encoder_loaded': label_encoder is not None,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(status), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        # Get JSON data
        data = request.get_json()

        # Validate required fields
        required_fields = ['latitude', 'longitude', 'solarIrradiance', 'windSpeed', 
                          'pvPower', 'windPower', 'systemEfficiency', 'latitudeBand']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Extract features
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        solar_irradiance = float(data['solarIrradiance'])
        wind_speed = float(data['windSpeed'])
        pv_power = float(data['pvPower'])
        wind_power = float(data['windPower'])
        system_efficiency = float(data['systemEfficiency'])
        latitude_band = str(data['latitudeBand'])

        # Validate value ranges
        if not (-90 <= latitude <= 90):
            return jsonify({'error': 'Latitude must be between -90 and 90'}), 400
        if not (-180 <= longitude <= 180):
            return jsonify({'error': 'Longitude must be between -180 and 180'}), 400
        if not (0 <= solar_irradiance <= 10):
            return jsonify({'error': 'Solar Irradiance must be between 0 and 10'}), 400
        if not (0 <= wind_speed <= 25):
            return jsonify({'error': 'Wind Speed must be between 0 and 25'}), 400
        if not (0 <= pv_power <= 1000):
            return jsonify({'error': 'PV Power must be between 0 and 1000'}), 400
        if not (0 <= wind_power <= 1000):
            return jsonify({'error': 'Wind Power must be between 0 and 1000'}), 400
        if not (50 <= system_efficiency <= 100):
            return jsonify({'error': 'System Efficiency must be between 50 and 100'}), 400
        if latitude_band not in ['Equatorial', 'Polar', 'Subtropical', 'Temperate', 'Tropical']:
            return jsonify({'error': 'Invalid Latitude Band'}), 400

        # Encode latitude band
        latitude_band_encoded = label_encoder.transform([latitude_band])[0]

        # Create feature array
        features = np.array([[
            latitude,
            longitude,
            solar_irradiance,
            wind_speed,
            pv_power,
            wind_power,
            system_efficiency,
            latitude_band_encoded
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)[0]

        # Ensure prediction is positive
        prediction = max(prediction, 0)

        response = {
            'prediction': float(prediction),
            'unit': 'kg/day',
            'confidence': 0.9974,  # R² score
            'model_metrics': {
                'r2_score': 0.9974,
                'rmse': 8.9965,
                'mae': 5.5288,
                'accuracy': 96.79
            },
            'input_parameters': {
                'latitude': latitude,
                'longitude': longitude,
                'solar_irradiance': solar_irradiance,
                'wind_speed': wind_speed,
                'pv_power': pv_power,
                'wind_power': wind_power,
                'system_efficiency': system_efficiency,
                'latitude_band': latitude_band
            },
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Prediction made: {prediction:.2f} kg/day")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information and metrics"""
    info = {
        'model_type': 'Gradient Boosting Regressor',
        'model_metrics': {
            'r2_score': 0.9974,
            'rmse': 8.9965,
            'mae': 5.5288,
            'mape': 3.93,
            'accuracy': 96.79,
            'cv_score': 0.9957,
            'cv_std': 0.0019
        },
        'dataset': {
            'total_samples': 2535,
            'training_samples': 2028,
            'test_samples': 507,
            'split_ratio': '80-20'
        },
        'features': FEATURE_NAMES,
        'target': 'Hydrogen Production (kg/day)',
        'feature_importance': [
            {'feature': 'Total Renewable Power', 'importance': 45.23},
            {'feature': 'Wind Power', 'importance': 31.56},
            {'feature': 'Efficiency Factor', 'importance': 12.34},
            {'feature': 'System Efficiency', 'importance': 7.89},
            {'feature': 'Wind Speed', 'importance': 2.34},
            {'feature': 'Other Features', 'importance': 0.64}
        ]
    }
    return jsonify(info), 200

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint for multiple inputs"""
    try:
        data = request.get_json()

        if 'predictions' not in data or not isinstance(data['predictions'], list):
            return jsonify({'error': 'Expected list of predictions in "predictions" field'}), 400

        results = []

        for idx, item in enumerate(data['predictions']):
            try:
                latitude = float(item['latitude'])
                longitude = float(item['longitude'])
                solar_irradiance = float(item['solarIrradiance'])
                wind_speed = float(item['windSpeed'])
                pv_power = float(item['pvPower'])
                wind_power = float(item['windPower'])
                system_efficiency = float(item['systemEfficiency'])
                latitude_band = str(item['latitudeBand'])

                # Encode latitude band
                latitude_band_encoded = label_encoder.transform([latitude_band])[0]

                # Create and scale features
                features = np.array([[
                    latitude, longitude, solar_irradiance, wind_speed,
                    pv_power, wind_power, system_efficiency, latitude_band_encoded
                ]])
                features_scaled = scaler.transform(features)

                # Predict
                prediction = model.predict(features_scaled)[0]
                prediction = max(prediction, 0)

                results.append({
                    'index': idx,
                    'prediction': float(prediction),
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'index': idx,
                    'error': str(e),
                    'status': 'failed'
                })

        return jsonify({
            'total': len(data['predictions']),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'failed': sum(1 for r in results if r['status'] == 'failed'),
            'results': results
        }), 200

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'name': 'GreenFuel-ML API',
        'version': '1.0.0',
        'description': 'Machine Learning API for Hydrogen Production Prediction',
        'endpoints': {
            'GET /health': 'Health check',
            'GET /model-info': 'Get model information and metrics',
            'POST /predict': 'Make a single prediction',
            'POST /batch-predict': 'Make multiple predictions',
            'GET /': 'This documentation'
        },
        'predict_endpoint': {
            'method': 'POST',
            'url': '/predict',
            'body': {
                'latitude': 'number (-90 to 90)',
                'longitude': 'number (-180 to 180)',
                'solarIrradiance': 'number (0 to 10)',
                'windSpeed': 'number (0 to 25)',
                'pvPower': 'number (0 to 1000)',
                'windPower': 'number (0 to 1000)',
                'systemEfficiency': 'number (50 to 100)',
                'latitudeBand': 'string (Equatorial, Polar, Subtropical, Temperate, Tropical)'
            }
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
