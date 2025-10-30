
# Step 3: MODEL TRAINING - Regression models for voltage and efficiency prediction

print("=" * 80)
print("MODEL TRAINING: Predicting Cell Voltage and Energy Efficiency")
print("=" * 80)

# Prepare data for modeling
# Select input features (exclude output variables and derived metrics)
input_features = [
    'Operating_Temperature_C', 'Current_Density_mA_cm2',
    'Cathode_Pressure_bar', 'Anode_Pressure_bar',
    'Anode_Catalyst_Loading_mg_cm2', 'Cathode_Catalyst_Loading_mg_cm2',
    'Membrane_Thickness_um', 'Membrane_Water_Content_lambda',
    # Add engineered features
    'Temp_x_CurrentDensity', 'CurrentDensity_per_MembraneThickness',
    'Pressure_Differential', 'Anode_Catalyst_Activity',
    'Membrane_Resistance_Index', 'Cathode_Catalyst_Efficiency',
    'Total_Catalyst_Loading'
]

# Encode categorical features
le_anode = LabelEncoder()
le_membrane = LabelEncoder()

df_engineered['Anode_Catalyst_Type_encoded'] = le_anode.fit_transform(df_engineered['Anode_Catalyst_Type'])
df_engineered['Membrane_Type_encoded'] = le_membrane.fit_transform(df_engineered['Membrane_Type'])

input_features.extend(['Anode_Catalyst_Type_encoded', 'Membrane_Type_encoded'])

print(f"\nTotal input features: {len(input_features)}")
print("Input features:", input_features)

# Prepare feature matrix X and target variables
X = df_engineered[input_features].values

# Target 1: Cell Voltage
y_voltage = df_engineered['Cell_Voltage_V'].values

# Target 2: Energy Efficiency
y_efficiency = df_engineered['Energy_Efficiency_percent'].values

# Split data into train and test sets (80-20 split)
X_train, X_test, y_voltage_train, y_voltage_test = train_test_split(
    X, y_voltage, test_size=0.2, random_state=42
)

_, _, y_efficiency_train, y_efficiency_test = train_test_split(
    X, y_efficiency, test_size=0.2, random_state=42
)

print(f"\nTraining set size: {X_train.shape[0]} samples")
print(f"Test set size: {X_test.shape[0]} samples")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n" + "=" * 80)
print("TRAINING MODELS")
print("=" * 80)

# Model 1: Random Forest for Cell Voltage
print("\n1. Random Forest Regressor - Cell Voltage Prediction")
print("-" * 80)
rf_voltage = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
rf_voltage.fit(X_train_scaled, y_voltage_train)

# Predictions
y_voltage_pred_train = rf_voltage.predict(X_train_scaled)
y_voltage_pred_test = rf_voltage.predict(X_test_scaled)

# Metrics
print(f"Training R² Score: {r2_score(y_voltage_train, y_voltage_pred_train):.6f}")
print(f"Test R² Score: {r2_score(y_voltage_test, y_voltage_pred_test):.6f}")
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_voltage_test, y_voltage_pred_test)):.6f} V")
print(f"Test MAE: {mean_absolute_error(y_voltage_test, y_voltage_pred_test):.6f} V")

# Model 2: Gradient Boosting for Cell Voltage
print("\n2. Gradient Boosting Regressor - Cell Voltage Prediction")
print("-" * 80)
gb_voltage = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
gb_voltage.fit(X_train_scaled, y_voltage_train)

# Predictions
y_voltage_pred_gb_train = gb_voltage.predict(X_train_scaled)
y_voltage_pred_gb_test = gb_voltage.predict(X_test_scaled)

# Metrics
print(f"Training R² Score: {r2_score(y_voltage_train, y_voltage_pred_gb_train):.6f}")
print(f"Test R² Score: {r2_score(y_voltage_test, y_voltage_pred_gb_test):.6f}")
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_voltage_test, y_voltage_pred_gb_test)):.6f} V")
print(f"Test MAE: {mean_absolute_error(y_voltage_test, y_voltage_pred_gb_test):.6f} V")

# Model 3: Random Forest for Energy Efficiency
print("\n3. Random Forest Regressor - Energy Efficiency Prediction")
print("-" * 80)
rf_efficiency = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
rf_efficiency.fit(X_train_scaled, y_efficiency_train)

# Predictions
y_efficiency_pred_train = rf_efficiency.predict(X_train_scaled)
y_efficiency_pred_test = rf_efficiency.predict(X_test_scaled)

# Metrics
print(f"Training R² Score: {r2_score(y_efficiency_train, y_efficiency_pred_train):.6f}")
print(f"Test R² Score: {r2_score(y_efficiency_test, y_efficiency_pred_test):.6f}")
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_efficiency_test, y_efficiency_pred_test)):.6f} %")
print(f"Test MAE: {mean_absolute_error(y_efficiency_test, y_efficiency_pred_test):.6f} %")

# Model 4: Gradient Boosting for Energy Efficiency
print("\n4. Gradient Boosting Regressor - Energy Efficiency Prediction")
print("-" * 80)
gb_efficiency = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
gb_efficiency.fit(X_train_scaled, y_efficiency_train)

# Predictions
y_efficiency_pred_gb_train = gb_efficiency.predict(X_train_scaled)
y_efficiency_pred_gb_test = gb_efficiency.predict(X_test_scaled)

# Metrics
print(f"Training R² Score: {r2_score(y_efficiency_train, y_efficiency_pred_gb_train):.6f}")
print(f"Test R² Score: {r2_score(y_efficiency_test, y_efficiency_pred_gb_test):.6f}")
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_efficiency_test, y_efficiency_pred_gb_test)):.6f} %")
print(f"Test MAE: {mean_absolute_error(y_efficiency_test, y_efficiency_pred_gb_test):.6f} %")

print("\n" + "=" * 80)
print("✓ All models trained successfully")
print("=" * 80)
