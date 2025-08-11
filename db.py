import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            plan TEXT default 'free',
            payment_proof TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
);


if __name__ == '__main__':
    init_db()
