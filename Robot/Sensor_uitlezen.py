from pyfirmata2 import Arduino
import time

# Arduino setup
board = Arduino("COM3")
print("Arduino gestart")
board.samplingOn(100)

# Motoren
motor_rechts = board.get_pin("d:3:p")
motor_links = board.get_pin("d:11:p")

# Sensoren
sensoren = {
    1: board.get_pin("a:1:i"),
    2: board.get_pin("a:2:i"),
    3: board.get_pin("a:3:i"),
    4: board.get_pin("a:4:i"),
    5: board.get_pin("a:5:i")
}
sensor_waarden = {i: 0 for i in range(1, 6)}
drempelwaarde = 0.5

# Sensor callbacks
for i in range(1, 6):
    sensoren[i].register_callback(lambda v, i=i: sensor_waarden.update({i: 1 if v > drempelwaarde else 0}))
    sensoren[i].enable_reporting()

# Motorsnelheid instellen
def stel_motorsnelheid_in(rechts, links):
    motor_rechts.write(rechts)
    motor_links.write(links)

def stop():
    stel_motorsnelheid_in(0, 0)

# Micro-acties
def stap_vooruit():
    stel_motorsnelheid_in(0.2, 0.2)
    time.sleep(0.1)
    stop()

def draai_links():
    stel_motorsnelheid_in(0.15, 0.2)
    time.sleep(0.1)
    stop()

def draai_rechts():
    stel_motorsnelheid_in(0.2, 0.15)
    time.sleep(0.1)
    stop()

def draai_scherp_links():
    stel_motorsnelheid_in(0.1, 0.2)
    time.sleep(0.12)
    stop()

def draai_scherp_rechts():
    stel_motorsnelheid_in(0.2, 0.1)
    time.sleep(0.12)
    stop()

# Bochten maken bij kruispunten
def maak_bocht(richting):
    if richting == "links":
        stel_motorsnelheid_in(0.15, 0.3)
    elif richting == "rechts":
        stel_motorsnelheid_in(0.3, 0.15)
    elif richting == "rechtdoor":
        stel_motorsnelheid_in(0.2, 0.2)
    elif richting == "stop":
        stop()
    time.sleep(0.7)
    stop()

# Routeplan
routeplan = ["links", "rechtdoor", "rechts", "stop"]
kruispunt_teller = 0
laatste_kruispunt = 0

# Hoofdloop
while True:
    patroon = [sensor_waarden[i] for i in range(1, 6)]
    print(f"Sensorpatroon: {patroon}")

    stop()
    time.sleep(0.05)

    tijd = time.time()

    # Kruispuntherkenning
    vierwegkruising = sum(patroon) == 5
    tsplitsing_links = patroon == [0, 1, 1, 1, 0]
    doodlopende_weg = patroon == [1, 1, 1, 0, 0] or patroon == [0, 0, 1, 1, 1]

    if (vierwegkruising or tsplitsing_links or doodlopende_weg) and tijd - laatste_kruispunt > 1.5 and kruispunt_teller < len(routeplan):
        actie = routeplan[kruispunt_teller]
        kruispunt_teller += 1
        laatste_kruispunt = tijd
        print(f"Kruispunt {kruispunt_teller} gedetecteerd → Actie: {actie}")
        maak_bocht(actie)
        continue

    # Volledige patronenlijst:
    if patroon in [(1,1,0,1,1), (1,1,0,1,0), (0,1,0,1,1), (0,1,0,1,0)]:
        stap_vooruit()
    elif patroon in [(1,0,1,1,1), (0,0,1,1,1), (1,0,0,1,1)]:
        draai_rechts()
    elif patroon == [0,1,1,1,1]:
        draai_scherp_rechts()
    elif patroon in [(1,1,1,0,1), (0,0,0,1,0), (1,1,1,0,0), (1,1,0,0,1)]:
        draai_links()
    elif patroon == [1,1,1,1,0]:
        draai_scherp_links()
    else:
        print("Onbekend patroon, wacht kort")
        stop()
        time.sleep(0.1)
