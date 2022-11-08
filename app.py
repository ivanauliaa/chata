import sys
import os

sys.path.append(os.getcwd())
from model.model import Model

docs = [
  "dimana lokasi tempat alamat zona daerah kota kabupaten letak posisi",
  "kapan pmb pendaftaran mahasiswa baru jadwal pelaksanaan",
  "berpenampilan rapi celana pendek kaos"
]

responses = [
  'Politeknik Elektronika Negeri Surabaya (PENS) berlokasi di Institut Teknologi Sepuluh Nopember, Kampus Jl. Raya ITS, Keputih, Kec. Sukolilo, Kota SBY, Jawa Timur',
  'Pendaftaran Mahasiswa Baru Politeknik Elektornika Negeri Surabaya (PMB PENS) dilaksanakan dari tanggal 10 Juli 2022 - 30 Juli 2022',
  'Harus berpenampilan rapi dan sopan'
]

mdl = Model(docs, responses)

from flask import Flask, render_template, request
app = Flask(__name__, template_folder='public')
app.static_folder = 'public'
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return mdl.predict(userText)
if __name__ == "__main__":
    app.run()