from pyfirmata2 import Arduino
import time

# maakt verbinding met de Arduino op COM3
board = Arduino("COM3")

print("Arduino gestart")
board.samplingOn(100)  # zet sample op 100ms

# motoren
motorrechts = board.get_pin("d:3:p")
motorlinks = board.get_pin("d:11:p")

# sensoren koppelen aan specifieke pinnen
sensor_links = board.get_pin("a:1:i")
sensor_linksmidden = board.get_pin("a:2:i")
sensor_midden = board.get_pin("a:3:i")
sensor_rechtsmidden = board.get_pin("a:4:i")
sensor_rechts = board.get_pin("a:5:i")

# dictionary om sensorwaarden op te slaan
sensor_values = {
    'sensor_1': 0,
    'sensor_2': 0,
    'sensor_3': 0,
    'sensor_4': 0,
    'sensor_5': 0
}

# threshold waarde instellen
threshold = 0.5

# callback functies
def IR_callback1(value):
    sensor_values['sensor_1'] = 1 if value > threshold else 0

def IR_callback2(value):
    sensor_values['sensor_2'] = 1 if value > threshold else 0

def IR_callback3(value):
    sensor_values['sensor_3'] = 1 if value > threshold else 0

def IR_callback4(value):
    sensor_values['sensor_4'] = 1 if value > threshold else 0

def IR_callback5(value):
    sensor_values['sensor_5'] = 1 if value > threshold else 0

# callbacks registreren en reporting inschakelen
sensor_links.register_callback(IR_callback1)
sensor_links.enable_reporting()

sensor_linksmidden.register_callback(IR_callback2)
sensor_linksmidden.enable_reporting()

sensor_midden.register_callback(IR_callback3)
sensor_midden.enable_reporting()

sensor_rechtsmidden.register_callback(IR_callback4)
sensor_rechtsmidden.enable_reporting()

sensor_rechts.register_callback(IR_callback5)
sensor_rechts.enable_reporting()



# functie voor motorsnelheid
def set_motor_speed(rechts_speed, links_speed):
    motorrechts.write(rechts_speed)
    motorlinks.write(links_speed)




def sensorrichting():
    sensor_value_tuple = tuple(sensor_values[f'sensor_{i}'] for i in range(1, 6))

    rechtdoor_combo = [
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1),
        (0, 0, 0, 1, 1),
        (0, 0, 1, 0, 0),
        (0, 1, 0, 1, 1),
        (1, 0, 0, 0, 0),
        (1, 0, 0, 0, 1),
        (1, 0, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (1, 1, 0, 1, 1),

        (0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0)
    ]
    kort_links_combo = [
        (0, 0, 1, 1, 0),    #misschien aanpassen
        (1, 1, 1, 0, 1),
        (1, 0, 0, 1, 1),
        (1, 1, 0, 1, 0),
        (1, 0, 1, 1, 0),
        (1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1),
        (0, 1, 1, 0, 0),
        (1, 1, 1, 0, 1),
    ]
    scherpe_links = [
        (0, 1, 1, 1, 1),
        (0, 0, 1, 1, 1),
    ]
    korte_rechts_combo = [
        (0, 1, 1, 0, 1),
        (1, 1, 0, 0, 1),
        (1, 0, 1, 1, 1),
        (0, 1, 0, 0, 1),
        (0, 1, 0, 0, 0),
        (0, 0, 0, 1, 0),
        (1, 1, 1, 0, 0),
        (1, 1, 0, 0, 0)
    ]
    scherpe_rechts = [
        (1, 1, 1, 1, 0),
        (1, 1, 1, 0, 0),
    ]
    stop= [
        (1, 1, 1, 1, 1),
    ]

    if sensor_value_tuple in rechtdoor_combo:
        return "rechtdoor"
    elif sensor_value_tuple in kort_links_combo:
        return "kort links"
    elif sensor_value_tuple in korte_rechts_combo:
        return "kort rechts"
    elif sensor_value_tuple in scherpe_links:
        return "scherp links"
    elif sensor_value_tuple in scherpe_rechts:
        return "scherpe rechts"
    elif sensor_value_tuple in stop:
        return "robot kwijt"
    else:
        return "stop"
# Plaats deze variabelen buiten de loop zodat ze behouden blijven
opgeslagen_patronen = []  # lijst voor unieke sensorpatronen
vorige_patroon = [0, 0, 0, 0, 0]  # beginwaarde voor vorige patroon

while True:
    # Lees de huidige sensorwaarden
    sensor_waarden = [
        sensor_values.get(f'sensor_{i}', 0)
        for i in range(1, 6)
    ]
    
    time.sleep(0.01)
    
    # Sla nieuw patroon op als het nog niet in de lijst staat
    if sensor_waarden not in opgeslagen_patronen:
        opgeslagen_patronen.append(sensor_waarden.copy())
        print(f"Nieuw patroon opgeslagen: {sensor_waarden}")
    
    # DEBUG info
    print("Sensor status:", sensor_waarden)
    print(f"Links:        {sensor_values['sensor_1']}")
    print(f"Linksmidden:  {sensor_values['sensor_2']}")
    print(f"Midden:       {sensor_values['sensor_3']}")
    print(f"Rechtsmidden: {sensor_values['sensor_4']}")
    print(f"Rechts:       {sensor_values['sensor_5']}")
    print("------")
    
    # ACTIE op basis van huidig en vorig patroon
    if sensor_waarden == [1, 1, 1, 1, 1] and vorige_patroon in [
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1]
    ]:
        print(f"Speciale actie voor vorige patroon {vorige_patroon}")
        set_motor_speed(0.1, 0.02)
    else:
        richting = sensorrichting()
        if richting == "rechtdoor":
            set_motor_speed(0.2, 0.2)
        elif richting == "kort links": 
            set_motor_speed(0.2, 0.125)
        elif richting == "kort rechts":
            set_motor_speed(0.125, 0.2)
        elif richting == "scherp links":
            set_motor_speed(0.2, 0.025)
        elif richting == "scherpe rechts": 
            set_motor_speed(0.025, 0.2)
        elif richting == "robot kwijt":
            set_motor_speed(0.0, 0.0)
        else:
            set_motor_speed(0.0, 0.0)
    
    # Update vorige patroon voor de volgende iteratie
    vorige_patroon = sensor_waarden.copy()
