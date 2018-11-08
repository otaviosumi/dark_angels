import os
import bcrypt as bc
import cx_Oracle as cx
from flask import Flask, render_template, request, flash, redirect, url_for, g, abort, session
app = Flask(__name__)

orcl_db = None
cursor = None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        dns_tns = cx.makedsn('grad.icmc.usp.br', 15215, 'orcl')
        db = g._database = cx.connect('K9012931','K9012931',dns_tns)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print("Closing DB")
        db.close()

def validate_password(password, pass_hash):
    validate = False;

    try:
        validate = bc.hashpw(password, pass_hash) == pass_hash
    except (TypeError):
        password = password.encode('utf-8')
        pass_hash = pass_hash.encode('utf-8')
        validate = bc.hashpw(password, pass_hash) == pass_hash

    return validate

@app.route('/')
def index_page():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))

@app.route('/validate_login', methods=['POST'])
def validate_login():
    user_id = request.form['user_id']
    password = request.form['password']

    #Check empty string
    if not user_id or not password:
        return redirect(url_for('login'))

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT nome, senha, grupo FROM funcionario WHERE nregistro = ' + user_id)
    query = cursor.fetchall()

    query_user = query[0][0]
    query_hash = query[0][1]
    query_group = query[0][2]

    #Check password
    if not validate_password(password, query_hash):
        flash("ID or password is incorrect. Try again.")
        return redirect(url_for('login'))
   
    session['username'] = query_user

    if query_group == 'ADM':
        return redirect(url_for('adm_section'))
        #return redirect(url_for('adm_section', user=query_user))
    else:
        return redirect(url_for('login'))

@app.route('/adm_section')
def adm_section():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    return render_template('adm_page.html', name=session['username'])

@app.route('/new_employee')
def new_employee():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    return render_template('new_employee_page.html')

@app.route('/register_employee', methods=['POST'])
def register_employee():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    emp_name = request.form['emp_name']
    emp_id = request.form['emp_id']
    emp_pass = request.form['emp_pass']
    emp_group = request.form.get('selectBox')
    emp_train = 'NULL'
    man_mec = 'NULL'
    man_ele = 'NULL'
    man_ti = 'NULL'

    emp_name = emp_name.encode('ascii', errors='ignore').decode()

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    if emp_group == "SEC":
        emp_train = '\'' + request.form['emp_train'] + '\''
    elif emp_group == "MAN":
        if request.form.get("man_ele"):
            man_ele = request.form['man_ele_nr']
        if request.form.get("man_mec"):
            man_mec = request.form['man_mec_nr']
        if request.form.get("man_ti"):
            man_ti = request.form['man_ti_nr']
     

    try:
        password = bc.hashpw(emp_pass, bc.gensalt())
    except (TypeError):
        password = bc.hashpw(emp_pass.encode('utf-8'), bc.gensalt()).decode()

    try: 
        cursor.execute('INSERT INTO FUNCIONARIO VALUES (' + 
            emp_id + ', \'' + 
            emp_name + '\', ' + 
            emp_train + ', ' + 
            man_mec + ', ' + 
            man_ele + ', ' + 
            man_ti + ', \'' + 
            password + '\', \'' +
            emp_group + '\')')

        orcl_db.commit()

    except cx.DatabaseError as e:
        flash("Register error. Check if all fields are properly filled and/or try again later.")
        raise
        return redirect(url_for('new_employee'))

    return redirect(url_for('adm_section'))


@app.route('/view_people')
def view_people():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT nregistro, nome, grupo FROM funcionario')
    rows = cursor.fetchall()
    return render_template("search_employee.html", rows=rows)

@app.route('/filter_people', methods=['POST'])
def filter_people():

    flag_filter_on = 0;

    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    select = 'SELECT nregistro, nome, grupo FROM funcionario'
    
    filter_id = request.form['id_emp']
    
    if filter_id:
        select = select + " WHERE nregistro = " + filter_id

    else:
        filter_name = request.form['name_emp']
         
        if filter_name:
            flag_filter_on = 1;
            select = select + " WHERE REGEXP_LIKE(nome, \'(^" + filter_name + "$)|(^" + filter_name + " )|( " + filter_name + "$)|(.* " + filter_name + " .*)', 'i')"

        if request.form.get("man_ele"):
            man_ele = request.form['man_ele_nr']
        if request.form.get("man_mec"):
            man_mec = request.form['man_mec_nr']
        if request.form.get("man_ti"):
            man_ti = request.form['man_ti_nr']
   

    
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("search_employee_filtered.html", rows=rows);

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
