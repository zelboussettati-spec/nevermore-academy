import itertools

start = 'Keuken'
cities = ['Tafel1', 'Tafel2', 'Tafel3']

distance = {
    'Keuken': {'Keuken': 0,   'Tafel1': 80,  'Tafel2': 40,  'Tafel3': 70},
    'Tafel1': {'Keuken': 80,  'Tafel1': 0,   'Tafel2': 50,  'Tafel3': 35},
    'Tafel2': {'Keuken': 40,  'Tafel1': 50,  'Tafel2': 0,   'Tafel3': 55},
    'Tafel3': {'Keuken': 70,  'Tafel1': 35,  'Tafel2': 55,  'Tafel3': 0}
}

distance2 = {
    'Keuken': {'Keuken': 0, 'Tafel1': 45, 'Tafel2': 70, 'Tafel3': 60},
    'Tafel1': {'Keuken': 45, 'Tafel1': 0, 'Tafel2': 30, 'Tafel3': 50},
    'Tafel2': {'Keuken': 70, 'Tafel1': 30, 'Tafel2': 0, 'Tafel3': 25},
    'Tafel3': {'Keuken': 60, 'Tafel1': 50, 'Tafel2': 25, 'Tafel3': 0}
}


distance3 = {
    'Keuken': {'Keuken': 0, 'Tafel1': 100, 'Tafel2': 10, 'Tafel3': 90},
    'Tafel1': {'Keuken': 100, 'Tafel1': 0, 'Tafel2': 60, 'Tafel3': 20},
    'Tafel2': {'Keuken': 10, 'Tafel1': 60, 'Tafel2': 0, 'Tafel3': 80},
    'Tafel3': {'Keuken': 90, 'Tafel1': 20, 'Tafel2': 80, 'Tafel3': 0}
}

class BruteForce:
    def __init__(self, distance, start, cities):
        self.distance = distance
        self.start = start
        self.cities = cities

    def bereken(self):
        min_distance = float('inf')
        best_route = None

        for perm in itertools.permutations(self.cities):
            route = [self.start] + list(perm) + [self.start]
            total_distance = sum(self.distance[route[i]][route[i+1]] for i in range(len(route)-1))

            # Print elke route en afstand
            print(f"Bezig met route: {route} met afstand {total_distance}")

            if total_distance < min_distance:
                min_distance = total_distance
                best_route = route

        return best_route, min_distance
    
class NearestNeighbor:
    def __init__(self, distance, start, cities):
        self.distance = distance
        self.start = start
        self.cities = cities

    def bereken(self):
        niet_bezocht = self.cities.copy()
        route = [self.start]
        huidige_stad = self.start
        totale_afstand = 0

        while niet_bezocht:
            dichtstbijzijnde = min(niet_bezocht, key=lambda stad: self.distance[huidige_stad][stad])
            totale_afstand += self.distance[huidige_stad][dichtstbijzijnde]
            route.append(dichtstbijzijnde)
            huidige_stad = dichtstbijzijnde
            niet_bezocht.remove(dichtstbijzijnde)

        totale_afstand += self.distance[huidige_stad][self.start]
        route.append(self.start)

        return route, totale_afstand
    
class FurthestNeighbor:
    def __init__(self, distance, start, cities):
        self.distance = distance
        self.start = start
        self.cities = cities

    def bereken(self):
        niet_bezocht = self.cities.copy()
        route = [self.start]
        huidige_stad = self.start
        totale_afstand = 0

        while niet_bezocht:
            verste = max(niet_bezocht, key=lambda stad: self.distance[huidige_stad][stad])
            totale_afstand += self.distance[huidige_stad][verste]
            route.append(verste)
            huidige_stad = verste
            niet_bezocht.remove(verste)

        totale_afstand += self.distance[huidige_stad][self.start]
        route.append(self.start)
        return route, totale_afstand
    
    
if __name__ == "__main__":
    print("\n*** Brute Force Algoritme ***")
    bf_solver = BruteForce(distance, start, cities)
    route_bf, dist_bf = bf_solver.bereken()
    print("Route:", route_bf)
    print("Totale afstand:", dist_bf)

    print("\n*** Nearest Neighboy Algoritme ***")
    nn_solver = NearestNeighbor(distance, start, cities)
    route_nn, dist_nn = nn_solver.bereken()
    print("Route:", route_nn)
    print("Totale afstand:", dist_nn)

    print("\n*** Furthest Neighbor ***")
    tsp_fn = FurthestNeighbor(distance, start, cities)
    route_fn, dist_fn = tsp_fn.bereken()
    print("Route:", route_fn)
    print("Totale afstand:", dist_fn)