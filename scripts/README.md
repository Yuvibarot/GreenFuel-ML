# Hydrogen Energy ML Project 🔋💧

## 🧪 Abstract
Hydrogen energy stands as a sustainable alternative to fossil fuels, and efficient hydrogen production remains a key research challenge. 
This project leverages **Machine Learning (ML)** to model and optimize a **Proton Exchange Membrane (PEM) electrolyzer**, aiming to improve hydrogen generation efficiency. 
By analyzing performance parameters, the model identifies critical features and predicts optimal operating conditions for maximum output and energy efficiency.

---

## 📌 Overview
This project applies **Machine Learning (ML)** techniques to model and optimize the performance of a **PEM (Proton Exchange Membrane) electrolyzer** used in hydrogen production.  

The complete workflow covers:
- Data preprocessing  
- Feature engineering  
- Model training and validation  
- Operating condition optimization  

The goal is to enhance **hydrogen production efficiency** by identifying the most influential parameters affecting the electrolyzer’s performance.

---

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
│   ├──chart_script_1.py
│   ├──chart_script_2.py
│   ├──chart_script.py
│
│── results/
│   ├── correlation_heatmap.png
│   ├── feature_importance_voltage.png
│   ├── feature_importance_efficiency.png
│   ├── optimization_heatmap.png
│
│── README.md
│── requirements.txt
```

---

## ⚙️ Workflow

### 1. Data Preprocessing
- Cleaned and standardized PEM electrolyzer data  
- Encoded categorical variables: `Anode_Catalyst_Type`, `Cathode_Catalyst_Type`, `Membrane_Type`

### 2. Feature Engineering
- Interaction features (e.g., **Temperature × Current Density**)  
- Normalized continuous features for model stability

### 3. Model Training
- Trained **Random Forest Regressor** and **Gradient Boosting Regressor**  
- Cross-validated to avoid overfitting

### 4. Evaluation
- Metrics: **R²**, **RMSE**, **MAE**  
- Achieved **~96–97% accuracy** on unseen test data

### 5. Optimization
- Performed **grid search** over temperature and current density ranges  
- Extracted **optimal operating conditions** for highest electrolyzer efficiency

---

## 📊 Key Results
| Metric | Voltage Model | Efficiency Model |
|:-------|:--------------:|:----------------:|
| **R² Score** | 0.97 | 0.96 |
| **Most Important Features** | Current Density, Temperature | Current Density, Temperature |
| **Optimal Conditions** | 60–80 °C, 800–2000 mA/cm² | Efficiency ≈ 94.7 % |

---

## 🧠 Results Preview
| Correlation Heatmap | Feature Importance | Optimization Map |
|:--------------------:|:------------------:|:----------------:|
| ![Correlation](results/correlation_heatmap.png) | ![Importance](results/feature_importance_voltage.png) | ![Optimization](results/optimization_heatmap.png) |

---

## 🚀 How to Run

### Clone the repository
```bash
git clone https://github.com/yourusername/Hydrogen-Energy-ML-Project.git
cd Hydrogen-Energy-ML-Project
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the notebook
Open and execute the main workflow in **Google Colab** or **Jupyter Notebook**:
```bash
notebooks/main_workflow.ipynb
```
Run cells sequentially to reproduce preprocessing, training, and optimization results.

---

## 📦 Requirements
```text
pandas
numpy
matplotlib
seaborn
scikit-learn
```

---

## ✨ Author
**Yuvraj Gopalbhai Barot**  
B.E. Artificial Intelligence & Data Science  
Apollo Institute of Engineering and Technology  
Project completed under **AICTE / Edunet / Shell Internship**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yuvraj%20Barot-blue?logo=linkedin)](https://www.linkedin.com/)
[![GitHub](https://img.shields.io/badge/GitHub-YuviBarot-black?logo=github)](https://github.com/yourusername)

---

> *Hydrogen isn’t just the fuel of the future — it’s the spark of sustainable innovation today.*
