import random
import requests
import sqlite3

r = requests.get('https://pokebuildapi.fr/api/v1/pokemon')
data = r.json()

db = sqlite3.connect('pokemons.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pokemon(
        pokemon_id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        atk INTEGER,
        def INTEGER,
        hp INTEGER,
        sp_atk INTEGER,
        sp_def INTEGER,
        speed INTEGER,
        type1 VARCHAR(255),
        type2 VARCHAR(255),
        evolution INTEGER,
        pre_evolution INTEGER,
        FOREIGN KEY(evolution) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pre_evolution) REFERENCES Pokemon(pokemon_id)
    );
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trainer(
        trainer_id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        pokemon1 INTEGER,
        pokemon2 INTEGER,
        pokemon3 INTEGER,
        pokemon4 INTEGER,
        pokemon5 INTEGER,
        pokemon6 INTEGER,
        FOREIGN KEY(pokemon1) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pokemon2) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pokemon3) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pokemon4) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pokemon5) REFERENCES Pokemon(pokemon_id),
        FOREIGN KEY(pokemon6) REFERENCES Pokemon(pokemon_id)
    );
    ''')

for pokemon in data:
    evo = pokemon['apiEvolutions'][0]['pokedexId'] if len(pokemon['apiEvolutions']) == 1 else None
    pre_evo = pokemon['apiPreEvolution']['pokedexIdd'] if len(pokemon['apiPreEvolution']) == 2 else None 
    cursor.execute(f'''
        INSERT INTO Pokemon(pokemon_id, name, atk, def, hp, sp_atk, sp_def, speed, type1, type2, evolution, pre_evolution)
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?);
        ''', (pokemon['id'], pokemon['name'], pokemon['stats']['attack'], pokemon['stats']['defense'], pokemon['stats']['HP'], pokemon['stats']['special_attack'], pokemon['stats']['special_defense'], pokemon['stats']['speed'], pokemon['apiTypes'][0]['name'], pokemon['apiTypes'][1]['name'] if len(pokemon['apiTypes']) > 1 else None, evo, pre_evo))
    
trainer_list = [
    {'trainer_id': 1, 'name': 'Ash', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
    {'trainer_id': 2, 'name': 'Blue', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
    {'trainer_id': 3, 'name': 'Marnie', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
    {'trainer_id': 4, 'name': 'May', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
    {'trainer_id': 5, 'name': 'Serena', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
    {'trainer_id': 6, 'name': 'Silver', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)}
]

for trainer in trainer_list:
    cursor.execute(f'''
        INSERT INTO Trainer(trainer_id, name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES(? ,? ,? ,? ,? ,? ,? ,?);
        ''', (trainer['trainer_id'], trainer['name'], trainer['pokemon1'], trainer['pokemon2'], trainer['pokemon3'], trainer['pokemon4'], trainer['pokemon5'], trainer['pokemon6']))

def search_pokemon(query):
    cursor.execute(f'''
        SELECT * FROM Pokemon WHERE name LIKE '%{query}%';
        ''')
    return cursor.fetchall()

    # pokemon = cursor.fetchall()
    # print(f'''
    # Pokemon ID: {pokemon[0][0]}
    # Name: {pokemon[0][1]}
    # Attack: {pokemon[0][2]}
    # Defense: {pokemon[0][3]}
    # HP: {pokemon[0][4]}
    # Special Attack: {pokemon[0][5]}
    # Special Defense: {pokemon[0][6]}
    # Speed: {pokemon[0][7]}
    # Type 1: {pokemon[0][8]}
    # Type 2: {pokemon[0][9]}
    # Evolution: {pokemon[0][10]}
    # Pre Evolution: {pokemon[0][11]}
    # ''')

def search_trainer(query):
    cursor.execute(f'''
        SELECT * FROM Trainer WHERE name LIKE '%{query}%';
        ''')
    return cursor.fetchall()
    
    # trainer = cursor.fetchall()
    # print(f'''
    # Trainer ID: {trainer[0][0]}
    # Name: {trainer[0][1]}
    # Pokemon 1: {trainer[0][2]}
    # Pokemon 2: {trainer[0][3]}
    # Pokemon 3: {trainer[0][4]}
    # Pokemon 4: {trainer[0][5]}
    # Pokemon 5: {trainer[0][6]}
    # Pokemon 6: {trainer[0][7]}
    # ''')
    
def get_pokemon_by_id(pokemon_id):
    cursor.execute('SELECT * FROM Pokemon WHERE pokemon_id = ?', (pokemon_id,))
    return cursor.fetchone()

def get_trainer_by_id(query):
    cursor.execute(f'''
        SELECT * FROM Trainer WHERE trainer_id = {query};
        ''')
    return cursor.fetchone()

search_pokemon('Pikachu')
search_trainer('Ash')
get_pokemon_by_id(25)
get_trainer_by_id(1)

db.commit()
db.close()