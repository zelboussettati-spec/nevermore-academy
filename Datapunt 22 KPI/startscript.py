import pandas as pd
from sqlalchemy import create_engine

# Database connectie
host = "localhost"
port = 3306
database = "hr"
user = "kpidashboard"
password = "VeiligWachtwoord123"
view_name = "view_klanttevredenheid_jonge_klanten"

# locatie json-bestand robot en excel bestand
robot_file = "robot_restaurant_log.json"
excel_file = "besteldata.xlsx"

# Maak een databaseverbinding met SQLAlchemy en pymysql
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Query de view en laad deze in een DataFrame
try:
    df = pd.read_sql(f"SELECT * FROM {view_name}", con=engine)
    print(df.head())
except Exception as e:
    print("Fout bij ophalen van data:", e)


# Inlezen van het JSON-bestand in een DataFrame
df2 = pd.read_json(bestandspad)

# Toon de eerste paar regels van het DataFrame
print(df2.head())