import pandas as pd
import statsmodels.api as sm
import itertools
import os
from datetime import datetime

def read_data(file_name):
    df = pd.read_excel(file_name)
    df.fillna(0, inplace=True)  # Replace missing values with 0
    return df

def generate_combinations(variables, max_length):
    return list(itertools.combinations(variables, max_length))

def create_interactions(df, combo):
    interaction_df = df.copy()
    for interaction in [var for var in combo if '_x_' in var]:
        var1, var2 = interaction.split('_x_')
        interaction_df[interaction] = df[var1] * df[var2]
    return interaction_df

def run_regressions(df, variables):
    regression_results = []
    for L in range(1, len(variables) + 1):
        for combo in generate_combinations(variables, L):
            X = df[list(combo)]
            y = df['CSUSHPINSA']  # Replace with your dependent variable name
            X = sm.add_constant(X)  # Adding a constant
            model = sm.OLS(y, X).fit()

            regression_results.append({
                'Variables': ', '.join(combo),
                'R-squared': model.rsquared,
                'Adj. R-squared': model.rsquared_adj,
                'P-value': model.f_pvalue,
                'AIC': model.aic,
                'BIC': model.bic
            })
    return regression_results

# Read top models file and extract variables
top_models_file = '../logs/csv_files/simple_regressions/simple_regressions_filtered/top_simple_models.csv'
top_models_df = pd.read_csv(top_models_file)
top_variables = top_models_df['Independent Variable'].tolist()

# Read data and run regressions
file_name = '../data/data.xlsx'
df = read_data(file_name)
results = run_regressions(df, top_variables)

# Save the results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f"../logs/csv_files/combination_regressions/combination_regression_results_{timestamp}.csv"
pd.DataFrame(results).to_csv(output_file_path, index=False)
print(f"Results saved to {output_file_path}")
