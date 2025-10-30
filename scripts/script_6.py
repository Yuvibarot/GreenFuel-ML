
# Try optimization with a different approach - grid search for key parameters
print("=" * 80)
print("OPTIMIZATION: Alternative Approach - Grid Search")
print("=" * 80)

# Create a grid of operating conditions focusing on key parameters
print("\nTesting combinations of key parameters...")

# Define ranges for key parameters
temps = np.linspace(60, 80, 5)
current_densities = np.linspace(800, 2500, 10)

best_efficiency = 0
best_conditions = None
best_voltage = 0
best_h2_production = 0

results_list = []

for temp in temps:
    for current_density in current_densities:
        # Fixed reasonable values for other parameters
        cathode_pressure = 25  # High pressure for efficiency
        anode_pressure = 2
        anode_loading = 1.2  # Moderate loading
        cathode_loading = 0.08  # Standard loading
        membrane_thickness = 50  # Thin membrane (Nafion 212)
        water_content = 22  # Well hydrated
        anode_type = 1  # IrO2 (most common)
        membrane_type = 2  # Nafion 212 (thinnest)
        
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
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        efficiency = rf_efficiency.predict(features_scaled)[0]
        voltage = rf_voltage.predict(features_scaled)[0]
        h2_production = current_density * 0.17412
        
        results_list.append({
            'Temperature_C': temp,
            'Current_Density_mA_cm2': current_density,
            'Voltage_V': voltage,
            'Efficiency_percent': efficiency,
            'H2_Production_mL_min': h2_production
        })
        
        # Track best efficiency
        if efficiency > best_efficiency and 1.5 <= voltage <= 2.5:
            best_efficiency = efficiency
            best_conditions = {
                'Operating_Temperature_C': temp,
                'Current_Density_mA_cm2': current_density,
                'Cathode_Pressure_bar': cathode_pressure,
                'Anode_Pressure_bar': anode_pressure,
                'Anode_Catalyst_Loading_mg_cm2': anode_loading,
                'Cathode_Catalyst_Loading_mg_cm2': cathode_loading,
                'Membrane_Thickness_um': membrane_thickness,
                'Membrane_Water_Content_lambda': water_content,
                'Anode_Catalyst_Type': 'IrO2',
                'Membrane_Type': 'Nafion_212'
            }
            best_voltage = voltage
            best_h2_production = h2_production

print("\n✓ Grid search completed!")
print("=" * 80)
print("OPTIMAL OPERATING CONDITIONS (from Grid Search)")
print("=" * 80)

for param, value in best_conditions.items():
    if isinstance(value, float):
        print(f"{param:40}: {value:10.2f}")
    else:
        print(f"{param:40}: {value:>10}")

print("\n" + "=" * 80)
print("PREDICTED PERFORMANCE AT OPTIMAL CONDITIONS")
print("=" * 80)
print(f"{'Cell Voltage':40}: {best_voltage:10.3f} V")
print(f"{'Energy Efficiency':40}: {best_efficiency:10.2f} %")
print(f"{'H2 Production Rate':40}: {best_h2_production:10.2f} mL/min")
print(f"{'H2 Production Rate':40}: {best_h2_production*0.06:10.2f} NL/h")

# Save optimization results
optimization_results = pd.DataFrame(results_list)
optimization_results.to_csv('optimization_grid_search_results.csv', index=False)

# Save best conditions
best_conditions_df = pd.DataFrame([best_conditions])
best_conditions_df['Predicted_Voltage_V'] = best_voltage
best_conditions_df['Predicted_Efficiency_percent'] = best_efficiency
best_conditions_df['Predicted_H2_mL_min'] = best_h2_production
best_conditions_df.to_csv('optimal_operating_conditions.csv', index=False)

print("\n✓ Optimization results saved to 'optimization_grid_search_results.csv'")
print("✓ Optimal conditions saved to 'optimal_operating_conditions.csv'")

# Compare with actual dataset
print("\n" + "=" * 80)
print("COMPARISON WITH ACTUAL DATA")
print("=" * 80)
print(f"{'Metric':40} {'Optimal (Predicted)':>20} {'Dataset Best':>20}")
print("-" * 80)
print(f"{'Maximum Efficiency (%)':40} {best_efficiency:>20.2f} {df['Energy_Efficiency_percent'].max():>20.2f}")
print(f"{'Minimum Voltage at High Eff (V)':40} {best_voltage:>20.3f} {df[df['Energy_Efficiency_percent'] > 90]['Cell_Voltage_V'].min():>20.3f}")
