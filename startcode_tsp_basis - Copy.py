import itertools

# Definieer de startlocatie (keuken) en de te bedienen tafels.
start = 'Keuken'
cities = ['Tafel1', 'Tafel2', 'Tafel3']

# Definieer de afstandsmatrix als een dictionary van dictionaries.
distance_3 = {
    'Keuken': {'Keuken': 0,   'Tafel1': 80,  'Tafel2': 40,  'Tafel3': 70},
    'Tafel1': {'Keuken': 80,  'Tafel1': 0,   'Tafel2': 50,  'Tafel3': 35},
    'Tafel2': {'Keuken': 40,  'Tafel1': 50,  'Tafel2': 0,   'Tafel3': 55},
    'Tafel3': {'Keuken': 70,  'Tafel1': 35,  'Tafel2': 55,  'Tafel3': 0}
}
distance_4 = {
    'Keuken': {'Keuken': 0,   'Tafel1': 65,  'Tafel2': 50,  'Tafel3': 0},
    'Tafel1': {'Keuken': 65,  'Tafel1': 0,   'Tafel2': 25,  'Tafel3': 70},
    'Tafel2': {'Keuken': 70,  'Tafel1': 40,  'Tafel2': 30,  'Tafel3': 0},
    'Tafel3': {'Keuken': 45,  'Tafel1': 50,  'Tafel2': 35,  'Tafel3': 0}
}

distance_6 = {
    'Keuken': {'Keuken': 0,   'Tafel1': 65,  'Tafel2': 50,  'Tafel3': 0},
    'Tafel1': {'Keuken': 65,  'Tafel1': 0,   'Tafel2': 25,  'Tafel3': 0},
    'Tafel2': {'Keuken': 70,  'Tafel1': 40,  'Tafel2': 30,  'Tafel3': 0},
    'Tafel3': {'Keuken': 45,  'Tafel1': 50,  'Tafel2': 35,  'Tafel3': 0}
}


# Begin met een grote afstand, zodat elke route hiermee vergeleken kan worden.
min_distance = 1000000
best_route = None

# Genereer alle mogelijke volgordes (permutations) van de tafels
for perm in list(itertools.permutations(cities)):
    route = []
    route.append(start)           # we beginnen bij de keuken
    route.extend(perm)            # bezoek de tafels in de gegeven volgorde
    route.append(start)           # keer terug naar de keuken

    print(f"Bezig met route: {route}")

    # Bereken de totale afstand voor de route
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_3[route[i]][route[i+1]]

    print(f"- afstand: {total_distance}")

    # Als deze route korter is dan de huidige kortste, slaan we deze op
    if total_distance < min_distance:
        min_distance = total_distance
        best_route = route

print(f"Kortste route: {best_route}")
print(f"Totale afstand: {min_distance}")
