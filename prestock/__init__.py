from flask import Flask

app = Flask(__name__)
app.config.from_object('prestock.config') # 追加

import prestock.views