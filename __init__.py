from flask import Flask

app = Flask(__name__)
app.config.from_object('line-bot.config') # 追加

import line-bot.views