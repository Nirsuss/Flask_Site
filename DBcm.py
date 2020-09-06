import mysql.connector#Диспетчер Контекста стр 371
class UseDatabase:
    def __int__(self, config: dict):
        self.configuration = config
    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.con.commit()
        self.cursor.close()
        self.conn.close()
