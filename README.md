# Dark Angels - segurança patrimonial de eventos
Trabalho para matéria de Bases de Dados do ICMC - USP


Instalando módulos
------------
```
python3 -m pip install bcrypt
python3 -m pip install cx_Oracle
python3 -m pip install virtualenv
python3 -m pip install Flask
```

Utilizando
--------------

Utilizamos a execução dentro de ambiente virtual da seguinte forma:
```
virtualenv venv
source venv/bin/activate
python3 index.py
```
Desta forma criamos o ambiente, o ligamos e rodamos utilizando a terceira versão do python.

Aplicativos de terceiros
----------------

Dark-Angel se utiliza das seguintes aplicações de terceiros:

|Nome            |Versão       |Website                 |
|----------------|:-----------:|------------------------|
|Python          |3.0.1      |https://www.python.org/|
|Virtualenv      |16.0.0       |https://virtualenv.pypa.io/en/stable/|
|Flask           |1.0.2        |http://flask.pocoo.org/docs/0.12/installation/|
| cx_Oracle  | 7.0.0  | https://pypi.org/project/cx_Oracle/ |
| ODPI-C  | x64 - 18.3  |  https://oracle.github.io/odpi/doc/installation.html#linux |
| SQL-developer  |  x64 - 18.3 |  https://www.oracle.com/database/technologies/appdev/sql-developer.html  |
| bcrypt  |  3.1.4 | https://pypi.org/project/bcrypt/  |
