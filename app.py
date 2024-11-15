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

@app.route('/crimes.html')
def serve_crimes():
    return send_from_directory('', 'crimes.html')

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
    data = request.json
    crime_data = (
        data['crime_name'], data['crime_description'], data['hero_id'], data['crime_date'],
        data['hero_name'], data['crime_severity']
    )
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO crimes (crime_name, crime_description, hero_id, crime_date, hero_name, crime_severity)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', crime_data)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Crime added successfully'}), 201

@app.route('/heroes', methods=['GET'])
def search_heroes():
    name = request.args.get('name')
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM heroes WHERE 1=1"
    params = []
    if name:
        query += " AND hero_name LIKE ?"
        params.append(f"%{name}%")
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
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
        crime_severity TEXT,
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
        SET popularity = CASE
            WHEN NEW.crime_severity BETWEEN 0 AND 50 THEN 20
            WHEN NEW.crime_severity BETWEEN 51 AND 100 THEN 40
            ELSE 0
        END
        WHERE id = NEW.hero_id;
    END;
    ''')
    
    conn.commit()
    conn.close()
    
    app.run(debug=True)