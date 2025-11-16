from flask import Flask, render_template, request, redirect, url_for
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    with open('text.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    with open('iot.txt', 'r', encoding='utf-8') as file:
        content1 = file.read()
    with open('iot2.txt', 'r', encoding='utf-8') as file:
        content2 = file.read()
    with open('iot3.txt', 'r', encoding='utf-8') as file:
        content3 = file.read()
    return render_template('1home.html', text=content,text1=content1, text2=content2, text3=content3)

@app.route('/data')
def data():
    df = pd.read_csv('out.csv')
    data_html = df.to_html(classes='table table-striped', index=False)
    return render_template('2data.html', data=data_html)

import pandas as pd

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        suhu_udara = request.form['suhu_udara']
        kelembaban_udara = request.form['kelembaban']
        suhu_tanah = request.form['suhu_tanah']
        kelembaban_tanah = request.form['kelembaban_tanah']
        cahaya = request.form['cahaya']
        arus_solar = request.form['arus_solar']
        arus_aki = request.form['arus_aki']
        tegangan_solar = request.form['tegangan_solar']
        tegangan_aki = request.form['tegangan_aki']

        df = pd.read_csv('support.csv')

        match = df[
            (df['suhu udara'] == suhu_udara) &
            (df['kelembaban udara'] == kelembaban_udara) &
            (df['suhu tanah'] == suhu_tanah) &
            (df['kelembaban tanah'] == kelembaban_tanah) &
            (df['cahaya'] == cahaya) &
            (df['arus solar'] == arus_solar) &
            (df['arus aki'] == arus_aki) &
            (df['tegangan solar'] == tegangan_solar) &
            (df['tegangan aki'] == tegangan_aki)
        ]

        if not match.empty:
            status = match['status'].iloc[0]  
        else:
            status = "Status tidak ditemukan"

        return render_template('3analysis.html', status=status)

    return render_template('3analysis.html')
    

@app.route('/visual')
def visual():
    return render_template('4visual.html')

if __name__ == "__main__":
    app.run(debug=True)
