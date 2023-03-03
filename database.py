class Database:
    def __init__(self, connection):
        self.connection = connection
        self.init()

    def init(self):
        cursor = self.connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bandcamp(
        album_artist TEXT,
        album_title TEXT,
        album_url TEXT,
        album_id TEXT,
        disabled TEXT
        )''')

        self.connection.commit()

    def saveBandcamp(self, album_artist, album_title, album_url, album_id, disabled):
        album_artist = str(album_artist)
        album_title = str(album_title)
        album_url = str(album_url)
        album_id = str(album_id)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Bandcamp WHERE album_id=%s", (album_id,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            cursor = self.connection.cursor()
            sql = '''UPDATE Bandcamp SET album_artist=%s,album_title=%s,album_url=%s,disabled=%s WHERE album_id=%s'''
            cursor.execute(sql, (album_artist, album_title,album_url,disabled,album_id))
            self.connection.commit()
        else:
            cursor = self.connection.cursor()
            sql = ''' INSERT INTO Bandcamp(album_artist, album_title, album_url, album_id, disabled)
              VALUES(%s,%s,%s,%s,%s) '''
            cursor.execute(sql, (album_artist, album_title, album_url, album_id, disabled))
            self.connection.commit()

    def getBandcamp(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Bandcamp")
        rows = cursor.fetchall()
        return rows