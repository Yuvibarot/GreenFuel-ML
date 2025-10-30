import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load the data
df = pd.read_csv('PEM_Electrolyzer_Operating_Parameters.csv')

# Select the key parameters for correlation analysis
key_params = [
    'Operating_Temperature_C',
    'Current_Density_mA_cm2',
    'Cell_Voltage_V',
    'Cathode_Pressure_bar',
    'Anode_Pressure_bar',
    'Membrane_Thickness_um',
    'Power_Density_W_cm2',
    'H2_Production_Rate_mL_min',
    'Energy_Efficiency_percent'
]

# Create subset with key parameters
df_subset = df[key_params]

# Calculate correlation matrix
corr_matrix = df_subset.corr()

# Create abbreviated labels for display (15 char limit)
label_mapping = {
    'Operating_Temperature_C': 'Temp (°C)',
    'Current_Density_mA_cm2': 'Current Dens',
    'Cell_Voltage_V': 'Cell Volt (V)',
    'Cathode_Pressure_bar': 'Cathode Pres',
    'Anode_Pressure_bar': 'Anode Pres',
    'Membrane_Thickness_um': 'Membrane Th',
    'Power_Density_W_cm2': 'Power Dens',
    'H2_Production_Rate_mL_min': 'H2 Prod Rate',
    'Energy_Efficiency_percent': 'Energy Eff'
}

# Rename index and columns
corr_matrix.index = [label_mapping[col] for col in corr_matrix.index]
corr_matrix.columns = [label_mapping[col] for col in corr_matrix.columns]

# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.index,
    colorscale='RdBu_r',
    zmid=0,
    zmin=-1,
    zmax=1,
    text=np.round(corr_matrix.values, 2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(
        title="Correlation"
    )
))

# Update layout
fig.update_layout(
    title="PEM Electrolyzer: Parameter Corr Matrix",
    xaxis_title="",
    yaxis_title="",
    font=dict(size=12)
)

# Rotate x-axis labels for readability
fig.update_xaxes(tickangle=45)

# Save as both PNG and SVG
fig.write_image("correlation_heatmap.png")
fig.write_image("correlation_heatmap.svg", format="svg")

print("Correlation heatmap created successfully!")
print(f"Correlation matrix shape: {corr_matrix.shape}")