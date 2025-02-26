import cx_Oracle

oracle_config = {
    "user": "integra",
    "password": "integra",
    "dsn": "192.168.0.42:1521/POTIGUAR",
    "encoding": "UTF-8"
}

def get_connection():
    try:
        conn = cx_Oracle.connect(**oracle_config)
        return conn
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Erro de conexão: {error.code} - {error.message}")
        return None 
