import sqlite3

def create_database():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, author TEXT, url TEXT, description TEXT)''')
    conn.commit()
    conn.close()