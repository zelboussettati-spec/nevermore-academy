from pyfirmata2 import Arduino
import time

class Robot:
    def __init__(self, poort="COM3"):
        self.board = Arduino(poort)
        print("Arduino verbonden")
        self.board.samplingOn(100)

        self.motor_rechts = self.board.get_pin("d:3:p")
        self.motor_links = self.board.get_pin("d:11:p")

        self.sensoren = {
            1: self.board.get_pin("a:1:i"),
            2: self.board.get_pin("a:2:i"),
            3: self.board.get_pin("a:3:i"),
            4: self.board.get_pin("a:4:i"),
            5: self.board.get_pin("a:5:i")
        }
        self.sensor_waarden = {i: 1 for i in range(1, 6)}  # 1 = wit, 0 = zwart
        self.drempelwaarde = 0.5

        for i in range(1, 6):
            self.sensoren[i].register_callback(
                lambda v, i=i: self.sensor_waarden.update({i: 1 if v > self.drempelwaarde else 0})
            )
            self.sensoren[i].enable_reporting()

        self.routeplan = ["rechtdoor", "rechts", "rechts" "stop"]
        self.kruispunt_teller = 0
        self.laatste_kruispunt = 0

    def stel_motorsnelheid_in(self, rechts, links):
        self.motor_rechts.write(rechts)
        self.motor_links.write(links)

    def stop(self):
        self.stel_motorsnelheid_in(0, 0)
        time.sleep(0.05)

    def stap_vooruit(self):
        self.stel_motorsnelheid_in(0.2, 0.2)
        time.sleep(0.12)
        self.stop()

    def draai_scherp_links(self):
        self.stel_motorsnelheid_in(0.3, 0.05)
        time.sleep(0.12)
        self.stop()

    def draai_scherp_rechts(self):
        self.stel_motorsnelheid_in(0.05, 0.3)
        time.sleep(0.12)
        self.stop()

    def maak_bocht(self, richting):
        if richting == "stop":
            self.stop()
            return

        # FASE 1: korte stop
        self.stop()
        time.sleep(0.5)

        # FASE 2: draai tot patroon (1,1,0,1,1) wordt gezien
        max_stappen = 25
        stappen = 0
        while stappen < max_stappen:
            patroon = [self.sensor_waarden[i] for i in range(1, 6)]
            if tuple(patroon) == (1, 1, 0, 1, 1):
                break
            if richting == "rechtdoor":
                self.stap_vooruit()
            elif richting == "links":
                self.draai_scherp_links()
            elif richting == "rechts":
                self.draai_scherp_rechts()
            stappen += 1


    def is_kruispunt(self, patroon):
        return tuple(patroon) in [
            (0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1),
            (0, 1, 0, 1, 0),
            (0, 0, 0, 1, 1),
            (1, 1, 0, 0, 0)
        ]

    def verwerk_sensorpatroon(self, patroon):
        match tuple(patroon):
            case (1, 1, 1, 1, 1) | (0, 0, 0, 0, 0):  # Geen lijn of alles lijn
                self.stop()
            case (1, 0, 1, 0, 1) | (0, 0, 1, 0, 0) | (0, 0, 1, 0, 1) | (1, 0, 1, 0, 0):
                self.stap_vooruit()
            case (0, 1, 0, 0, 0) | (0, 1, 1, 0, 0) | (1, 1, 0, 0, 0):
                self.stel_motorsnelheid_in(0.2, 0.15)
            case (1, 0, 0, 0, 0) | (1, 1, 1, 0, 0) | (1, 1, 1, 0, 1) | (0, 1, 1, 1, 0) |(1, 1, 1, 1, 0):
                self.draai_scherp_rechts()
            case (0, 0, 0, 1, 1) | (0, 0, 0, 1, 0) | (0, 0, 1, 1, 0) | (0, 0, 0, 0, 1):
                self.stel_motorsnelheid_in(0.15, 0.2)
            case (0, 0, 0, 0, 1) | (0, 1, 1, 1, 1) | (0, 1, 1, 0, 0) | (0, 0, 0, 1, 1):
                self.draai_scherp_links()
            case _:
                self.stap_vooruit()

    def start(self):
        while True:
            patroon = [self.sensor_waarden[i] for i in range(1, 6)]
            print(f"Sensorpatroon: {patroon}")
            self.stop()
            time.sleep(0.05)

            tijd = time.time()
            if self.is_kruispunt(patroon) and tijd - self.laatste_kruispunt > 1.5 and self.kruispunt_teller < len(self.routeplan):
                actie = self.routeplan[self.kruispunt_teller]
                print(f"Kruispunt {self.kruispunt_teller + 1} → Actie: {actie}")
                self.maak_bocht(actie)
                self.kruispunt_teller += 1
                self.laatste_kruispunt = tijd
            else:
                self.verwerk_sensorpatroon(patroon)

if __name__ == "__main__":
    robot = Robot()
    robot.start()
