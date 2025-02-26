import sqlite3


class DateBase:
    def __init__(self):
        self.connection: sqlite3.Connection = sqlite3.connect('tudaSuda/dataPlace.db')#tudaSuda/
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
        
    def close(self):
        self.connection.close()

    def execute(self, request):
        self.cursor.execute(request)
        return self.cursor
        
        
if __name__ == '__main__':
    base = DateBase()
    a = base.execute(
        f"""SELECT * FROM users WHERE id = 0"""
            ).fetchone()
    
    print(a)
    base.commit()
    base.close()
    