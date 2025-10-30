
# Step 2: FEATURE ENGINEERING - Create interaction terms

print("=" * 80)
print("FEATURE ENGINEERING: Creating Interaction Terms")
print("=" * 80)

# Create a copy of the dataframe for feature engineering
df_engineered = df.copy()

# 1. Temperature × Current Density (affects voltage through combined thermal and electrochemical effects)
df_engineered['Temp_x_CurrentDensity'] = (
    df_engineered['Operating_Temperature_C'] * 
    df_engineered['Current_Density_mA_cm2']
)
print("✓ Created: Temp_x_CurrentDensity")

# 2. Current Density / Membrane Thickness (ohmic resistance effect)
df_engineered['CurrentDensity_per_MembraneThickness'] = (
    df_engineered['Current_Density_mA_cm2'] / 
    df_engineered['Membrane_Thickness_um']
)
print("✓ Created: CurrentDensity_per_MembraneThickness")

# 3. Pressure Differential (Cathode - Anode)
df_engineered['Pressure_Differential'] = (
    df_engineered['Cathode_Pressure_bar'] - 
    df_engineered['Anode_Pressure_bar']
)
print("✓ Created: Pressure_Differential")

# 4. Catalyst Activity Index (anode loading × temperature effect)
df_engineered['Anode_Catalyst_Activity'] = (
    df_engineered['Anode_Catalyst_Loading_mg_cm2'] * 
    np.exp(df_engineered['Operating_Temperature_C'] / 100)
)
print("✓ Created: Anode_Catalyst_Activity")

# 5. Membrane Resistance Index (thickness / water content)
df_engineered['Membrane_Resistance_Index'] = (
    df_engineered['Membrane_Thickness_um'] / 
    df_engineered['Membrane_Water_Content_lambda']
)
print("✓ Created: Membrane_Resistance_Index")

# 6. Power per unit temperature (efficiency indicator)
df_engineered['Power_per_Temperature'] = (
    df_engineered['Power_Density_W_cm2'] / 
    df_engineered['Operating_Temperature_C']
)
print("✓ Created: Power_per_Temperature")

# 7. Cathode catalyst efficiency (loading × pressure)
df_engineered['Cathode_Catalyst_Efficiency'] = (
    df_engineered['Cathode_Catalyst_Loading_mg_cm2'] * 
    df_engineered['Cathode_Pressure_bar']
)
print("✓ Created: Cathode_Catalyst_Efficiency")

# 8. Temperature-normalized voltage
df_engineered['Voltage_per_Temperature'] = (
    df_engineered['Cell_Voltage_V'] / 
    df_engineered['Operating_Temperature_C']
)
print("✓ Created: Voltage_per_Temperature")

# 9. Current efficiency (H2 production rate / current density)
df_engineered['Current_Efficiency'] = (
    df_engineered['H2_Production_Rate_mL_min'] / 
    df_engineered['Current_Density_mA_cm2']
)
print("✓ Created: Current_Efficiency")

# 10. Total catalyst loading
df_engineered['Total_Catalyst_Loading'] = (
    df_engineered['Anode_Catalyst_Loading_mg_cm2'] + 
    df_engineered['Cathode_Catalyst_Loading_mg_cm2']
)
print("✓ Created: Total_Catalyst_Loading")

print("\n" + "=" * 80)
print(f"Total features after engineering: {df_engineered.shape[1]}")
print(f"New interaction features created: {df_engineered.shape[1] - df.shape[1]}")
print("=" * 80)

# Display statistics for new features
print("\nStatistics for New Interaction Features:")
print("-" * 80)
new_features = [
    'Temp_x_CurrentDensity', 'CurrentDensity_per_MembraneThickness',
    'Pressure_Differential', 'Anode_Catalyst_Activity',
    'Membrane_Resistance_Index', 'Power_per_Temperature',
    'Cathode_Catalyst_Efficiency', 'Voltage_per_Temperature',
    'Current_Efficiency', 'Total_Catalyst_Loading'
]
print(df_engineered[new_features].describe())

# Save engineered dataset
df_engineered.to_csv('PEM_Data_Engineered_Features.csv', index=False)
print("\n✓ Engineered dataset saved to 'PEM_Data_Engineered_Features.csv'")
