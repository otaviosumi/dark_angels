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
# K9012931

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
    return render_template('new_employee_page.html')

####################################################################################

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

####################################################################################################################################


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



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
