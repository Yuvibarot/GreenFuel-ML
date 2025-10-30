
# Step 4: OPTIMIZATION - Find best operating conditions

print("=" * 80)
print("OPTIMIZATION: Finding Best Operating Conditions")
print("=" * 80)

# Define objective function to maximize efficiency (minimize negative efficiency)
def objective_function(params):
    """
    Objective: Maximize energy efficiency while maintaining reasonable H2 production
    """
    # Unpack parameters
    temp = params[0]
    current_density = params[1]
    cathode_pressure = params[2]
    anode_pressure = params[3]
    anode_loading = params[4]
    cathode_loading = params[5]
    membrane_thickness = params[6]
    water_content = params[7]
    anode_type = int(round(params[8]))  # Categorical
    membrane_type = int(round(params[9]))  # Categorical
    
    # Calculate engineered features
    temp_x_current = temp * current_density
    current_per_thickness = current_density / membrane_thickness
    pressure_diff = cathode_pressure - anode_pressure
    anode_activity = anode_loading * np.exp(temp / 100)
    membrane_resistance = membrane_thickness / water_content
    cathode_efficiency = cathode_loading * cathode_pressure
    total_catalyst = anode_loading + cathode_loading
    
    # Create feature vector
    features = np.array([[
        temp, current_density, cathode_pressure, anode_pressure,
        anode_loading, cathode_loading, membrane_thickness, water_content,
        temp_x_current, current_per_thickness, pressure_diff,
        anode_activity, membrane_resistance, cathode_efficiency,
        total_catalyst, anode_type, membrane_type
    ]])
    
    # Scale features
    features_scaled = scaler.transform(features)
    
    # Predict efficiency and voltage
    efficiency = rf_efficiency.predict(features_scaled)[0]
    voltage = rf_voltage.predict(features_scaled)[0]
    
    # Multi-objective: maximize efficiency, minimize voltage, ensure production
    # Weighted objective: 70% efficiency, 20% low voltage, 10% high production
    h2_production = current_density * 0.17412  # Approximate production rate
    
    # Constraints: voltage should be reasonable (1.5-2.5V), efficiency > 65%
    penalty = 0
    if voltage < 1.5 or voltage > 2.5:
        penalty += 1000
    if efficiency < 65:
        penalty += 1000
    
    # Minimize negative efficiency (to maximize efficiency)
    objective = -efficiency + 0.2 * voltage - 0.001 * h2_production + penalty
    
    return objective

# Define bounds for optimization
# [temp, current_density, cathode_p, anode_p, anode_loading, cathode_loading, 
#  membrane_thickness, water_content, anode_type_code, membrane_type_code]
bounds = [
    (50, 80),      # Operating_Temperature_C (optimal range)
    (500, 4000),   # Current_Density_mA_cm2 (practical range)
    (10, 30),      # Cathode_Pressure_bar
    (1, 4),        # Anode_Pressure_bar
    (0.5, 2.5),    # Anode_Catalyst_Loading_mg_cm2
    (0.05, 0.2),   # Cathode_Catalyst_Loading_mg_cm2
    (50, 180),     # Membrane_Thickness_um
    (18, 24),      # Membrane_Water_Content_lambda
    (0, 2),        # Anode_Catalyst_Type_encoded (0=Ir_black, 1=IrO2, 2=IrRuOx)
    (0, 2)         # Membrane_Type_encoded (0=Nafion_115, 1=Nafion_117, 2=Nafion_212)
]

print("\nRunning optimization (this may take a moment)...")
print("-" * 80)

# Initial guess (near typical industrial conditions)
x0 = [70, 2000, 20, 2, 1.5, 0.1, 50, 22, 1, 2]

# Run optimization
result = minimize(
    objective_function,
    x0,
    method='L-BFGS-B',
    bounds=bounds,
    options={'maxiter': 1000}
)

if result.success:
    optimal_params = result.x
    print("\n✓ Optimization Successful!")
    print("=" * 80)
    print("OPTIMAL OPERATING CONDITIONS")
    print("=" * 80)
    
    # Decode categorical variables
    anode_types = ['Ir_black', 'IrO2', 'IrRuOx']
    membrane_types = ['Nafion_115', 'Nafion_117', 'Nafion_212']
    
    optimal_conditions = {
        'Operating_Temperature_C': optimal_params[0],
        'Current_Density_mA_cm2': optimal_params[1],
        'Cathode_Pressure_bar': optimal_params[2],
        'Anode_Pressure_bar': optimal_params[3],
        'Anode_Catalyst_Loading_mg_cm2': optimal_params[4],
        'Cathode_Catalyst_Loading_mg_cm2': optimal_params[5],
        'Membrane_Thickness_um': optimal_params[6],
        'Membrane_Water_Content_lambda': optimal_params[7],
        'Anode_Catalyst_Type': anode_types[int(round(optimal_params[8]))],
        'Membrane_Type': membrane_types[int(round(optimal_params[9]))]
    }
    
    for param, value in optimal_conditions.items():
        if isinstance(value, float):
            print(f"{param:40}: {value:10.2f}")
        else:
            print(f"{param:40}: {value:>10}")
    
    # Predict performance with optimal conditions
    temp_x_current = optimal_params[0] * optimal_params[1]
    current_per_thickness = optimal_params[1] / optimal_params[6]
    pressure_diff = optimal_params[2] - optimal_params[3]
    anode_activity = optimal_params[4] * np.exp(optimal_params[0] / 100)
    membrane_resistance = optimal_params[6] / optimal_params[7]
    cathode_efficiency = optimal_params[5] * optimal_params[2]
    total_catalyst = optimal_params[4] + optimal_params[5]
    
    optimal_features = np.array([[
        optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3],
        optimal_params[4], optimal_params[5], optimal_params[6], optimal_params[7],
        temp_x_current, current_per_thickness, pressure_diff,
        anode_activity, membrane_resistance, cathode_efficiency,
        total_catalyst, int(round(optimal_params[8])), int(round(optimal_params[9]))
    ]])
    
    optimal_features_scaled = scaler.transform(optimal_features)
    
    predicted_voltage = rf_voltage.predict(optimal_features_scaled)[0]
    predicted_efficiency = rf_efficiency.predict(optimal_features_scaled)[0]
    predicted_h2_production = optimal_params[1] * 0.17412  # mL/min
    
    print("\n" + "=" * 80)
    print("PREDICTED PERFORMANCE AT OPTIMAL CONDITIONS")
    print("=" * 80)
    print(f"{'Cell Voltage':40}: {predicted_voltage:10.3f} V")
    print(f"{'Energy Efficiency':40}: {predicted_efficiency:10.2f} %")
    print(f"{'H2 Production Rate (approx.)':40}: {predicted_h2_production:10.2f} mL/min")
    print(f"{'H2 Production Rate (approx.)':40}: {predicted_h2_production*0.06:10.2f} NL/h")
    
    # Save optimal conditions
    optimal_df = pd.DataFrame([optimal_conditions])
    optimal_df['Predicted_Voltage_V'] = predicted_voltage
    optimal_df['Predicted_Efficiency_percent'] = predicted_efficiency
    optimal_df['Predicted_H2_mL_min'] = predicted_h2_production
    optimal_df.to_csv('optimal_operating_conditions.csv', index=False)
    
    print("\n✓ Optimal conditions saved to 'optimal_operating_conditions.csv'")
    
else:
    print("\n✗ Optimization failed:", result.message)
