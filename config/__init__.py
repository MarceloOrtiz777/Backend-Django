import pymysql

# Hace que Django use pymysql (driver MySQL 100% Python) en vez de mysqlclient,
# que requiere compilación y suele dar problemas al instalar en Windows.
pymysql.install_as_MySQLdb()
