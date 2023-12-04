import pandas as pd
import statsmodels.api as sm
import os
from datetime import datetime

def read_data(file_name):
    df = pd.read_excel(file_name)
    df.fillna(0, inplace=True)  # Replace missing values with 0
    return df

def run_simple_regressions(df, dependent_var):
    independent_vars = [var for var in df.columns if var != dependent_var and var != 'Date']
    simple_regression_results = []

    for var in independent_vars:
        X = df[var]
        y = df[dependent_var]

        # Convert to numeric and handle missing values
        X = pd.to_numeric(X, errors='coerce')
        X.fillna(0, inplace=True)  # or use another method to handle missing values
        y.fillna(0, inplace=True)

        # Reshape X if it's a Series
        if len(X.shape) == 1:
            X = X.values.reshape(-1, 1)

        X = sm.add_constant(X)  # Add a constant
        model = sm.OLS(y, X).fit()

        simple_regression_results.append({
            'Independent Variable': var,
            'R-squared': model.rsquared,
            'P-value': model.pvalues.iloc[1] if len(model.pvalues) > 1 else np.nan,  # p-value for the variable, handle single-variable case
            'Standard Error': model.bse.iloc[1] if len(model.bse) > 1 else np.nan  # standard error for the variable, handle single-variable case
        })

    
    return simple_regression_results


# Example Usage
file_name = '../data/data.xlsx'  # Update the file path if needed
df = read_data(file_name)


results = run_simple_regressions(df, 'CSUSHPINSA')  # Replace with the name of your dependent variable

# Save the results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f"../logs/csv_files/simple_regressions/simple_regression_results_{timestamp}.csv"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

pd.DataFrame(results).to_csv(output_file_path, index=False)
print(f"Results saved to {output_file_path}")

