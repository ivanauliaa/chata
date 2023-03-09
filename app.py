import sys
import os
import pandas as pd
from flask import Flask, render_template, request

sys.path.append(os.getcwd())
from model.model import Model
from config.env import env

df1 = pd.read_csv('1-key-value-response.csv', names=['key', 'value'])
df1['value'] = df1['value'].str.replace('\n', '<br>')
df2 = pd.read_csv('2-key-value-response.csv', names=['key', 'value'])
df2['value'] = df2['value'].str.replace('\n', '<br>')
df3 = pd.read_csv('3-key-value-response.csv', names=['key', 'value'])
df3['value'] = df3['value'].str.replace('\n', '<br>')
df4 = pd.read_csv('4-key-value-response.csv', names=['key', 'value'])
df4['value'] = df4['value'].str.replace('\n', '<br>')

mdls = [
  Model(df1['key'].tolist(), df1['value'].tolist()),
  Model(df2['key'].tolist(), df2['value'].tolist()),
  Model(df3['key'].tolist(), df3['value'].tolist()),
  Model(df4['key'].tolist(), df4['value'].tolist()),
]

app = Flask(__name__, template_folder=env.TEMPLATE_DIR)
app.static_folder = env.STATIC_DIR
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")
def get_bot_response():
    category = int(request.args.get('category'))
    userInput = request.args.get('msg')

    if category >= 0 and category < len(mdls):
      return mdls[category].predict(userInput)
    else:
      return 'Invalid category'

if __name__ == "__main__":
    app.env = env.ENVIRONMENT
    try:
      app.run(host=env.APP_HOST, port=env.APP_PORT, debug=env.ENVIRONMENT=='development')
    except Exception as err:
      print(err)
