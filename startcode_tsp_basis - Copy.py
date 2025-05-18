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
    'Keuken': {'Keuken': 0,   'Tafel1': 60,  'Tafel2': 45,  'Tafel3': 70,  'Tafel4': 55},
    'Tafel1': {'Keuken': 60,  'Tafel1': 0,   'Tafel2': 35,  'Tafel3': 40,  'Tafel4': 30},
    'Tafel2': {'Keuken': 45,  'Tafel1': 35,  'Tafel2': 0,   'Tafel3': 50,  'Tafel4': 20},
    'Tafel3': {'Keuken': 55,  'Tafel1': 30,  'Tafel2': 20,  'Tafel3': 25,  'Tafel4': 0}
}

distance_6 = {
    'Keuken': {'Keuken': 0,   'Tafel1': 65,  'Tafel2': 50,  'Tafel3': 70,  'Tafel4': 60,  'Tafel5': 55,  'Tafel6': 45},
    'Tafel1': {'Keuken': 65,  'Tafel1': 0,   'Tafel2': 25,  'Tafel3': 40,  'Tafel4': 35,  'Tafel5': 45,  'Tafel6': 50},
    'Tafel2': {'Keuken': 70,  'Tafel1': 40,  'Tafel2': 30,  'Tafel3': 0,   'Tafel4': 25,  'Tafel5': 30,  'Tafel6': 20},
    'Tafel3': {'Keuken': 45,  'Tafel1': 50,  'Tafel2': 35,  'Tafel3': 20,  'Tafel4': 25,  'Tafel5': 10,  'Tafel6': 0}
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
        total_distance += distance[route[i]][route[i+1]]

    print(f"- afstand: {total_distance}")

    # Als deze route korter is dan de huidige kortste, slaan we deze op
    if total_distance < min_distance:
        min_distance = total_distance
        best_route = route

print(f"Kortste route: {best_route}")
print(f"Totale afstand: {min_distance}")
