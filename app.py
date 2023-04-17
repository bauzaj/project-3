from sqlalchemy import create_engine
from flask import Flask, render_template, jsonify
from config import username, pw, hostname, port, db
import pandas as pd

app = Flask(__name__)

engine = create_engine(f'postgresql+psycopg2://{username}:{pw}@{hostname}:{port}/{db}')

@app.route('/api/v1.0/prpvff')
def prpvff():
    conn = engine.connect()
    query = '''SELECT income, spemch, prpmel, fastfd, AVG(bmi) as avg_bmi
               FROM resp r
               WHERE spemch BETWEEN 1 AND 5 AND income >=0 AND fastfd >= 1 AND bmi > 0
               GROUP BY spemch, income, prpmel, fastfd;'''
    df = pd.read_sql(query, conn)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/v1.0/genhealth')
def genhealth():
    conn = engine.connect()
    query = '''SELECT AVG(bmi) FROM resp
               WHERE bmi >= 0 AND genhth >= 0
               GROUP BY genhth;'''
    df = pd.read_sql(query, conn)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/v1.0/eat_healthy')
def eat_healthy():
    conn = engine.connect()
    query = '''SELECT genhth, AVG(exfreq) as avg_exferq
               FROM resp r
               WHERE genhth >=1 AND exfreq >= 1
            GROUP BY genhth;'''
    df = pd.read_sql(query, conn)
    return jsonify(df.to_dict(orient='records'))

@app.route('/index')
def index():
    prpvff_data = pd.read_json('http://127.0.0.1:5000/api/v1.0/prpvff')
    genhealth_data = pd.read_json('http://127.0.0.1:5000/api/v1.0/genhealth')
    eat_healthy_data = pd.read_json('http://127.0.0.1:5000/api/v1.0/eat_healthy')

    prpvff_column_names = prpvff_data.columns.tolist()
    prpvff_data = prpvff_data.values.tolist()
    genhealth_column_names = genhealth_data.columns.tolist()
    genhealth_data = genhealth_data.values.tolist()
    eat_healthy_column_names = eat_healthy_data.columns.tolist()
    eat_healthy_data = eat_healthy_data.values.tolist()

    return render_template('index.html', prpvff_column_names=prpvff_column_names, prpvff_data=prpvff_data,
                           genhealth_column_names=genhealth_column_names, genhealth_data=genhealth_data,
                           eat_healthy_column_names=eat_healthy_column_names, eat_healthy_data=eat_healthy_data)

if __name__ == '__main__':
    app.run(debug=True)
