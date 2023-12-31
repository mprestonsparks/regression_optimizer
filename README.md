# Regression Optimizer
<br>

## OVERVIEW
### main.py
- Takes data from a spreadsheet (in `data/data.xlsx`)
- Runs linear regressions to predict a dependent variable using every combination of independent variables
- Ranks these models by highest R-squared value
- Saves output to `/logs`

### analyze_model.py
- Takes data produced by `main.py` from `logs/text_files/master_tables` (a comprehensive table of model results)
- Creates a custom prompt incorporating `master_table` data
- Sends the generated prompt to an LLM for analysis
- Saves the LLM response in `logs/text_files/gpt_summaries/`
<br><br>

## GETTING STARTED

### Setup Virtual Environment and Install Dependencies
1. Clone the repository to your machine and navigate to the new directory

**MacOS**<br>
```python -m venv venv``` <br>
```source venv/bin/activate``` <br>
```pip install -r requirements.txt```
<br>

**Windows**<br>
```python -m venv venv``` <br>
```venv/Scripts/activate``` <br>
```pip install -r requirements.txt```
<br><br>
### Run `main.py`
1. Ensure that your data is correctly formatted and placed in the **data/data.xlsx** file
2. Run ```python src/main.py``` to perform the regression analysis <br>
<br>

### Run `analyze_model.py`
After running **main.py**
1. Run ```python src/analyze_model.py```
2. Check the **logs/text_files/gpt_summaries/** directory for the analysis results
<br><br>
<br><br>
## LICENSE
**Copyright 2023 &copy; M. Preston Sparks** <br>
All Rights Reserved. <br>
Unauthorized copying, modification, distribution, or use of this repository's contents, including but not limited to software, data files, documentation, and any other materials, via any medium, is strictly prohibited without express written permission from the copyright holder. <br>
This repository contains proprietary and confidential material. <br>
**Written by M. Preston Sparks, December 2023.**
