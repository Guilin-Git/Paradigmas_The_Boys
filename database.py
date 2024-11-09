import sqlite3

def create_connection():
    return sqlite3.connect('heroes.db')

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        real_name TEXT,
        hero_name TEXT,
        gender TEXT,
        height REAL,
        weight REAL,
        birth_date TEXT,
        birth_place TEXT,
        powers TEXT,
        strength_level INTEGER,
        popularity INTEGER,
        status TEXT DEFAULT 'Ativo',
        battle_history TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_trigger():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS ban_hero
    AFTER UPDATE OF popularity ON heroes
    FOR EACH ROW
    WHEN NEW.popularity < 20
    BEGIN
        UPDATE heroes SET status = 'Banido' WHERE id = NEW.id;
    END;
    ''')
    conn.commit()
    conn.close()

def add_hero(hero_data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO heroes (real_name, hero_name, gender, height, weight, birth_date,
                        birth_place, powers, strength_level, popularity, status, battle_history)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', hero_data)
    conn.commit()
    conn.close()

def remove_hero(hero_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM heroes WHERE id = ?', (hero_id,))
    conn.commit()
    conn.close()

def update_hero(hero_id, updated_data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE heroes
    SET real_name = ?, hero_name = ?, gender = ?, height = ?, weight = ?, birth_date = ?,
        birth_place = ?, powers = ?, strength_level = ?, popularity = ?, status = ?, battle_history = ?
    WHERE id = ?
    ''', (*updated_data, hero_id))
    
    conn.commit()
    conn.close()

def search_heroes(name=None, status=None, popularity=None):
    conn = create_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM heroes WHERE 1=1"
    params = []
    
    if name:
        query += " AND hero_name LIKE ?"
        params.append(f"%{name}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if popularity is not None:
        query += " AND popularity >= ?"
        params.append(popularity)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Inicializa o banco de dados e o trigger
create_table()
create_trigger()
