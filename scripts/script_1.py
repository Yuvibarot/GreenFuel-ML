
# Step 1: DATA EXPLORATION - Analyze correlations between parameters

# Select numerical columns for correlation analysis
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Calculate correlation matrix
correlation_matrix = df[numerical_cols].corr()

# Display correlations with Cell_Voltage_V (our primary target)
print("=" * 80)
print("CORRELATIONS WITH CELL VOLTAGE (Primary Target)")
print("=" * 80)
voltage_correlations = correlation_matrix['Cell_Voltage_V'].sort_values(ascending=False)
print(voltage_correlations)

print("\n" + "=" * 80)
print("CORRELATIONS WITH ENERGY EFFICIENCY (Secondary Target)")
print("=" * 80)
efficiency_correlations = correlation_matrix['Energy_Efficiency_percent'].sort_values(ascending=False)
print(efficiency_correlations)

# Key parameter relationships
print("\n" + "=" * 80)
print("KEY PARAMETER RELATIONSHIPS")
print("=" * 80)

key_pairs = [
    ('Current_Density_mA_cm2', 'Cell_Voltage_V'),
    ('Operating_Temperature_C', 'Cell_Voltage_V'),
    ('Current_Density_mA_cm2', 'H2_Production_Rate_mL_min'),
    ('Membrane_Thickness_um', 'Cell_Voltage_V'),
    ('Anode_Catalyst_Loading_mg_cm2', 'Cell_Voltage_V'),
    ('Cell_Voltage_V', 'Energy_Efficiency_percent')
]

for param1, param2 in key_pairs:
    corr = correlation_matrix.loc[param1, param2]
    print(f"{param1:40} <-> {param2:40}: {corr:7.4f}")

# Save correlation matrix to CSV for later use
correlation_matrix.to_csv('correlation_matrix.csv')
print("\n✓ Correlation matrix saved to 'correlation_matrix.csv'")
