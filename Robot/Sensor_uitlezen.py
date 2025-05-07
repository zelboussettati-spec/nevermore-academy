from pyfirmata2 import Arduino
import time

class Robot:
    def __init__(self, poort="COM3"):
        self.board = Arduino(poort)
        print("Arduino verbonden")
        self.board.samplingOn(100)

        # Motoren
        self.motor_rechts = self.board.get_pin("d:3:p")
        self.motor_links = self.board.get_pin("d:11:p")

        # Sensoren
        self.sensoren = {
            1: self.board.get_pin("a:1:i"),  # L1
            2: self.board.get_pin("a:2:i"),  # L2
            3: self.board.get_pin("a:3:i"),  # M
            4: self.board.get_pin("a:4:i"),  # R2
            5: self.board.get_pin("a:5:i")   # R1
        }
        self.sensor_waarden = {i: 0 for i in range(1, 6)}
        self.drempelwaarde = 0.5

        # Register callbacks
        for i in range(1, 6):
            self.sensoren[i].register_callback(lambda v, i=i: self.sensor_waarden.update({i: 1 if v > self.drempelwaarde else 0}))
            self.sensoren[i].enable_reporting()

        # Routeplan
        self.routeplan = ["links", "rechtdoor", "rechts", "stop"]
        self.kruispunt_teller = 0
        self.laatste_kruispunt = 0

    # Motor aansturen
    def stel_motorsnelheid_in(self, rechts, links):
        self.motor_rechts.write(rechts)
        self.motor_links.write(links)

    def stop(self):
        self.stel_motorsnelheid_in(0, 0)
        time.sleep(0.05)

    # Kleine acties
    def stap_vooruit(self):
        self.stel_motorsnelheid_in(0.2, 0.2)
        time.sleep(0.1)
        self.stop()

    def draai_links(self):
        self.stel_motorsnelheid_in(0.15, 0.2)
        time.sleep(0.1)
        self.stop()

    def draai_rechts(self):
        self.stel_motorsnelheid_in(0.2, 0.15)
        time.sleep(0.1)
        self.stop()

    def draai_scherp_links(self):
        self.stel_motorsnelheid_in(0.1, 0.2)
        time.sleep(0.12)
        self.stop()

    def draai_scherp_rechts(self):
        self.stel_motorsnelheid_in(0.2, 0.1)
        time.sleep(0.12)
        self.stop()

    def maak_bocht(self, richting):
        if richting == "links":
            self.stel_motorsnelheid_in(0.15, 0.3)
        elif richting == "rechts":
            self.stel_motorsnelheid_in(0.3, 0.15)
        elif richting == "rechtdoor":
            self.stel_motorsnelheid_in(0.2, 0.2)
        elif richting == "stop":
            self.stop()
        time.sleep(0.7)
        self.stop()

    # Kruispuntherkenning
    def is_kruispunt(self, patroon):
        return tuple(patroon) in [
            (1, 1, 1, 1, 1),    # vierwegkruising
            (0, 1, 1, 1, 0),    # T-splitsing
            (1, 1, 1, 0, 0),    # doodlopend links
            (0, 0, 1, 1, 1)     # doodlopend rechts
        ]

    # Interpretatie van patronen (volgens reader)
    def verwerk_sensorpatroon(self, patroon):
        match tuple(patroon):
            case (0, 0, 0, 0, 0) | (1, 1, 1, 1, 1):
                self.stop()
            case (0, 1, 0, 1, 0) | (1, 1, 0, 1, 1) | (1, 1, 0, 1, 0) | (0, 1, 0, 1, 1):
                self.stap_vooruit()
            case (1, 0, 1, 1, 1) | (1, 0, 0, 1, 1) | (0, 0, 1, 1, 1):
                self.draai_rechts()
            case (0, 1, 1, 1, 1) | (0, 0, 0, 1, 1) | (0, 0, 0, 1, 0) | (1, 0, 0, 0, 1):
                self.draai_scherp_rechts()
            case (1, 1, 1, 0, 1) | (1, 1, 1, 0, 0) | (1, 1, 0, 0, 1) | (1, 0, 1, 0, 0):
                self.draai_links()
            case (1, 1, 1, 1, 0) | (1, 0, 0, 0, 0) | (1, 0, 0, 1, 0) | (0, 1, 0, 0, 0):
                self.draai_scherp_links()
            case _:
                self.stap_vooruit()

    # Hoofdlus
    def start(self):
        while True:
            patroon = [self.sensor_waarden[i] for i in range(1, 6)]
            print(f"Sensorpatroon: {patroon}")
            self.stop()
            time.sleep(0.05)

            tijd = time.time()
            if self.is_kruispunt(patroon) and tijd - self.laatste_kruispunt > 1.5 and self.kruispunt_teller < len(self.routeplan):
                actie = self.routeplan[self.kruispunt_teller]
                self.kruispunt_teller += 1
                self.laatste_kruispunt = tijd
                print(f"Kruispunt {self.kruispunt_teller} → Actie: {actie}")
                self.maak_bocht(actie)
            else:
                self.verwerk_sensorpatroon(patroon)


if __name__ == "__main__":
    robot = Robot()
    robot.start()
