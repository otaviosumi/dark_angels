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
<<<<<<< HEAD
    elif query_group == 'SEC':
        return redirect(url_for('infracao'))
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

@app.route('/view_people/<id_emp>')
def view_people_id(id_emp):
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT nregistro, nome, (case when grupo=\'ADM\' then \'Administration\' when grupo=\'SEC\' then \'Security\' when grupo=\'MAN\' then \'Maintenance\' end), treinamento, man_mecanica, man_eletrica, man_ti FROM funcionario WHERE nregistro=' + id_emp)
    emp_data = cursor.fetchall()
    return render_template("employee_data.html", data=emp_data)
        

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

        group_in = ''
        if request.form.get("filter_adm"):
            group_in = '\'ADM\''
        if request.form.get("filter_sec"):
            group_in = '\'SEC\'' if not group_in else group_in + ',\'SEC\''
        if request.form.get("filter_man"):
            group_in = '\'MAN\'' if not group_in else group_in + ',\'MAN\''

        if group_in:
            group_in = "(" + group_in + ")"
            select = select + " AND grupo IN " + group_in if flag_filter_on else select + " WHERE grupo IN " + group_in

    order = request.form.get('selectBox_order')
    if order:
        select = select + " ORDER BY " + order

    print(select) 
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("search_employee_filtered.html", rows=rows);

@app.route('/patrol_page')
def patrol_page():
=======
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
>>>>>>> 965e6731e74701961bca9d6b201194b69251ef05
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

<<<<<<< HEAD
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    select = "SELECT pa.chefe, pa.assistente, pr.lugar, TO_CHAR(pa.dia_data, 'dd/mm/yyyy') FROM patrulha pa JOIN protege pr ON pa.id_patrulha=pr.patrulha ORDER BY pa.dia_data, pa.chefe, pa.assistente"
    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("patrol_page.html", rows=rows);

@app.route('/new_patrol')
def new_patrol():
=======
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

@app.route('/view_people/<id_emp>')
def view_people_id(id_emp):
>>>>>>> 965e6731e74701961bca9d6b201194b69251ef05
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

<<<<<<< HEAD
=======
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT nregistro, nome, (case when grupo=\'ADM\' then \'Administration\' when grupo=\'SEC\' then \'Security\' when grupo=\'MAN\' then \'Maintenance\' end), treinamento, man_mecanica, man_eletrica, man_ti FROM funcionario WHERE nregistro=' + id_emp)
    emp_data = cursor.fetchall()
    return render_template("employee_data.html", data=emp_data)
        

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

        group_in = ''
        if request.form.get("filter_adm"):
            group_in = '\'ADM\''
        if request.form.get("filter_sec"):
            group_in = '\'SEC\'' if not group_in else group_in + ',\'SEC\''
        if request.form.get("filter_man"):
            group_in = '\'MAN\'' if not group_in else group_in + ',\'MAN\''

        if group_in:
            group_in = "(" + group_in + ")"
            select = select + " AND grupo IN " + group_in if flag_filter_on else select + " WHERE grupo IN " + group_in

    order = request.form.get('selectBox_order')
    if order:
        select = select + " ORDER BY " + order

    print(select) 
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("search_employee_filtered.html", rows=rows);

@app.route('/patrol_page')
def patrol_page():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    select = "SELECT pa.chefe, pa.assistente, pr.lugar, TO_CHAR(pa.dia_data, 'dd/mm/yyyy') FROM patrulha pa JOIN protege pr ON pa.id_patrulha=pr.patrulha ORDER BY pa.dia_data, pa.chefe, pa.assistente"
    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("patrol_page.html", rows=rows);

@app.route('/new_patrol')
def new_patrol():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

>>>>>>> 965e6731e74701961bca9d6b201194b69251ef05
    select = "SELECT nome_evento FROM nome_local";

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("new_patrol.html", rows=rows);

@app.route('/register_patrol', methods=['POST'])
def register_patrol(): 
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    pat_leader = request.form['pat_leader']
    pat_assist = request.form['pat_assist']
    pat_date = request.form['pat_date']
    pat_start_time = request.form['pat_start_time']
    pat_finish_time = request.form['pat_finish_time']

    new_pat_location = ''
    pat_location=''

    if request.form.get("new_location"):
        new_pat_location = request.form['pat_location'];

        if not new_pat_location:
            flash("Enter or select a location")
            return redirect(url_for('new_patrol'))

    else:
        pat_location = request.form.get('selectBox');

        if not pat_location:
            flash("Enter or select a location")           
            return redirect(url_for('new_patrol'))

    pat_finish_time = 'TO_TIMESTAMP(\'' + pat_finish_time + '\', \'HH24:MI\')' if pat_finish_time else 'NULL'

    location = new_pat_location if new_pat_location else pat_location;
    print(location)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute("SELECT id_patrulha FROM patrulha ORDER BY id_patrulha DESC");
    last_id = cursor.fetchall();

    try:
        #Patrulha insert
        cursor.execute('INSERT INTO patrulha VALUES (' +
            pat_leader + ', ' + 
            pat_assist + ', ' + 
            'TO_DATE(\'' + pat_date + '\', \'YYYY-MM-DD\'), ' +
            str(last_id[0][0]+1) + ')')

        #Location insert
        if new_pat_location:
            cursor.execute('INSERT INTO nome_local VALUES (' +
                '\'' + new_pat_location + '\')')


        orcl_db.commit()
        #Protect insert
        cursor.execute('INSERT INTO protege VALUES (\'' + 
                location + '\', ' +
                str(last_id[0][0]+1) + ', ' + 
                'TO_TIMESTAMP(\'' + pat_start_time + '\', \'HH24:MI\'), ' + 
                pat_finish_time + ')')

        orcl_db.commit()

    except cx.DatabaseError as e:
        flash("Register error. Check if all fields are properly filled and/or try again later.")
        return redirect(url_for('new_patrol'))

    return redirect(url_for('patrol_page'))
