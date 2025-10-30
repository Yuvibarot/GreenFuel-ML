# Hydrogen Energy ML Project 🔋💧

## 📌 Overview
This project applies Machine Learning (ML) techniques to model and optimize the performance of a **PEM (Proton Exchange Membrane) electrolyzer** for hydrogen production. The workflow includes data preprocessing, feature engineering, model training, evaluation, and optimization of operating conditions for efficient hydrogen generation.

## 📂 Repository Structure
```
Hydrogen-Energy-ML-Project/
│── data/                     # Datasets and results
│   ├── PEM_Data_Engineered_Features.csv
│   ├── correlation_matrix.csv
│   ├── feature_importance_voltage.csv
│   ├── feature_importance_efficiency.csv
│   ├── model_predictions_test_set.csv
│   ├── validation_results_detailed.csv
│   ├── optimization_grid_search_results.csv
│   ├── Optimization Results.csv
│   ├── optimal_operating_conditions.csv
│   ├── KEY_RESULTS_SUMMARY.csv
│
│── notebooks/
│   ├── main_workflow.ipynb        # End-to-end pipeline (Colab-ready)
│
│── scripts/
│   ├── script_1.py
│   ├── script_2.py
│   ├── script_3.py
│   ├── script_4.py
│   ├── script_5.py
│   ├── script_6.py
│   ├── script_7.py
│   ├── script_8.py
│   ├── script_9.py
│   ├── script.py
│   ├── chart_script_1.py
│   ├── chart_script_2.py
│   ├── chart_script.py
│
│── results/
│   ├── correlation_heatmap.png
│   ├── chart_1.png
│   ├── chart.png
│   ├── ANALYSIS_SUMMARY_REPORT.txt
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
**1. **Clone the repository**
```bash
   git clone https://github.com/Yuvibarot/GreenFuel-ML.git
   cd GreenFuel-ML
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
