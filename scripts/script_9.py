
# Create a summary CSV for key results
summary_data = {
    'Metric': [
        'Dataset Size',
        'Number of Features',
        'Training Samples',
        'Test Samples',
        '',
        'Voltage Model - R² Score',
        'Voltage Model - RMSE (V)',
        'Voltage Model - MAE (V)',
        '',
        'Efficiency Model - R² Score',
        'Efficiency Model - RMSE (%)',
        'Efficiency Model - MAE (%)',
        '',
        'Optimal Temperature (°C)',
        'Optimal Current Density (mA/cm²)',
        'Optimal Voltage (V)',
        'Optimal Efficiency (%)',
        'Optimal H2 Production (mL/min)',
        '',
        'Analysis Status'
    ],
    'Value': [
        '500 samples',
        '18 original + 10 engineered = 28 total',
        '400',
        '100',
        '',
        '0.9703 (97.0%)',
        '0.0486',
        '0.0390',
        '',
        '0.9649 (96.5%)',
        '1.987',
        '1.595',
        '',
        '60.00',
        '800.00',
        '1.563',
        '94.68',
        '139.30',
        '',
        'COMPLETE ✓'
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('KEY_RESULTS_SUMMARY.csv', index=False)

print("=" * 80)
print("KEY RESULTS SUMMARY")
print("=" * 80)
print(summary_df.to_string(index=False))
print("\n✓ Key results summary saved to 'KEY_RESULTS_SUMMARY.csv'")

# List all generated files
print("\n" + "=" * 80)
print("COMPLETE LIST OF GENERATED FILES")
print("=" * 80)
files_list = [
    '1. correlation_matrix.csv - Full correlation matrix',
    '2. PEM_Data_Engineered_Features.csv - Dataset with 10 new interaction features',
    '3. feature_importance_voltage.csv - Feature rankings for voltage prediction',
    '4. feature_importance_efficiency.csv - Feature rankings for efficiency prediction',
    '5. model_predictions_test_set.csv - Predictions and errors on test set',
    '6. optimal_operating_conditions.csv - Best operating parameters found',
    '7. optimization_grid_search_results.csv - All optimization results',
    '8. validation_results_detailed.csv - Detailed validation metrics',
    '9. ANALYSIS_SUMMARY_REPORT.txt - Comprehensive text report',
    '10. KEY_RESULTS_SUMMARY.csv - Summary of key findings'
]

for file in files_list:
    print(f"  {file}")

print("\n" + "=" * 80)
