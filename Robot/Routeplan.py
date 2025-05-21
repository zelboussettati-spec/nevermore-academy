class RoutePlanner:
    def __init__(self):
        self.routes = {
            6: ["rechts", "links", "rechtdoor"],
            5: ["links", "links", "rechts", "rechts"],
            7: ["rechtdoor", "rechts", "rechtdoor", "links"]
        }

    def get_route(self, tafelnummer):
        return self.routes.get(tafelnummer, [])

    def combineer_routes(self, tafels):
        volledige_route = []
        for tafel in tafels:
            volledige_route += self.get_route(tafel)
        volledige_route.append("stop")
        return volledige_route
