from flask import Flask,render_template,request,flash,redirect
import os
import pred
import datetime 
import json
import shutil
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
from werkzeug.utils import secure_filename

line_bot_api = LineBotApi('6eB8eGyJKDMxFfhsZoppTbjc7B2aE441+u20PCqV2ASAuhKxLXek36HnCQnD5OL/xYle6oLj3mAe3ePBqS4IlLgweK1YIap1rejFjlFQZVcsXIYqfNFugjNOfFI5/0RmG5ovWbC28J5jxkWfh7qf4AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e4322b2aca42c6689e252179cf3691cd')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}
TODAY = str(datetime.date.today())

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] 
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pred.predict(event.message.text))
    )

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

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_form():
    dir = './recommend/'+TODAY
    if request.method == 'GET':
        preprocess.get_recommend()

    if request.method == 'POST':
        preprocess.post_recommend(request)
            
if __name__ == "__main__":
    app.run(debug=True)