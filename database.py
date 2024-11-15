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

def create_crimes_table():
        conn = create_connection()
        cursor = conn.cursor()
        # Define the updated structure without hero_id and hero_name
        cursor.execute('DROP TABLE IF EXISTS crimes')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS crimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_name TEXT,
            crime_description TEXT,
            crime_date TEXT,
            crime_severity INTEGER
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
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_hero_status
        AFTER UPDATE OF popularity ON heroes
        FOR EACH ROW
        WHEN NEW.popularity < 20 AND NEW.status != 'Banido'
        BEGIN
            UPDATE heroes SET status = 'Banido' WHERE id = NEW.id;
        END;
        ''')
    conn.commit()
    conn.close()

def create_missions_table():
    conn = create_connection()
    cursor = conn.cursor()
    # Define the updated structure without hero_id and hero_name
    cursor.execute('DROP TABLE IF EXISTS missions')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_name TEXT,
        mission_description TEXT,
        difficulty_level INTEGER CHECK(difficulty_level BETWEEN 1 AND 10),
        result TEXT CHECK(result IN ('Sucesso', 'Fracasso')),
        reward INTEGER
    )
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


def add_mission(mission_data):
    """
    Adiciona uma missão à tabela de missões e associa o herói à missão.
    :param mission_data: Dados da missão em forma de tupla (mission_name, mission_description, difficulty_level, result, reward)
    :param hero_id: ID do herói designado para a missão
    """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO missions (mission_name, mission_description, difficulty_level, result, reward)
    VALUES (?, ?, ?, ?, ?)
    ''', mission_data)

    # Atualizar a popularidade do herói apenas se necessário
    if mission_data[3] == "Sucesso":
        cursor.execute('''
        UPDATE heroes SET popularity = popularity + ? WHERE id = ?
        ''', (mission_data[4]))

    conn.commit()
    conn.close()

def add_crime(crime_data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO crimes (crime_name, crime_description, crime_date, crime_severity)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', crime_data)
    conn.commit()
    conn.close()

def remove_hero(hero_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM heroes WHERE id = ?', (hero_id,))
    conn.commit()
    conn.close()

def update_hero(hero_id, updated_data):
    """
    Atualiza os campos especificados do herói com base nos dados fornecidos.
    :param hero_id: ID do herói a ser atualizado
    :param updated_data: Dicionário com os campos e valores a serem atualizados, ex: {"popularity": 50}
    """
    conn = create_connection()
    cursor = conn.cursor()

    # Construir a query dinamicamente com base nos campos fornecidos
    fields = ', '.join([f"{key} = ?" for key in updated_data.keys()])
    values = list(updated_data.values())
    values.append(hero_id)

    query = f"UPDATE heroes SET {fields} WHERE id = ?"
    cursor.execute(query, values)
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

def search_crimes(hero_name=None, crime_severity=None):
    conn = create_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM crimes WHERE 1=1"
    params = []
    
    if hero_name:
        query += " AND hero_name LIKE ?"
        params.append(f"%{hero_name}%")
    if crime_severity:
        query += " AND crime_severity = ?"
        params.append(crime_severity)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_hero_by_id(hero_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM heroes WHERE id = ?', (hero_id,))
    hero = cursor.fetchone()
    conn.close()
    return hero

# Initialize the database and trigger
create_table()
create_crimes_table()
create_trigger()
create_missions_table()