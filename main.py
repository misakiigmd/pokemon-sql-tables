from random import randint
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
        trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    {'name': 'Ash', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)},
    {'name': 'Blue', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)},
    {'name': 'Marnie', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)},
    {'name': 'May', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)},
    {'name': 'Serena', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)},
    {'name': 'Silver', 'pokemon1': randint(1, 898), 'pokemon2': randint(1, 898), 'pokemon3': randint(1, 898), 'pokemon4': randint(1, 898), 'pokemon5': randint(1, 898), 'pokemon6': randint(1, 898)}
]

for trainer in trainer_list:
    cursor.execute(f'''
        INSERT INTO Trainer(name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES(? ,? ,? ,? ,? ,? ,?);
        ''', (trainer['name'], trainer['pokemon1'], trainer['pokemon2'], trainer['pokemon3'], trainer['pokemon4'], trainer['pokemon5'], trainer['pokemon6']))

db.commit()
    
def get_pokemon_by_id(pokemon_id):
    cursor.execute('SELECT * FROM Pokemon WHERE pokemon_id = ?', (pokemon_id,))
    return cursor.fetchone()

def get_trainer_by_id(query):
    cursor.execute(f'''
        SELECT * FROM Trainer WHERE trainer_id = {query};
        ''')
    return cursor.fetchone()

def search_pokemon():
    query = input("Enter a pokémon to search for: ")
    result = cursor.execute(f"SELECT * FROM Pokemon WHERE name LIKE '%{query}%'")
    result = result.fetchall()
    if len(result) == 0:
        print("No result.")
        search_pokemon()
    elif len(result) == 1:
        result = result[0]
    else: 
        for r in range(len(result)) : 
            print(f'{r}: {result[r][1]}')
        query = int(input("What pokémon are you looking for? (int): "))
        result = result[query]
    evo = get_pokemon_by_id(result[10])
    pre_evo = get_pokemon_by_id(result[11])
    print(f'''
    Pokédex ID: {result[0]}
    Name: {result[1]}
    Attack: {result[2]}
    Defense: {result[3]}
    HP: {result[4]}
    Special Attack: {result[5]}
    Special Defense: {result[6]}
    Speed: {result[7]}
    Type(s): {result[8]}, {result[9]}
    Evolution: {evo[1] if evo else None}
    Pre-evolution: {pre_evo[1] if pre_evo else None}
    ''')

def search_trainer(): 
    query = input('Enter a trainer: ')
    result = cursor.execute(f"SELECT * FROM trainer WHERE name LIKE '%{query}%'")
    result = result.fetchall()
    if len(result) == 0:
        print("aucun résultat")
    elif len(result) == 1:
        result = result[0]
    else: 
        for r in range(len(result)): 
            print(f'{r}: {result[r][1]}')
        query = int(input("What trainer are you looking for? (int): "))
        result = result[query]
    
    print(f"""
    Name: {result[1]}
    Pokémon 1: {get_pokemon_by_id(result[2])[1]}
    Pokémon 2: {get_pokemon_by_id(result[3])[1]}
    Pokémon 3: {get_pokemon_by_id(result[4])[1]}
    Pokémon 4: {get_pokemon_by_id(result[5])[1]}
    Pokémon 5: {get_pokemon_by_id(result[6])[1]}
    Pokémon 6: {get_pokemon_by_id(result[7])[1]}
    """)

def new_trainer():
    name = input("Enter your name: ")
    pokemons = [randint(1, 898) for i in range(6)]
    cursor.execute(f'''
        INSERT INTO Trainer(name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES(? ,? ,? ,? ,? ,? ,?);
        ''', (name, pokemons[0], pokemons[1], pokemons[2], pokemons[3], pokemons[4], pokemons[5]))
    db.commit()
    
new_trainer()