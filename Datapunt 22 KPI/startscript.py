# begin met:
# pip install sqlalchemy
# pip install pymsql
# pip install cryptography   

import pandas as pd
from sqlalchemy import create_engine

# Databaseconfiguratie
host = "localhost"
port = 3306  # Standaard MariaDB/MySQL-poort, kan ook 3307 zijn
database = "hr"
user = "kpidashboard"
password = "mand"
view_name = "beschikbaarheid" # de view voor jouw kpi-story

# locatie json-bestand robot
bestandspad = 'robot_restaurant_log.json'

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