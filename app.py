from flask import Flask, render_template, request, redirect, session
from utils import konversi_nilai_ke_label, konversi_label_ke_bobot

app = Flask(__name__)
app.secret_key = "rahasia"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/biodata", methods=["GET", "POST"])
def biodata():
    if request.method == "POST":
        session["biodata"] = {
            "nama": request.form["nama"],
            "nim": request.form["nim"],
            "prodi": request.form["prodi"]
        }
        return redirect("/biodata")

    return render_template("biodata.html", biodata=session.get("biodata"))

@app.route("/sks", methods=["GET", "POST"])
def sks():
    if request.method == "POST":
        # fixed 3 input, tidak pakai 'jumlah'
        session["sks"] = [
            int(request.form[f"sks{i}"]) for i in range(3)
        ]
        return redirect("/")

    return render_template("sks.html")

@app.route("/nilai", methods=["GET", "POST"])
def nilai():
    if request.method == "POST":
        # fixed 3 input, tidak pakai 'jumlah'
        session["nilai"] = [
            float(request.form[f"nilai{i}"]) for i in range(3)
        ]
        return redirect("/")

    return render_template("nilai.html")

@app.route("/lihat-nilai")
def lihat_nilai():
    sks = session.get("sks")
    nilai = session.get("nilai")

    if not sks or not nilai or len(sks) != len(nilai):
        return render_template("lihat_nilai.html", data=[])

    data = []
    for i in range(len(nilai)):
        label = konversi_nilai_ke_label(nilai[i])
        bobot = konversi_label_ke_bobot(label)
        data.append((sks[i], nilai[i], label, bobot))

    return render_template("lihat_nilai.html", data=data)

@app.route("/lihat-ip")
def lihat_ip():
    sks = session.get("sks")
    nilai = session.get("nilai")

    if not sks or not nilai or len(sks) != len(nilai):
        return render_template("lihat_ip.html", ips=None)

    total = 0
    for i in range(len(nilai)):
        label = konversi_nilai_ke_label(nilai[i])
        total += konversi_label_ke_bobot(label) * sks[i]

    ips = round(total / sum(sks), 2)
    return render_template("lihat_ip.html", ips=ips)

if __name__ == "__main__":
    app.run(debug=True)
