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
