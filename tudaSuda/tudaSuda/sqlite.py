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
    import json
    
    img = json.dumps([f'3'])
    base.execute(f"""UPDATE route
                    SET img = '{img}'
                    WHERE id = {1}; """
                     )
    base.commit()
    base.close()
    