from random import randint
import requests
import sqlite3

# On utilise une API pour récupérer les données des pokémons
r = requests.get('https://pokebuildapi.fr/api/v1/pokemon')
data = r.json()

# On crée deux tables dans la base de données, une pour les pokémons et une pour les dresseurs
db = sqlite3.connect('pokemons.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pokemon(
        pokemon_id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        attack INTEGER,
        defense INTEGER,
        hp INTEGER,
        special_attack INTEGER,
        special_defense INTEGER,
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

# On insère les données des pokémons dans la base de données
for pokemon in data:
    evo = pokemon['apiEvolutions'][0]['pokedexId'] if len(pokemon['apiEvolutions']) == 1 else None
    pre_evo = pokemon['apiPreEvolution']['pokedexIdd'] if len(pokemon['apiPreEvolution']) == 2 else None 
    cursor.execute(f'''
        INSERT INTO Pokemon(pokemon_id, name, attack, defense, hp, special_attack, special_defense, speed, type1, type2, evolution, pre_evolution)
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?);
        ''', (pokemon['id'], pokemon['name'], pokemon['stats']['attack'], pokemon['stats']['defense'], pokemon['stats']['HP'], pokemon['stats']['special_attack'], pokemon['stats']['special_defense'], pokemon['stats']['speed'], pokemon['apiTypes'][0]['name'], pokemon['apiTypes'][1]['name'] if len(pokemon['apiTypes']) > 1 else None, evo, pre_evo))
    
# On crée les données des dresseurs manuellement, avec des pokémons aléatoires et on les insère dans la base de données
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

# On enregistre les changements dans la base de données
db.commit()
    
# Fonction pour récupérer un pokémon à partir de son ID
def get_pokemon_by_id(pokemon_id):
    cursor.execute('SELECT * FROM Pokemon WHERE pokemon_id = ?', (pokemon_id,))
    return cursor.fetchone()

# Fonction pour chercher un pokémon dans la base de données grâce à son nom
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

# Fonction pour récupérer un dresseur à partir de son ID
def get_trainer_by_id(query):
    cursor.execute(f'''
        SELECT * FROM Trainer WHERE trainer_id = {query};
        ''')
    return list(cursor.fetchone())

# Fonction pour chercher un dresseur dans la base de données grâce à son nom
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
    
# Fonction pour créer un nouveau dresseur
def new_trainer():
    name = input("Enter your name: ")
    pokemons = [randint(1, 898) for i in range(6)]
    cursor.execute(f'''
        INSERT INTO Trainer(name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES(? ,? ,? ,? ,? ,? ,?);
        ''', (name, pokemons[0], pokemons[1], pokemons[2], pokemons[3], pokemons[4], pokemons[5]))
    db.commit()
    print("Trainer created.")
    
# Fonction pour chercher un pokémon ou un dresseur
def search():
    query = input("What do you want to search for? (pokemon/trainer): ")
    if query.lower() == "pokemon" or query.lower() == "pokémon":
        search_pokemon()
    elif query.lower() == "trainer":
        search_trainer()
    else:
        print("Invalid input.")
        search()
        
# Formule pour calculer les dégâts pendant les combats
def calculate_damage(attacker, defender):
    damage = (50 * attacker[2] * randint(1, 101) / 100) / defender[3]
    return int(damage)

# Fonction pour lister les dresseurs
def list_trainers():
    cursor.execute('SELECT * FROM Trainer')
    trainers = cursor.fetchall()
    print("\nTrainers:")
    for trainer in trainers:
        print(f"{trainer[0]}: {trainer[1]}")
    
# Fonction pour lister les pokémons d'un dresseur
def list_pokemons_by_trainer(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    pokemons = [get_pokemon_by_id(trainer[2]), get_pokemon_by_id(trainer[3]), get_pokemon_by_id(trainer[4]), get_pokemon_by_id(trainer[5]), get_pokemon_by_id(trainer[6]), get_pokemon_by_id(trainer[7])]
    print("\nPokémons:")
    for pokemon in pokemons:
        print(f"{pokemon[0]}: {pokemon[1]}")
        
# Fonction pour simuler un combat entre deux dresseurs et leurs pokémons
def fight():
    list_trainers()
    trainer1 = get_trainer_by_id(int(input("Enter the ID of the first trainer: ")))
    trainer2 = get_trainer_by_id(int(input("Enter the ID of the second trainer: ")))
    list_pokemons_by_trainer(trainer1[0])
    pokemon1 = get_pokemon_by_id(int(input("Enter the ID of the first pokemon: ")))
    list_pokemons_by_trainer(trainer2[0])
    pokemon2 = get_pokemon_by_id(int(input("Enter the ID of the second pokemon: ")))
    print(f"\n{trainer1[1]} VS {trainer2[1]}")
    while trainer1[2] > 0 and trainer2[2] > 0:
        print(f"{pokemon1[1]} attacks {pokemon2[1]}")
        damage = calculate_damage(get_pokemon_by_id(trainer1[2]), get_pokemon_by_id(trainer2[2]))
        print(f"{pokemon2[1]} loses {damage} HP")
        trainer2[2] -= damage
        if trainer2[2] <= 0:
            print(f"{pokemon2[1]} is knocked out.")
            break
        print(f"{pokemon2[1]} attacks {pokemon1[1]}")
        damage = calculate_damage(get_pokemon_by_id(trainer2[2]), get_pokemon_by_id(trainer1[2]))
        print(f"{pokemon1[1]} loses {damage} HP")
        trainer1[2] -= damage
        if trainer1[2] <= 0:
            print(f"{pokemon1[1]} is knocked out.")
            break
    if trainer1[2] > trainer2[2]:
        print(f"{trainer1[1]} wins!")
    elif trainer2[2] > trainer1[2]:
        print(f"{trainer2[1]} wins!")
        
# Menu principal
if __name__ == '__main__':
    while True:
        print("\n1. Search\n2. New trainer\n3. Fight\n4. Exit\n")
        choice = input("What do you want to do? (int): ")
        if choice == '1':
            search()
        elif choice == '2':
            new_trainer()
        elif choice == '3':
            fight()
        elif choice == '4':
            break
        else:
            print("Invalid input.")