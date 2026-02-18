from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_presensi_2026'

users = [
    {"id": 1, "username": "admin", "password": "123", "role": "Admin", "nim": "-"}
]
data_pertemuan = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u_input = request.form.get('username')
        p_input = request.form.get('password')
        found = next((u for u in users if u['username'] == u_input and u['password'] == p_input), None)
        
        if found:
            session.clear()
            session['user_login'] = found['username']
            session['user_role'] = found['role']
            session['nim'] = found.get('nim', '-')
            
            if found['role'] == 'Admin': return redirect(url_for('admin_page'))
            if found['role'] == 'Dosen': return redirect(url_for('dashboard_dosen'))
            if found['role'] == 'Mahasiswa': return redirect(url_for('dashboard_mahasiswa'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/Admin')
def admin_page():
    if session.get('user_role') != 'Admin': return redirect(url_for('login'))
    return render_template('tampilan_admin.html', username=session.get('user_login'), users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    global users
    u, p, r, n = request.form.get('username'), request.form.get('password'), request.form.get('role'), request.form.get('nim', '-')
    if u and p:
        new_id = users[-1]['id'] + 1 if users else 1
        users.append({"id": new_id, "username": u, "password": p, "role": r, "nim": n})
    return redirect(url_for('admin_page'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    global users
    if user_id != 1:
        users = [u for u in users if u['id'] != user_id]
    return redirect(url_for('admin_page'))

@app.route('/dashboard/dosen')
def dashboard_dosen():
    if session.get('user_role') != 'Dosen': return redirect(url_for('login'))
    return render_template('dashboard_dosen.html')

@app.route('/dosen/pertemuan')
@app.route('/dosen/pertemuan/<int:id_p>')
def dosen_pertemuan(id_p=None):
    if session.get('user_role') != 'Dosen': return redirect(url_for('login'))
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    return render_template('pertemuan_dosen.html', pertemuan=data_pertemuan, p_detail=p_detail)

@app.route('/dosen/tambah', methods=['POST'])
def tambah_pertemuan():
    global data_pertemuan
    nama, tgl, mulai, selesai = request.form.get('nama'), request.form.get('tanggal'), request.form.get('mulai'), request.form.get('selesai')
    new_id = data_pertemuan[-1]['id'] + 1 if data_pertemuan else 1
    data_pertemuan.append({"id": new_id, "nama": nama, "tanggal": tgl, "mulai": mulai, "selesai": selesai})
    return redirect(url_for('dosen_pertemuan'))

@app.route('/dashboard/mahasiswa')
def dashboard_mahasiswa():
    if session.get('user_role') != 'Mahasiswa': return redirect(url_for('login'))
    return render_template('dashboard_mahasiswa.html')

@app.route('/mahasiswa/pertemuan')
@app.route('/mahasiswa/pertemuan/<int:id_p>')
def mahasiswa_pertemuan(id_p=None):
    if session.get('user_role') != 'Mahasiswa': return redirect(url_for('login'))
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    return render_template('pertemuan_mahasiswa.html', pertemuan=data_pertemuan, p_detail=p_detail)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)