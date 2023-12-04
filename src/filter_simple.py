import pandas as pd

# Read the CSV file
file_path = '../logs/csv_files/simple_regressions/simple_regression_results_20231204_102756.csv'  # Update with the actual file path
df = pd.read_csv(file_path)

# Filter out models with high p-values
p_value_threshold = 0.05
filtered_df = df[df['P-value'] < p_value_threshold]

# (Optional) Store the names of independent variables for multicollinearity check later

# Rank models by R-squared
ranked_df = filtered_df.sort_values(by='R-squared', ascending=False)

# Select top 10 models
top_models = ranked_df.head(10)

# Save to new CSV file
output_file_path = '../logs/csv_files/simple_regressions/simple_regressions_filtered/top_simple_models.csv'  # Update with the desired file path
top_models.to_csv(output_file_path, index=False)
print(f"Top 10 models saved to {output_file_path}")
