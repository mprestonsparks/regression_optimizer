import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations, combinations_with_replacement
from datetime import datetime

# Read data from Excel
def read_data(file_name):
    df = pd.read_excel('../data/' + file_name)
    
    # Convert all columns to numeric, except for the date column
    for col in df.columns:
        if col != 'Date':  # Replace 'Date' with the name of your date column
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill missing values
    df.fillna(0, inplace=True)

    # Debugging: Print out data types
    print("Data types after conversion:")
    print(df.dtypes)

    return df

# Generate all combinations of independent variables including unique interactions
def generate_combinations(variables, max_length):
    all_combos = []
    for L in range(1, max_length+1):
        for combo in combinations(variables, L):
            all_combos.append(combo)
            if L == 1:  # Only add interactions for single variables
                continue
            for interaction in combinations(combo, 2):
                interaction_term = '_x_'.join(interaction)
                all_combos.append(combo + (interaction_term,))
    return all_combos

# Create interaction terms
def create_interactions(df, variables):
    interaction_df = df.copy()
    for interaction in [var for var in variables if '_x_' in var]:
        var1, var2 = interaction.split('_x_')
        interaction_df[interaction] = df[var1] * df[var2]
    return interaction_df

# Helper function to determine if the current model is better
def is_better_model(current, best):
    return (current['Adj. R-squared'] > best['Adj. R-squared']) or \
           (current['Adj. R-squared'] == best['Adj. R-squared'] and current['AIC'] < best['AIC']) or \
           (current['Adj. R-squared'] == best['Adj. R-squared'] and current['AIC'] == best['AIC'] and current['BIC'] < best['BIC'])

# Run regression for each combination and find the best model
def find_best_model(df, dependent_var):
    independent_vars = [var for var in df.columns if var != dependent_var and var != 'Date']
    best_criteria = {'Adj. R-squared': -np.inf, 'AIC': np.inf, 'BIC': np.inf}
    best_model = None
    best_combo = None
    master_summary_data = []
    model_number = 1

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # File paths to save output
    text_file_path = f"../logs/text_files/regression_summaries/regression_summary_{timestamp}.txt"
    csv_file_path = f"../logs/csv_files/model_summaries/model_summaries_{timestamp}.csv"
    master_table_path = f"../logs/text_files/master_tables/master_table_{timestamp}.txt"

    with open(text_file_path, 'w') as log_file, open(master_table_path, 'w') as master_file:
        for combo in generate_combinations(independent_vars, len(independent_vars)):
            interaction_df = create_interactions(df, combo)
            X = interaction_df[list(combo)].reset_index(drop=True)
            X = sm.add_constant(X)
            y = df[dependent_var].reset_index(drop=True)

            try:
                model = sm.OLS(y, X).fit()
                model_criteria = {
                    'Adj. R-squared': model.rsquared_adj,
                    'AIC': model.aic,
                    'BIC': model.bic
                }

                if is_better_model(model_criteria, best_criteria):
                    best_criteria = model_criteria
                    best_model = model
                    best_combo = combo

                model_summary = f"Model with variables {combo}:\n" + model.summary().as_text() + "\n\n"
                print(model_summary)
                log_file.write(model_summary)

                # Extract model parameters for the master table
                params = model.params
                pvalues = model.pvalues
                conf_int = model.conf_int()
                for param in params.index:
                    master_summary_data.append({
                        'Model Number': model_number,
                        'Variable': param,
                        'Coefficient': params[param],
                        'P-Value': pvalues[param],
                        'Confidence Interval Low': conf_int.loc[param, 0],
                        'Confidence Interval High': conf_int.loc[param, 1]
                    })

                model_number += 1

            except Exception as e:
                print(f"Error with combo {combo}: {e}")

        best_summary = f"Best model with R-squared {best_criteria['Adj. R-squared']} uses variables {best_combo}\n"
        print(best_summary)
        log_file.write(best_summary)

        # Convert the list of dictionaries to a DataFrame and save it
        master_summary_df = pd.DataFrame(master_summary_data)
        master_summary_df.to_csv(master_table_path, index=False)

    # Return the paths to the saved files for further use
    return best_model, best_combo, text_file_path, csv_file_path, master_table_path


file_name = 'data.xlsx'
df = read_data(file_name)
best_model, best_combo, text_file_path, csv_file_path, model_summaries = find_best_model(df, 'House_Price_Index')

print(model_summaries)

