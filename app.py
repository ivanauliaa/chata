import sys
import os
from flask import Flask, render_template, request

sys.path.append(os.getcwd())
from model.model import Model
from config.env import env

docs = [
  'dimana lokasi tempat alamat zona daerah kota kabupaten letak posisi',
  'kapan pmb pendaftaran mahasiswa baru jadwal pelaksanaan',
  'berpenampilan rapi celana pendek kaos',
  'halo hai hi',
  'sosmed medsos sosial media instagram ig website web facebook fb twitter tw youtube yt'
]

responses = [
  'Politeknik Elektronika Negeri Surabaya (PENS) berlokasi di Institut Teknologi Sepuluh Nopember, Kampus Jl. Raya ITS, Keputih, Kec. Sukolilo, Kota SBY, Jawa Timur.<br><br>Sumber: <a href="https://pens.ac.id" target="_blank">pens.ac.id</a>',
  'Pendaftaran Mahasiswa Baru Politeknik Elektornika Negeri Surabaya (PMB PENS) dilaksanakan dari tanggal 10 Juli 2022 - 30 Juli 2022.<br><br>Sumber: <a href="https://pmb.pens.ac.id" target="_blank">pmb.pens.ac.id</a>',
  'Mahasiswa wajib berpenampilan rapi dan sopan.<br><br>Sumber: Peraturan Akademik PENS',
  'Hi 👋, apakah ada yang bisa dibantu?',
  'Daftar Sosial Media Politeknik Elektronika Negeri Surabaya (PENS)<br>Web: <a href="https://pens.ac.id" target="_blank">pens.ac.id</a><br>Facebook: <a href="https://www.facebook.com/pens.eepis/" target="_blank">Politeknik Elektronika Negeri Surabaya</a><br>Instagram: <a href="https://www.instagram.com/penseepis/" target="_blank">@penseepis</a><br>Twitter: <a href="https://twitter.com/penseepis" target="_blank">@penseepis</a><br>Youtube: <a href="https://www.youtube.com/channel/UCgCH04Vjy22hnfTZBTMDccQ" target="_blank">PENS TV</a><br><br>Sumber: <a href="https://pens.ac.id" target="_blank">pens.ac.id</a>'
]

mdl = Model(docs, responses)

app = Flask(__name__, template_folder=env.TEMPLATE_DIR)
app.static_folder = env.STATIC_DIR
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return mdl.predict(userText)
if __name__ == "__main__":
    app.env = env.ENVIRONMENT
    try:
      app.run(host=env.APP_HOST, port=env.APP_PORT, debug=env.ENVIRONMENT=='development')
    except Exception as err:
      print(err)
