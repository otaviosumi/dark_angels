# Dark Angels - segurança de eventos
Um trabalho de base de dados

Utilizando Postgresql:
------
Primeiro se instala a BD:
```
sudo apt-get install postgresql postgresql-contrib
```
Depois se cria um usuário:
```
sudo passwd postgres
```
Iniciar e Parar o servidor local:
```
sudo service postgresql start
sudo service postgresql stop
```
Loga-se no usuário:
```
su - postgres
```
Para sair do prompt:
```
\q
```
Instalando módulos:
--------
```
pip install psycopg2
```
Aplicativos de terceiros
----------------

Dark-Angel se utiliza das seguintes aplicações de terceiros:

|Nome            |Versão       |Website                 |
|----------------|:-----------:|------------------------|
|Postgresql      |9.5.14       |https://www.postgresql.org/download/|
|Python          |2.7.12       |https://www.python.org/|
|Psycopg         |2.7.5        |http://initd.org/psycopg/|
|Virtualenv      |16.0.0       |https://virtualenv.pypa.io/en/stable/|
