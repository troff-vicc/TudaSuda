import sqlite3


class DateBase:
    def __init__(self):
        self.connection: sqlite3.Connection = sqlite3.connect('dataPlace.db')#tudaSuda/
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
    encoded_string = base64.b64encode(file.read())
    base.execute(
        f"""DELETE FROM images WHERE id = 2"""
            )
    base.commit()
    base.close()
    