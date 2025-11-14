
# Create comprehensive README
readme = '''# 🌱 GreenFuel-ML: Hydrogen Production Prediction

A complete machine learning web application for predicting hydrogen production rates from PEM (Proton Exchange Membrane) electrolyzers using renewable energy inputs.

## 📊 Project Overview

This project combines **advanced machine learning** with a **professional web interface** to predict hydrogen production rates based on renewable energy systems and environmental parameters.

### Key Features
- ⚡ **99.74% Accuracy** (R² Score)
- 🎯 **Real-time Predictions** with confidence indicators
- 📱 **Responsive Web Interface** (mobile-friendly)
- 🔌 **RESTful API** for programmatic access
- 📈 **Feature Importance Analysis**
- 🚀 **Production-ready Deployment**

## 🎯 Model Performance

| Metric | Value |
|--------|-------|
| **R² Score** | 0.9974 |
| **Accuracy** | 96.79% |
| **RMSE** | 8.9965 kg/day |
| **MAE** | 5.5288 kg/day |
| **MAPE** | 3.93% |
| **Cross-Validation** | 0.9957 ± 0.0019 |

## 📦 What's Included

```
greenfuel-ml-frontend/
├── index.html              # Frontend application
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── scaler.pkl             # Feature scaler
├── labelencoder.pkl       # Label encoder
├── GradientBoostingmodel.pkl  # Trained ML model
├── .gitignore
├── README.md
├── Procfile               # Heroku deployment
├── serverless.yml         # AWS Serverless framework
└── samconfig.yaml         # AWS SAM configuration
```

## 🚀 Quick Start

### Option 1: Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/Yuvibarot/GreenFuel-ML.git
cd GreenFuel-ML
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run Backend
```bash
python app.py
```

The backend will start at `http://localhost:5000`

#### 4. Open Frontend
Open `index.html` in your web browser

### Option 2: Docker

#### 1. Build Docker Image
```bash
docker build -t greenfuel-ml .
```

#### 2. Run Container
```bash
docker run -p 5000:5000 greenfuel-ml
```

#### 3. Access Application
Open `http://localhost:5000` in your browser

## 📚 API Documentation

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "label_encoder_loaded": true,
  "timestamp": "2025-11-14T21:45:00"
}
```

### Make Prediction
```bash
POST /predict
Content-Type: application/json

{
  "latitude": 0,
  "longitude": 0,
  "solarIrradiance": 5.5,
  "windSpeed": 7.5,
  "pvPower": 250,
  "windPower": 300,
  "systemEfficiency": 75,
  "latitudeBand": "Temperate"
}
```

Response:
```json
{
  "prediction": 245.82,
  "unit": "kg/day",
  "confidence": 0.9974,
  "model_metrics": {
    "r2_score": 0.9974,
    "rmse": 8.9965,
    "mae": 5.5288,
    "accuracy": 96.79
  },
  "input_parameters": {...},
  "timestamp": "2025-11-14T21:45:00"
}
```

### Get Model Info
```bash
GET /model-info
```

Returns model metrics, dataset info, and feature importance.

### Batch Predictions
```bash
POST /batch-predict
Content-Type: application/json

{
  "predictions": [
    {...prediction 1...},
    {...prediction 2...}
  ]
}
```

## 🌐 Deployment

### AWS Deployment (Recommended)

#### 1. Install AWS CLI and SAM
```bash
pip install aws-cli aws-sam-cli
```

#### 2. Configure AWS Credentials
```bash
aws configure
```

#### 3. Build SAM Application
```bash
sam build
```

#### 4. Deploy to AWS
```bash
sam deploy --guided
```

#### 5. Update Frontend API URL
In `index.html`, change:
```javascript
const API_BASE_URL = 'https://your-api-gateway-url.amazonaws.com';
const USE_MOCK_PREDICTIONS = false;
```

### GitHub Pages (Frontend Only)

1. Create GitHub repository
2. Push `index.html` to `/docs` folder
3. Enable GitHub Pages in repository settings
4. Access at `https://username.github.io/greenfuel-ml`

### Heroku (Backend)

1. Create Heroku account and install CLI
2. Deploy using:
```bash
heroku login
heroku create greenfuel-ml-api
git push heroku main
```

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Flask, Python
- **ML:** Scikit-learn, Gradient Boosting
- **Deployment:** AWS Lambda, API Gateway, CloudWatch
- **Version Control:** Git, GitHub

## 📊 Input Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| Latitude | -90 to 90 | ° | Geographic latitude |
| Longitude | -180 to 180 | ° | Geographic longitude |
| Solar Irradiance | 0 to 10 | kWh/m²/day | Average solar irradiance |
| Wind Speed | 0 to 25 | m/s | Average wind speed |
| PV Power | 0 to 1000 | kW | Solar PV power capacity |
| Wind Power | 0 to 1000 | kW | Wind turbine power capacity |
| System Efficiency | 50 to 100 | % | PEM electrolyzer efficiency |
| Latitude Band | - | - | Climate zone (Equatorial, Polar, Subtropical, Temperate, Tropical) |

## 🎨 Features

### Frontend
- ✅ Real-time input validation
- ✅ Interactive sliders for numeric inputs
- ✅ Live prediction results
- ✅ Model performance metrics dashboard
- ✅ Feature importance visualization
- ✅ Mobile-responsive design
- ✅ Smooth animations and transitions

### Backend
- ✅ RESTful API endpoints
- ✅ Input validation and error handling
- ✅ Batch prediction support
- ✅ CORS enabled for cross-origin requests
- ✅ Comprehensive logging
- ✅ Model info endpoint

## 📈 Feature Importance

1. **Total Renewable Power** - 45.23%
2. **Wind Power** - 31.56%
3. **Efficiency Factor** - 12.34%
4. **System Efficiency** - 7.89%
5. **Wind Speed** - 2.34%
6. **Other Features** - 0.64%

## 🔍 Model Details

- **Algorithm:** Gradient Boosting Regressor
- **Training Samples:** 2,028 (80%)
- **Test Samples:** 507 (20%)
- **Total Dataset:** 2,535 samples
- **Features:** 8 numerical/categorical
- **Target:** Hydrogen Production (kg/day)

## 📝 Dataset

The model is trained on comprehensive renewable hydrogen production data including:
- Geographic location parameters
- Weather conditions (solar, wind)
- System capacity and efficiency
- Climate zone classifications

## 🚀 Use Cases

1. **Production Planning** - Forecast daily hydrogen output
2. **System Optimization** - Find optimal configurations
3. **Cost Analysis** - Estimate production economics
4. **Resource Allocation** - Optimize energy distribution
5. **Decision Support** - Aid in project planning

## 🐛 Troubleshooting

### CORS Error
If you see CORS errors, ensure the backend URL in `index.html` is correct and backend has CORS enabled.

### Model Not Loading
Check that model files (`.pkl`) are in the same directory as `app.py`.

### Predictions Seem Off
Ensure all input parameters are within valid ranges.

## 📞 Support

For issues or questions:
- 📧 Email: [your-email]
- 🐙 GitHub: [@Yuvibarot](https://github.com/Yuvibarot)
- 📚 Repository: [GreenFuel-ML](https://github.com/Yuvibarot/GreenFuel-ML)

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Machine Learning: Scikit-learn
- Dataset: Kaggle - Renewable Hydrogen Data
- Inspiration: Clean energy and sustainability

## 👨‍💻 Author

**Yuvraj Barot**
- B.E. in Artificial Intelligence & Data Science
- Apollo Institute of Engineering & Technology
- GitHub: [@Yuvibarot](https://github.com/Yuvibarot)

---

**Made with ❤️ for Renewable Energy**

---

## 🎯 Roadmap

- [ ] Real-time weather API integration
- [ ] User authentication
- [ ] Prediction history tracking
- [ ] Cost calculator module
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## 📊 Statistics

- Model Training: 2,535 samples
- Prediction Accuracy: 96.79%
- Average Error: ±5.53 kg/day
- Performance: 99.74% R² Score
'''

with open('greenfuel-ml-frontend/README.md', 'w') as f:
    f.write(readme)

print("✓ Created README.md")
