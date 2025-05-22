import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from datetime import datetime

# Databaseconnectie
host = "localhost"
port = 3306
database = "hr"
user = "kpidashboard"
password = "VeiligWachtwoord123"
view_name = "view_klanttevredenheid_jonge_klanten"

# Robotlog en Excel-bestand
robot_file = "robot_restaurant_log.json"
excel_file = "besteldata.xlsx"

# Verbinding met database
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

try:
    df_human = pd.read_sql(f"SELECT * FROM {view_name}", con=engine)
except Exception as e:
    print("Fout bij ophalen SQL-view:", e)
    df_human = pd.DataFrame()

# Inlezen robotdata
try:
    df_robot = pd.read_json(robot_file)
except Exception as e:
    print("Fout bij lezen robotlog:", e)
    df_robot = pd.DataFrame()

# Robotdata voorbereiden
if not df_robot.empty:
    df_robot["Date_str"] = pd.to_datetime(df_robot["Date"]).dt.strftime("%d-%m-%Y")
    df_robot["Datetime_Picked"] = pd.to_datetime(df_robot["Date_str"] + " " + df_robot["Time_Picked"], format="%d-%m-%Y %H:%M:%S", errors='coerce')
    df_robot["Birth_Date"] = pd.to_datetime(df_robot["Birth_Date"], format="%d-%m-%Y", errors='coerce')
    df_robot["Age"] = (df_robot["Datetime_Picked"] - df_robot["Birth_Date"]).dt.days // 365
    robot_young = df_robot[(df_robot["Age"] <= 45) & (df_robot["Rating"].apply(lambda x: isinstance(x, (int, float))))]
    avg_robot = robot_young["Rating"].mean()
else:
    avg_robot = None

# Inlezen en verwerken Excel-besteldata
try:
    besteldata = pd.read_excel(excel_file)

    # Converteer datumkolommen 
    besteldata["Birth_Date"] = pd.to_datetime(besteldata["Birth_Date"], dayfirst=True, errors='coerce')
    besteldata["Date"] = pd.to_datetime(besteldata["Date"], dayfirst=True, errors='coerce')

    # Leeftijd berekenen
    besteldata["Age"] = (besteldata["Date"] - besteldata["Birth_Date"]).dt.days // 365

    # Filter op jonge klanten (≤ 45 jaar) met geldige beoordeling
    human_young = besteldata[
        (besteldata["Age"] <= 45) &
        (besteldata["Rating"].apply(lambda x: isinstance(x, (int, float))))
    ]

    # Gemiddelde berekenen
    avg_human = human_young["Rating"].mean()

except Exception as e:
    print("Fout bij lezen of verwerken besteldata:", e)
    avg_human = None

# Visualisatie: Robot vs Bediening
labels = ['Bediening', 'Robot']
scores = [avg_human if avg_human is not None else 0, avg_robot if avg_robot is not None else 0]

plt.bar(labels, scores, color=['steelblue', 'seagreen'])
plt.ylim(0, 10)
plt.ylabel("Gemiddelde klanttevredenheid (1-10)")
plt.title("Klanttevredenheid bij jonge klanten (≤ 45 jaar)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
