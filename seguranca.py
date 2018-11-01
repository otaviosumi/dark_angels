import os
import cx_Oracle as cx
from flask import Flask, render_template, request, flash, redirect, url_for, g, abort, session
app = Flask(__name__)

orcl_db = None;
cursor = None;

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

@app.route('/infracao')
def login():
    return render_template('autuacao.html')


@app.route('/insert_autuation', methods=['POST'])
def insert_autuation():
    name_infration = request.form['name_infration']
    rg_infration = request.form['rg_infration']
    cpf_infration = request.form['cpf_infration']
    curso_infration = request.form['curso_infration']
    uni_infration = request.form['uni_infration']

    #Check empty string
    # if not user_id or not password:
        # return redirect(url_for('login'))

    #Open DB connection
    orcl_db = get_db();
    cursor = orcl_db.cursor()
    statement = 'INSERT INTO FLAGRANTE(CPF, NOME, RG, CURSO, UNIVERSIDADE)VALUES(:1, :2, :3, :4, :5)'
    cursor.execute(statement, (cpf_infration, name_infration, rg_infration, curso_infration, uni_infration))
    orcl_db.commit()
    return render_template('autuacao.html')

    # cursor.execute('SELECT nome, senha, grupo FROM funcionario WHERE nregistro = ' + user_id)
    # query = cursor.fetchall()

    # query_user = query[0][0]
    # query_hash = query[0][1]
    # query_group = query[0][2]

    #Check password
    #if not validate_password(password, query_hash.replace('\n','')):
        #flash("ID or password is incorrect. Try again.");
        #return redirect(url_for('login'))
   
    #session['username'] = query_user;

    #if query_group == 'ADM':
        #return redirect(url_for('adm_section', user=query_user));
    #else:
        #return redirect(url_for('login'));

if __name__ == '__main__':
    app.secret_key = os.urandom(12);
    app.run(debug=True)
