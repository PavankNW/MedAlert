from flask import Flask, render_template, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL Server Connection
server = 'CPCINPUDV003086'
database = 'sampDB'
#username = 'your_username'
#password = 'your_password'
conn_str = f'DRIVER=SQL Server;SERVER={server};DATABASE={database}'#'UID={username};PWD={password}'
 
#Connect to the database
conn = pyodbc.connect(conn_str)

cursor = conn.cursor()

@app.route('/')
def home():
    patient_ids = get_patient_ids()
    return render_template('index.html', patient_ids=patient_ids)

@app.route('/get_bio_vitals', methods=['POST'])
def get_bio_vitals():
    Patient_ID = request.form.get('patient_id')
    bio_vitals = get_bio_vitals_data(Patient_ID)
    return jsonify(bio_vitals)

@app.route('/get_lifestyle_params', methods=['POST'])
def get_lifestyle_params():
    Patient_ID = request.form.get('patient_id')
    lifestyle_params = get_lifestyle_params_data(Patient_ID)
    return jsonify(lifestyle_params)

def get_patient_ids():
    cursor.execute("SELECT DISTINCT Patient_ID FROM secondary_table")
    patient_ids = [row.Patient_ID for row in cursor.fetchall()]
    return patient_ids

def get_bio_vitals_data(Patient_ID):
    cursor.execute(f"SELECT [Heart_Rate(60--100 bpm)], [Body_Temperature(95--98.6 F)], [O2_Saturation_in_Blood(95%--100%)], [Diastolic_BP (70-90mm Hg)], [Systolic_BP (110- 130mm Hg)], [Respiratory_Rate (12-16 bpm)] FROM secondary_table WHERE Patient_ID = '{Patient_ID}'")
    bio_vitals = [{'Heart_Rate': row[0], 'Body_Temperature': row[1], 'O2_Saturation_in_Blood': row[2], 'Diastolic_BP': row[3], 'Systolic_BP': row[4], 'Respiratory_Rate': row[5]} for row in cursor.fetchall()]
    return bio_vitals

def get_lifestyle_params_data(Patient_ID):
    cursor.execute(f"SELECT [sugar_fast(70-100 mg/dL)], [sugar_normal(140-160 mg/dL)], [sugar_after_meal(170-200 mg/dL)], [cholestrol(125-200 mg/dL)], [sleep(>7 Hrs)] FROM secondary_table WHERE Patient_ID = '{Patient_ID}'")
    lifestyle_params = [{'sugar_fast': row[0], 'sugar_normal': row[1], 'sugar_after_meal': row[2], 'cholestrol': row[3], 'sleep': row[4]} for row in cursor.fetchall()]
    return lifestyle_params

if __name__ == '__main__':
    app.run(debug=True)