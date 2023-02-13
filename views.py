from flask import render_template, request 
from line-bot import app
from line-bot import pred


@app.route('/')
def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template('index.html', my_dict=my_dict)

@app.route('/form', methods=['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method == 'POST':
        print('POSTデータ受け取ったので処理します。')
        message = pred.predict(request.form['data1'])
        return f'POST受け取ったよ: {message}'