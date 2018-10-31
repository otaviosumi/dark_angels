# Dark Angels - segurança patrimonial de eventos
Trabalho para matéria de Bases de Dados do ICMC - USP

Utilizando Postgresql:
------
Primeiro deve-se instalar tudo que é necessário para rodar tanto o BD([ODPI-C](https://oracle.github.io/odpi/doc/installation.html#linux), [SQL-developer](https://askubuntu.com/questions/458554/how-to-install-sql-developer-on-ubuntu-14-04), [cx_Oracle](https://pypi.org/project/cx_Oracle/)) quanto as questões de segurança([bcrypt](https://pypi.org/project/bcrypt/)).

Instalando módulos
------------
```
pip install bcrypt
pip install cx_Oracle
pip install virtualenv
pip install Flask
```
Aplicativos de terceiros
----------------

Dark-Angel se utiliza das seguintes aplicações de terceiros:

|Nome            |Versão       |Website                 |
|----------------|:-----------:|------------------------|
|Python          |2.7.12       |https://www.python.org/|
|Virtualenv      |16.0.0       |https://virtualenv.pypa.io/en/stable/|
|Flask           |1.0.2        |http://flask.pocoo.org/docs/0.12/installation/|
| cx_Oracle  | 7.0.0  | https://pypi.org/project/cx_Oracle/ |
| ODPI-C  | x64 - 18.3  |  https://oracle.github.io/odpi/doc/installation.html#linux |
| SQL-developer  |  x64 - 18.3 |  https://www.oracle.com/database/technologies/appdev/sql-developer.html  |
| bcrypt  |  3.1.4 | https://pypi.org/project/bcrypt/  |
