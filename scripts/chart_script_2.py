import pandas as pd
import plotly.graph_objects as go

# Load voltage feature importance data
try:
    df_voltage = pd.read_csv('feature_importance_voltage.csv')
    print("Voltage data loaded successfully")
except FileNotFoundError:
    print("feature_importance_voltage.csv not found")
    df_voltage = pd.DataFrame({'Feature': [], 'Importance': []})

# Load efficiency feature importance data  
try:
    df_efficiency = pd.read_csv('feature_importance_efficiency.csv')
    print("Efficiency data loaded successfully")
except FileNotFoundError:
    print("feature_importance_efficiency.csv not found")
    df_efficiency = pd.DataFrame({'Feature': [], 'Importance': []})

# Get top 10 features for each model and sort by importance
df_voltage_top = df_voltage.nlargest(10, 'Importance').sort_values('Importance', ascending=True).copy()
df_efficiency_top = df_efficiency.nlargest(10, 'Importance').sort_values('Importance', ascending=True).copy()

# Abbreviate feature names to meet 15 character limit
def abbreviate_feature_name(name):
    name = str(name)
    # Common abbreviations
    abbrevs = {
        'Current_Density_mA_cm2': 'Curr_Density',
        'Operating_Temperature_C': 'Op_Temp',
        'Temperature': 'Temp',
        'Anode_Pressure_bar': 'Anode_Press',
        'Cathode_Pressure_bar': 'Cath_Press', 
        'Membrane_Thickness_um': 'Membr_Thick',
        'Water_Flow_Rate': 'Water_Flow',
        'Cell_Area_cm2': 'Cell_Area',
        'Catalyst_Loading': 'Catalyst_Ld',
        'CurrentDensity_per_MembraneThickness': 'CD_per_MT',
        'Temp_x_CurrentDensity': 'Temp_x_CD',
        'Pressure_Difference': 'Press_Diff',
        'Flow_Rate_per_Area': 'Flow_per_Area'
    }
    
    for full, abbrev in abbrevs.items():
        name = name.replace(full, abbrev)
    
    # Truncate to 15 characters if still too long
    return name[:15]

df_voltage_top['Feature_Short'] = df_voltage_top['Feature'].apply(abbreviate_feature_name)
df_efficiency_top['Feature_Short'] = df_efficiency_top['Feature'].apply(abbreviate_feature_name)

# Create combined dataset with model prefixes for y-axis
voltage_features = []
efficiency_features = []

for i, row in df_voltage_top.iterrows():
    voltage_features.append(f"V: {row['Feature_Short']}")
    
for i, row in df_efficiency_top.iterrows():
    efficiency_features.append(f"E: {row['Feature_Short']}")

# Combine all features with a separator
all_features = efficiency_features + [''] + voltage_features
all_importance = (df_efficiency_top['Importance'].tolist() + 
                 [0] + 
                 df_voltage_top['Importance'].tolist())

# Create colors list - orange for efficiency, spacer, cyan for voltage  
colors = (['#DB4545'] * len(efficiency_features) + 
          ['white'] + 
          ['#1FB8CD'] * len(voltage_features))

# Create the chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=all_importance,
    y=all_features,
    orientation='h',
    marker_color=colors,
    text=[f'{val:.1%}' if val > 0 else '' for val in all_importance],
    textposition='auto',
    showlegend=False
))

# Update layout
fig.update_layout(
    title='RF Feature Importance Analysis',
    xaxis_title='Importance',
    yaxis_title='Features (V=Voltage, E=Efficiency)',
    showlegend=False
)

# Update traces
fig.update_traces(cliponaxis=False)

# Format x-axis as percentage
fig.update_xaxes(tickformat='.1%')

# Add annotations to separate sections
fig.add_annotation(
    x=0, y=len(efficiency_features) + 1,
    text="Voltage Model",
    showarrow=False,
    font=dict(size=12, color='#1FB8CD'),
    xanchor='left'
)

fig.add_annotation(
    x=0, y=len(efficiency_features)/2 - 1,
    text="Efficiency Model", 
    showarrow=False,
    font=dict(size=12, color='#DB4545'),
    xanchor='left'
)

# Save the chart
fig.write_image('chart.png')
fig.write_image('chart.svg', format='svg')

print("Feature importance chart saved successfully")
print(f"Voltage features: {len(df_voltage_top)}")
print(f"Efficiency features: {len(df_efficiency_top)}")
print("Top voltage features:", df_voltage_top['Feature'].head(3).tolist())
print("Top efficiency features:", df_efficiency_top['Feature'].head(3).tolist())