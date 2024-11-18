from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def create_connection():
    return sqlite3.connect('heroes.db')

@app.route('/')
def serve_HomePage():
    return send_from_directory('', 'index.html')

@app.route('/heroes.html')
def serve_index():
    return send_from_directory('', 'heroes.html')

@app.route('/missao.html')
def serve_missions():
    return send_from_directory('', 'missao.html')

@app.route('/crimes.html')
def serve_crimes():
    return send_from_directory('', 'crimes.html')

@app.route('/missao-heroi.html')
def serve_mission_hero():
    return send_from_directory('', 'missao-heroi.html')

@app.route('/heroes', methods=['POST'])
def add_hero():
    data = request.json
    hero_data = (
        data['real_name'], data['hero_name'], data['gender'], data['height'], data['weight'],
        data['birth_date'], data['birth_place'], data['powers'], data['strength_level'],
        data['popularity'], "Ativo", data['battle_history']
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO heroes (real_name, hero_name, gender, height, weight, birth_date,
                        birth_place, powers, strength_level, popularity, status, battle_history)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', hero_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Hero added successfully'}), 201

@app.route('/heroes/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM heroes WHERE id = ?', (hero_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Hero deleted successfully'}), 200

@app.route('/heroes/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
    data = request.json
    updated_data = (
        data['real_name'], data['hero_name'], data['gender'], data['height'], data['weight'],
        data['birth_date'], data['birth_place'], data['powers'], data['strength_level'],
        data['popularity'], data['battle_history'], hero_id
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE heroes
    SET real_name = ?, hero_name = ?, gender = ?, height = ?, weight = ?, birth_date = ?,
        birth_place = ?, powers = ?, strength_level = ?, popularity = ?, battle_history = ?
    WHERE id = ?
    ''', updated_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Hero updated successfully'}), 200
    
@app.route('/crimes', methods=['POST'])
def add_crime():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crimes (crime_name, crime_description, hero_id, hero_name, crime_date, crime_severity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['crime_name'], data['crime_description'], data['hero_id'], data['hero_name'], data['crime_date'],
        data['crime_severity']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Crime added successfully'}), 201

@app.route('/heroes', methods=['GET'])
def search_heroes():
    name = request.args.get('name', type=str)
    popularity = request.args.get('popularity', type=int)
    status = request.args.get('status', type=str)
    
    print(f"Received parameters - Name: {name}, Popularity: {popularity}, Status: {status}")
    
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM heroes WHERE 1=1"
    params = []
    
    if name:
        query += " AND hero_name LIKE ?"
        params.append(f"%{name}%")
    
    if popularity is not None:
        query += " AND popularity = ?"
        params.append(popularity)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    print(f"Executing query: {query} with params: {params}")
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return jsonify({'message': 'No heroes found matching the criteria'}), 404
    
    return jsonify(results)


@app.route('/crimes', methods=['GET'])
def search_crimes():
    hero_name = request.args.get('hero_name')
    crime_severity = request.args.get('crime_severity')
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
    return jsonify(results)

@app.route('/missions', methods=['POST'])
def add_mission():
    data = request.json
    mission_data = (
        data['mission_name'], data['description'], data['difficulty_level'],
        data['result'], data['rewards']
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO missions (mission_name, description, difficulty_level, result, rewards)
    VALUES (?, ?, ?, ?, ?)
    ''', mission_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mission added successfully'}), 201

@app.route('/missions', methods=['GET'])
def search_missions():
    name = request.args.get('name')
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM missions WHERE 1=1"
    params = []
    if name:
        query += " AND mission_name LIKE ?"
        params.append(f"%{name}%")
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route('/mission_heroes', methods=['POST'])
def add_hero_mission():
    data = request.json
    hero_mission_data = (
        data['hero_id'], data['mission_id'], data['mission_name'], data['hero_name'],
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO mission_heroes (hero_id, mission_id, mission_name, hero_name)
    VALUES (?, ?, ?, ?)
    ''', hero_mission_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mission linked to hero successfully'}), 201

@app.route('/missions/<int:mission_id>', methods=['PUT'])
def update_mission(mission_id):
    data = request.json
    updated_data = (
        data['mission_name'], data['description'], data['difficulty_level'],
        data['result'], data['rewards'], mission_id
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE missions
    SET mission_name = ?, description = ?, difficulty_level = ?, result = ?, rewards = ?
    WHERE id = ?
    ''', updated_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mission updated successfully'}), 200

@app.route('/missions/<int:mission_id>', methods=['DELETE'])
def delete_mission(mission_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM missions WHERE id = ?', (mission_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mission deleted successfully'}), 200

@app.route('/heroes_list', methods=['GET'])
def get_heroes_list():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, hero_name FROM heroes")
    heroes = cursor.fetchall()
    conn.close()
    return jsonify(heroes)

if __name__ == '__main__':
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        real_name TEXT NOT NULL,
        hero_name TEXT NOT NULL,
        gender TEXT,
        height REAL,
        weight REAL,
        birth_date TEXT,
        birth_place TEXT,
        powers TEXT,
        strength_level INTEGER,
        popularity INTEGER DEFAULT 0,
        status TEXT,
        battle_history TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crime_name TEXT NOT NULL,
        crime_description TEXT,
        hero_id INTEGER,
        crime_date TEXT,
        hero_name TEXT,
        crime_severity INTEGER,
        FOREIGN KEY (hero_id) REFERENCES heroes (id)
    )
    ''')
    
    # Create trigger to update hero popularity
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS update_hero_popularity
    AFTER INSERT ON crimes
    FOR EACH ROW
    BEGIN
    UPDATE heroes
    SET popularity = 
        CASE
            WHEN NEW.crime_severity BETWEEN 0 AND 10 THEN popularity - 10
            WHEN NEW.crime_severity BETWEEN 11 AND 20 THEN popularity - 20
            WHEN NEW.crime_severity BETWEEN 21 AND 30 THEN popularity - 30
            WHEN NEW.crime_severity BETWEEN 31 AND 40 THEN popularity - 40
            WHEN NEW.crime_severity BETWEEN 41 AND 50 THEN popularity - 50
            WHEN NEW.crime_severity BETWEEN 51 AND 60 THEN popularity - 60
            WHEN NEW.crime_severity BETWEEN 61 AND 70 THEN popularity - 70
            WHEN NEW.crime_severity BETWEEN 71 AND 80 THEN popularity - 80
            WHEN NEW.crime_severity BETWEEN 81 AND 90 THEN popularity - 90
            WHEN NEW.crime_severity BETWEEN 91 AND 100 THEN popularity - 100
            ELSE popularity
        END
    WHERE id = NEW.hero_id;
    END
    ''')

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS update_hero_status
    AFTER UPDATE OF popularity ON heroes
    FOR EACH ROW
    WHEN NEW.popularity <= 20
    BEGIN
        UPDATE heroes
        SET status = 'banido'
        WHERE id = NEW.id;
    END
''')
    
    conn.commit()
    conn.close()
    
    app.run(debug=True)