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
    cursor.execute(f'''
        INSERT INTO Pokemon(pokemon_id, name, atk, def, hp, sp_atk, sp_def, speed, type1, type2, evolution, pre_evolution)
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?);
        ''', (pokemon['id'], pokemon['name'], pokemon['stats']['attack'], pokemon['stats']['defense'], pokemon['stats']['HP'], pokemon['stats']['special_attack'], pokemon['stats']['special_defense'], pokemon['stats']['speed'], pokemon['apiTypes'][0]['name'], pokemon['apiTypes'][1]['name'] if len(pokemon['apiTypes']) > 1 else None, pokemon['apiEvolutions'][0]['pokedexId'] if len('apiEvolutions') == 1 else None, pokemon['apiPreEvolution'][0]['pokedexIdd'] if len('apiPreEvolution') == 1 else None))
    
# List of trainers (including Ash, Blue, May, Silver, Serena and Marnie) with randomly generated pokemons,;

trainer_list = [
    {'name': 'Ash', 'pokemon1': random.randint(1, 898), 'pokemon2': random.randint(1, 898), 'pokemon3': random.randint(1, 898), 'pokemon4': random.randint(1, 898), 'pokemon5': random.randint(1, 898), 'pokemon6': random.randint(1, 898)},
]
db.commit()