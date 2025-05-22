import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Bestandspaden
robot_file = "C:/Users/faysa/OneDrive - Windesheim Office365/HBO-ICT/ICT 1e jaars periode 2/Bestelrobot VS/m2-2/Datapunt 22 KPI/robot_restaurant_log_week_cleaned.json"
medewerkers_file = "C:/Users/faysa/OneDrive - Windesheim Office365/HBO-ICT/ICT 1e jaars periode 2/Bestelrobot VS/m2-2/Datapunt 22 KPI/besteldata.xlsx"

# Databaseconnectie (MySQL)
host = "localhost"
port = 3306
database = "hr"
user = "kpidashboard"
password = "VeiligWachtwoord123"

def maak_engine():
    engine_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(engine_str)

def laad_view(view_name):
    try:
        engine = maak_engine()
        df_view = pd.read_sql(f"SELECT * FROM {view_name}", con=engine)
        print(f"[INFO] View '{view_name}' succesvol geladen:")
        print(df_view.head())
        return df_view
    except Exception as e:
        print(f"[FOUT] Laden view '{view_name}': {e}")
        return pd.DataFrame()

def laad_data():
    try:
        df_robot = pd.read_json(robot_file)
        print("[INFO] Robotlog geladen:")
        print(df_robot.head())
    except Exception as e:
        print(f"[FOUT] Robotlog laden mislukt: {e}")
        df_robot = pd.DataFrame()

    try:
        df_mens = pd.read_excel(medewerkers_file)
        print("[INFO] Medewerkersbestand geladen:")
        print(df_mens.head())
    except Exception as e:
        print(f"[FOUT] Medewerkersbestand laden mislukt: {e}")
        df_mens = pd.DataFrame()

    # Voorbereiding
    for df in [df_robot, df_mens]:
        df["Birth_Date"] = pd.to_datetime(df["Birth_Date"], dayfirst=True, errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["Age"] = (df["Date"] - df["Birth_Date"]).dt.days // 365
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
        df["Total_Amount"] = pd.to_numeric(df["Total_Amount"], errors="coerce")

    return df_robot, df_mens

# KPI 1: Klanttevredenheid bediening van jonge klanten (<=45):
def bereken_kpi1(df_robot, df_mens):
    young_robot = df_robot[df_robot["Age"] <= 45]
    young_mens = df_mens[df_mens["Age"] <= 45]
    
    print("\nKPI 1: Klanttevredenheid bediening van jonge klanten (<=45)")
    print("Aantal jonge klanten (robot):", df_robot[df_robot["Age"] <= 45].shape[0])
    print("Gem. beoordeling (robot, ≤ 45):", df_robot[df_robot["Age"] <= 45]["Rating"].mean())

    print("\nAantal jonge klanten (mens):", df_mens[df_mens["Age"] <= 45].shape[0])
    print("Gem. beoordeling (mens, ≤ 45):", df_mens[df_mens["Age"] <= 45]["Rating"].mean())

    return young_robot["Rating"].mean(), young_mens["Rating"].mean()

# KPI 3: Aantal opgepikte orders per uur: 
def figuur_kpi3(df_robot, df_mens):
    df_robot["Time_Picked"] = pd.to_datetime(df_robot["Time_Picked"], format="%H:%M:%S", errors="coerce")
    df_robot["Uur"] = df_robot["Time_Picked"].dt.hour
    robot_orders = df_robot.groupby("Uur")["Order_ID"].count()

    df_mens["Time_Order"] = pd.to_datetime(df_mens["Time_Order"], format="%H:%M:%S", errors="coerce")
    df_mens["Uur"] = df_mens["Time_Order"].dt.hour
    mens_orders = df_mens.groupby("Uur")["Order_ID"].count()

    df = pd.DataFrame({"Robot": robot_orders, "Mens": mens_orders}).fillna(0)

    fig, ax = plt.subplots()
    df.plot(kind="bar", ax=ax)
    ax.set_ylabel("Aantal orders")
    ax.set_xlabel("Uur van de dag")

    # Tabel om data te vergelijken
    tabel = pd.DataFrame({
        "Robot": robot_orders,
        "Mens": mens_orders
    }).fillna(0)

    print("\nKPI 3: Aantal opgepikte orders per uur")
    print(tabel)


    return fig

# KPI 4: Bezorgsnelheid in seconden: 
def bereken_kpi4(df_robot, df_mens):
    if "Time_Order" not in df_robot.columns:
        df_robot["Time_Order"] = pd.to_datetime(df_robot["Time_Picked"], format="%H:%M:%S", errors="coerce")
    else:
        df_robot["Time_Order"] = pd.to_datetime(df_robot["Time_Order"], format="%H:%M:%S", errors="coerce")

    df_robot["Time_Delivery"] = pd.to_datetime(df_robot["Time_Delivery"], format="%H:%M:%S", errors="coerce")
    df_robot["Seconds"] = (df_robot["Time_Delivery"] - df_robot["Time_Order"]).dt.total_seconds()

    df_mens["Time_Order"] = pd.to_datetime(df_mens["Time_Order"], format="%H:%M:%S", errors="coerce")
    df_mens["Time_Delivery"] = pd.to_datetime(df_mens["Time_Delivery"], format="%H:%M:%S", errors="coerce")
    df_mens["Seconds"] = (df_mens["Time_Delivery"] - df_mens["Time_Order"]).dt.total_seconds()

    print("\nKPI 4: Bezorgsnelheid in seconden")
    print("Robot bezorgtijden (seconden):")
    print(df_robot["Seconds"].describe())  # gemiddelde, min, max, std

    print("Mens bezorgtijden (seconden):")
    print(df_mens["Seconds"].describe())  # gemiddelde, min, max, std


    return df_robot["Seconds"].mean(), df_mens["Seconds"].mean()

# KPI 5: Kosten per dag: 
def figuur_kpi5(df_robot, df_mens):
    df_robot["Date"] = pd.to_datetime(df_robot["Date"], dayfirst=True, errors="coerce")
    df_mens["Date"] = pd.to_datetime(df_mens["Date"], dayfirst=True, errors="coerce")

    robot_kosten = df_robot.groupby(df_robot["Date"].dt.date)["Total_Amount"].sum()
    mens_kosten = df_mens.groupby(df_mens["Date"].dt.date)["Total_Amount"].sum()

    df = pd.DataFrame({"Robot": robot_kosten, "Mens": mens_kosten}).fillna(0)

    fig, ax = plt.subplots()
    df.plot(kind="bar", ax=ax)
    ax.set_ylabel("Totale kosten (€)")
    ax.set_xlabel("Datum")

    print("\nKPI 5: Kosten per dag")

    print("Kosten per dag - Robot:")
    print(df_robot.groupby(df_robot["Date"].dt.date)["Total_Amount"].sum())

    print("\nKosten per dag - Mens:")
    print(df_mens.groupby(df_mens["Date"].dt.date)["Total_Amount"].sum())
    return fig
