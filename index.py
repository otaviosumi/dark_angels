import os
import bcrypt as bc
import cx_Oracle as cx
from flask import Flask, render_template, request, flash, redirect, url_for, g, abort, session
app = Flask(__name__)

orcl_db = None;
cursor = None;

def is_client(client_cnpj):
	orcl_db = get_db()
	cursor = orcl_db.cursor()
	cursor.execute('SELECT CNPJ FROM CLIENTE WHERE CNPJ=\'' + client_cnpj + '\'')
	query = cursor.fetchall()
	if len(query) > 0:
		query_cnpj = query[0][0]
		if query_cnpj == client_cnpj:
			return True
	return False


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
    return bc.hashpw(password, pass_hash) == pass_hash

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
    if not validate_password((password).encode('utf-8'), (query_hash.replace('\n','')).encode('utf-8')):
        flash("ID or password is incorrect. Try again.");
        return redirect(url_for('login'))
   
    session['username'] = query_user;

    if query_group == 'ADM':
        return redirect(url_for('adm_section', user=query_user));
    else:
        return redirect(url_for('login'));

@app.route('/adm_section/<user>')
def adm_section(user):

    #Check if someone just type the url manually
    if str(request.referrer).find('login') == -1:
        abort(403)

    return render_template('adm_page.html', name=user)


#################################################################################################################
#Client stuff
@app.route('/add_new_client', methods=['POST'])
def add_new_client():

	#default values
	client_cnpj = 'null'
	cep_central = 'null'
	num_central = 0
	contrat_days= 0
	contract_description = 'null'
	contract_price = 0.0

	client_cnpj = request.form['cnpj']
	client_cnpj = client_cnpj[0:17]
	cep_central = request.form['cep_central']
	cep_central = cep_central[0:9]
	num_central = request.form['num_central']
	num_central = int(num_central)
	contrat_days = request.form['days']
	contrat_days = int(contrat_days)
	contract_description = request.form['desc']
	contract_description = contract_description[0:99]
	contract_price = request.form['price']
	contract_price = float(contract_price)

	orcl_db = get_db()
	cursor = orcl_db.cursor()
	if not is_client(client_cnpj):
		cursor.execute('INSERT INTO CLIENTE VALUES ( \'' + client_cnpj + '\')')
		print ('New client added')
	print('Old client found')

	print ('cep_central: ' + cep_central+ '\n' + 'num_central: '+ str(num_central))
	cursor.execute('INSERT INTO CONTRATO  VALUES ( \'' + client_cnpj + '\', \''
													+ cep_central + '\', '
													+ str(num_central) + ', '
													+ str(contrat_days) + ', \''
													+ contract_description + '\', '
													+ str(contract_price) + ')')

	orcl_db.commit()
	print ('Client ' + client_cnpj + ' added')



	return render_template('adm_page.html', name=session['username'])



@app.route('/new_client/')
def adm_add_client():
	#Check if someone just type the url manually
    if not 'username' in session:
        abort(403)

    return render_template('adm_page_add_client.html', name=session['username'])

if __name__ == '__main__':
    app.secret_key = os.urandom(12);
    app.run(debug=True)