<<<<<<< HEAD
####################################################################################################################################

@app.route('/seguranca')
def infracao():
    if not 'username' in session:
        abort(403)

    return render_template('seguranca_page.html', name=session['username'])

@app.route('/autuacao')
def autuation():
    if not 'username' in session:
        abort(403)
        
    return render_template('autuacao.html', name=session['username'])

@app.route('/insert_autuation', methods=['POST'])
def insert_autuation():
    name_infringement = request.form['name_infringement']
    rg_infringement = request.form['rg_infringement']
    cpf_infringement = request.form['cpf_infringement']
    curso_infringement = request.form['curso_infringement']
    uni_infringement = request.form['uni_infringement']
    descr_infringement = request.form['description_infringement']
    pos_infringement = request.form['position_infringement']
    date_infringement = request.form['date_infringement']
    number_patrol = request.form['number_patrol']

    orcl_db = get_db();
    cursor = orcl_db.cursor()
    statement = 'INSERT INTO FLAGRANTE(CPF, NOME, RG, CURSO, UNIVERSIDADE)VALUES(:1, :2, :3, :4, :5)'
    cursor.execute(statement, (cpf_infringement, name_infringement, rg_infringement, curso_infringement, uni_infringement))
    orcl_db.commit()


    statement = """INSERT INTO AUTUACAO(FLAGRANTE, PATRULHA, HORA, INFRACAO)VALUES(:1, :2, to_date(:3, 'YYYY-MM-DD'), :4)"""
    cursor.execute(statement, (cpf_infringement, number_patrol, date_infringement, descr_infringement))
    orcl_db.commit()


    statement = """INSERT INTO MEDIDAS_TOMADAS(FLAGRANTE, PATRULHA, HORA, MEDIDA)VALUES(:1, :2, to_date(:3, 'YYYY-MM-DD'), :4)"""
    cursor.execute(statement, (cpf_infringement, number_patrol, date_infringement, pos_infringement))

    orcl_db.commit()
    return redirect('autuacao')


@app.route('/consulta_autuacao')
def view_consult():
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT cpf, nome, universidade, curso FROM flagrante')
    rows = cursor.fetchall()
    return render_template("consulta_autuacao.html", rows=rows)

@app.route('/consulta_autuacao/<cpf>')
def view_consult_id(cpf):
    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute('SELECT nome, cpf, universidade, curso FROM flagrante WHERE cpf = ' + "'" + cpf + "'" )
    infrin_data = cursor.fetchall()

    cursor.execute('SELECT infracao FROM autuacao WHERE flagrante = ' + "'" + cpf + "'" )
    infrin_data = infrin_data + cursor.fetchall()

    cursor.execute('SELECT medida FROM medidas_tomadas WHERE flagrante = ' + "'" + cpf + "'" )
    infrin_data = infrin_data + cursor.fetchall()

    return render_template("info_autuacao.html", data=infrin_data)
        

@app.route('/filtra_autuacao', methods=['POST'])
def filter_consult():

    flag_filter_on = 0;

    #Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    select = 'SELECT cpf, nome, universidade, curso FROM flagrante WHERE '
    
    filter_id = request.form['cpf']
    
    if filter_id:
        flag_filter_on = 1;
        select = select + " cpf = " + "'" + filter_id + "'"

    filter_name = request.form['name_infrin']     
    if filter_name:
        if flag_filter_on:
            select = select + " AND "
        select = select + " REGEXP_LIKE(nome, \'(^" + filter_name + "$)|(^" + filter_name + " )|( " + filter_name + "$)|(.* " + filter_name + " .*)', 'i')"
        flag_filter_on = 1;       

    filter_uni = request.form['universidade']
    if filter_uni:
        if flag_filter_on:
            select = select + " AND "

        select = select + " REGEXP_LIKE(universidade, \'(^" + filter_uni + "$)|(^" + filter_uni + " )|( " + filter_uni + "$)|(.* " + filter_uni + " .*)', 'i')"
        flag_filter_on = 1;

    filter_curso = request.form['curso']
    if filter_curso:
        if flag_filter_on:
            select = select + " AND "
        select = select + " REGEXP_LIKE(curso, \'(^" + filter_curso + "$)|(^" + filter_curso + " )|( " + filter_curso + "$)|(.* " + filter_curso + " .*)', 'i')"

    order = request.form.get('selectBox_order')
    if order:
        select = select + " ORDER BY " + order

    print(select) 
    #Open DB connection
    orcl_db = get_db()
    cursor = orcl_db.cursor()

    cursor.execute(select)
    rows = cursor.fetchall()

    return render_template("consulta_autuacao_filtrada.html", rows=rows);



=======
>>>>>>> 965e6731e74701961bca9d6b201194b69251ef05

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
