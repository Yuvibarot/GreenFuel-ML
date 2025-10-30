import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import r2_score

# Load the data
df = pd.read_csv('model_predictions_test_set.csv')

# Calculate R² score for Cell Voltage
r2_voltage = r2_score(df['Actual_Voltage'], df['Predicted_Voltage_RF'])

# Calculate absolute error for coloring
df['abs_voltage_error'] = np.abs(df['Voltage_Error_RF'])

# Create scatter plot for Cell Voltage
fig = px.scatter(df, 
                x='Actual_Voltage', 
                y='Predicted_Voltage_RF',
                color='abs_voltage_error',
                color_continuous_scale='plasma',
                labels={
                    'Actual_Voltage': 'Actual Volt',
                    'Predicted_Voltage_RF': 'Predicted Volt',
                    'abs_voltage_error': 'Error Mag'
                },
                title='Model Prediction Accuracy - Random Forest')

# Add diagonal line (y=x) for perfect predictions
min_val = min(df['Actual_Voltage'].min(), df['Predicted_Voltage_RF'].min())
max_val = max(df['Actual_Voltage'].max(), df['Predicted_Voltage_RF'].max())

fig.add_trace(go.Scatter(
    x=[min_val, max_val],
    y=[min_val, max_val],
    mode='lines',
    line=dict(color='red', dash='dash', width=2),
    name='Perfect Pred',
    showlegend=True
))

# Update traces for better visibility
fig.update_traces(cliponaxis=False)

# Update layout
fig.update_layout(
    coloraxis_colorbar_title="Error Mag",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Add R² annotation to the plot
fig.add_annotation(
    text=f'R² = {r2_voltage:.3f}',
    xref="paper", yref="paper",
    x=0.02, y=0.98,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12),
    bgcolor="white",
    bordercolor="black",
    borderwidth=1
)

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

print("Chart created successfully!")
print(f"R² Score for Cell Voltage: {r2_voltage:.4f}")