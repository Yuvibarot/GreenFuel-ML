# Hydrogen Energy ML Project 🔋💧

## 📌 Overview
This project applies Machine Learning (ML) techniques to model and optimize the performance of a **PEM (Proton Exchange Membrane) electrolyzer** for hydrogen production. The workflow includes data preprocessing, feature engineering, model training, evaluation, and optimization of operating conditions for efficient hydrogen generation.

## 📂 Repository Structure
```
Hydrogen-Energy-ML-Project/
│── data/
│   ├── Summary/
│   │   ├──KEY_RESULTS_SUMMARY.csv 
│   ├── Optimization/
│   │   ├──optimal_operating_conditions.csv
│   │   ├──Optimization Results.csv
│   │   ├──optimization_grid_search_results.csv
│   ├── Processed
│   │   ├──correlation_matrix.csv
│   │   ├──feature_importance_efficiency.csv
│   │   ├──feature_importance_voltage.csv
│   │   ├──model_predictions_test_set.csv
│   │   ├──validation_results_detailed.csv
│   ├── Raw
│   │   ├── PEM_Data_Engineered_Features.csv
│
│── week 1 task/
│   ├── Data_Cleaning_Preprocessing_Renewable_Hydrogen.ipynb
│   ├──Data_Cleaning_Report.txt
│   ├──Renewable_Hydrogen_Data_CLEANED.csv
│   ├──Renewable_Hydrogen_Data_RAW.csv
│   
│── week 2 task/
│   ├──ML_Model_Evaluation_Results.csv
│   ├──ml_model_performance.png
│   ├──ML_Model_Summary_Report.txt
│   ├──ML Prediction Model Hydrogen Production.ipynb
│   ├──PROJECT_SUMMARY.txt
│
│── README.md
│── requirements.txt
```

## ⚙️ Workflow
### 1. Data Preprocessing
- Cleaned raw PEM electrolyzer data
- Encoded categorical variables: *Anode_Catalyst_Type, Cathode_Catalyst_Type, Membrane_Type*

### 2. Feature Engineering
- Added interaction terms (e.g., Temp × Current Density)
- Normalized key parameters

### 3. Model Training
- Used **Random Forest Regressor** and **Gradient Boosting Regressor**

### 4. Evaluation
- Metrics: R², RMSE, MAE
- Achieved ~96–97% accuracy on test data

### 5. Optimization
- Grid search across temperature & current density
- Identified optimal operating conditions for high efficiency

## 📊 Key Results
- **Voltage Model Accuracy:** R² ≈ 0.97  
- **Efficiency Model Accuracy:** R² ≈ 0.96  
- **Top Features:** Current Density, Operating Temperature  
- **Optimal Conditions:** ~60–80 °C, 800–2000 mA/cm² → Efficiency up to ~94.7%  

## 🚀 How to Run
**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/Hydrogen-Energy-ML-Project.git
cd Hydrogen-Energy-ML-Project
```
**2. Install dependencies:**
```bash
pip install -r requirements.txt
```
**3. Open the notebook:**
```bash
notebooks/main_workflow.ipynb
```
Run cells step by step to reproduce results.

## 📦 Requirements
- pandas  
- numpy  
- matplotlib  
- seaborn  
- scikit-learn  

## ✨ Author
**Yuvraj G. Barot**  
B.E. Artificial Intelligence & Data Science  
Apollo Institute of Engineering and Technology  
Project completed under **AICTE / Edunet / Shell Internship**

[LinkedIn](https://www.linkedin.com/in/yuvraj-barot-59a1512b1)  
[GitHub](https://github.com/Yuvibarot/GreenFuel-ML)
