@echo off
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main_with_interactions.py
pause
