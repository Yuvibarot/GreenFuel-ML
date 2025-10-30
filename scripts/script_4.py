
# Feature importance analysis
print("=" * 80)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)

# Get feature importances from Random Forest models
feature_names = input_features

# For Cell Voltage model
voltage_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf_voltage.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Features for Cell Voltage Prediction:")
print("-" * 80)
print(voltage_importance.head(10).to_string(index=False))

# For Energy Efficiency model
efficiency_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf_efficiency.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n\nTop 10 Features for Energy Efficiency Prediction:")
print("-" * 80)
print(efficiency_importance.head(10).to_string(index=False))

# Save feature importance
voltage_importance.to_csv('feature_importance_voltage.csv', index=False)
efficiency_importance.to_csv('feature_importance_efficiency.csv', index=False)

print("\n✓ Feature importance saved")

# Create predictions dataframe for validation
results_df = pd.DataFrame({
    'Actual_Voltage': y_voltage_test,
    'Predicted_Voltage_RF': y_voltage_pred_test,
    'Predicted_Voltage_GB': y_voltage_pred_gb_test,
    'Actual_Efficiency': y_efficiency_test,
    'Predicted_Efficiency_RF': y_efficiency_pred_test,
    'Predicted_Efficiency_GB': y_efficiency_pred_gb_test
})

# Calculate prediction errors
results_df['Voltage_Error_RF'] = results_df['Actual_Voltage'] - results_df['Predicted_Voltage_RF']
results_df['Voltage_Error_GB'] = results_df['Actual_Voltage'] - results_df['Predicted_Voltage_GB']
results_df['Efficiency_Error_RF'] = results_df['Actual_Efficiency'] - results_df['Predicted_Efficiency_RF']
results_df['Efficiency_Error_GB'] = results_df['Actual_Efficiency'] - results_df['Predicted_Efficiency_GB']

results_df.to_csv('model_predictions_test_set.csv', index=False)
print("✓ Test set predictions saved to 'model_predictions_test_set.csv'")
