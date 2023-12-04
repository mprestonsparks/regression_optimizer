# import pandas as pd
# import numpy as np
# from statsmodels.stats.outliers_influence import variance_inflation_factor

# # Function to calculate VIF
# def calculate_vif(data, independent_vars):
#     # Ensure data only contains the independent variables
#     data = data[independent_vars]
#     vif_data = pd.DataFrame()
#     vif_data["Variable"] = independent_vars
#     # Calculate VIF for each independent variable
#     vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(len(independent_vars))]
#     return vif_data

# # Read the CSV file containing the simple regression results
# simple_results_file_path = '../logs/csv_files/simple_regressions/simple_regression_results_20231203_182034.csv'
# simple_results_df = pd.read_csv(simple_results_file_path)

# # Assuming 'Independent Variable' is the column with your variable names
# independent_vars = simple_results_df['Independent Variable'].tolist()

# # Load the original dataset
# original_df = pd.read_excel('../data/data.xlsx')

# # Convert 'N/A' to NaN to use interpolation
# original_df.replace("N/A", np.nan, inplace=True)

# # Use interpolation to fill NaN values
# original_df.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
# original_df.interpolate(method='linear', limit_direction='backward', axis=0, inplace=True)

# # ... rest of the code remains the same ...


# # Exclude the 'YYYY-MM' column and dependent variable column from the VIF calculation
# if 'YYYY-MM' in original_df.columns:
#     original_df = original_df.drop(columns=['YYYY-MM'])
# # Assuming the dependent variable is the second column, drop it as well
# original_df = original_df.drop(original_df.columns[1], axis=1)

# # Update the list of independent variables to match the columns in the DataFrame
# independent_vars = original_df.columns.tolist()

# # Perform the VIF calculation on numeric independent variables only
# vif_df = calculate_vif(original_df, independent_vars)

# # Print the VIF DataFrame
# print("VIF DataFrame:")
# print(vif_df)



import pandas as pd

# Read the CSV file containing complex regression results
file_path = '../logs/csv_files/combination_regressions/combination_regression_results_20231204_103038.csv'  # Update with the actual file path
df = pd.read_csv(file_path)

# Filter out models with high p-values
p_value_threshold = 0.05
filtered_df = df[df['P-value'] < p_value_threshold]

# Rank models by Adjusted R-squared
ranked_df = filtered_df.sort_values(by='Adj. R-squared', ascending=False)

# Select top 10 models
top_models = ranked_df.head(10)

# Save to new CSV file
output_file_path = '../logs/csv_files/combination_regressions/combination_regressions_filtered/top_combination_models.csv'  # Update with the desired file path
top_models.to_csv(output_file_path, index=False)
print(f"Top 10 models saved to {output_file_path}")
