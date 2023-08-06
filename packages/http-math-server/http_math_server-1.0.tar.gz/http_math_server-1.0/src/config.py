from os import getenv


DB_USER = getenv('pguser', default='postgres')
DB_PASS = getenv('pgpasswd', default='1234')
DB_HOST = getenv('pghost', default='localhost')
# DB_HOST = getenv('pghost', default='78a17a034b1d')
DB_PORT = getenv('pgport', default=5432)
DB_NAME = getenv('pgdb', default='math_data')
