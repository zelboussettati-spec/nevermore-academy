from PyQt6.QtWidgets import ( 
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QSpinBox, QFrame, QListWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import os
from PyQt6.QtWidgets import QApplication
from mysql import start_database_dp9

class Winkelmand:

    def __init__(self):
        self.items = {}     # Dictionary waarin items worden opgeslagen
        self.tafelnummer = 1    #Tafelnummer krijgt standaard waarde

    def voegToe(self, product_id, naam, prijs):     # Voeg product toe of verhoogd de hoeveelheid als het al bestaat. 
        if product_id in self.items:        # Als product al in de dict staat, verhoog alleen de hoeveelheid met 1
            self.items[product_id][2] += 1
        else:
            self.items[product_id] = [naam, prijs, 1]   # Anders maakt nieuwe entry met hoeveelheid 1

    def verwijder(self, product_id):    # dit verwijder een product uit de winkelmand.
        if product_id in self.items:    
            del self.items[product_id]

    def wijzigHoeveelheid(self, product_id, hoeveelheid):   # hier kunnen we de hoeveelheid aanpassen van product
        if product_id in self.items:
            if hoeveelheid > 0: 
                self.items[product_id][2] = hoeveelheid
            else:
                self.verwijder(product_id)  #hoeveelheid <0  wordt verwijderd

    def berekenTotaal(self):        # hier wordt de totaal berekend. 
        return sum(prijs * hoeveelheid for _, prijs, hoeveelheid in self.items.values())

    def setTafelnummer(self, nummer):   #tafelnummer instellen in de GUI
        self.tafelnummer = nummer


class WinkelmandScherm(QWidget):    
    def __init__(self, winkelmand):
        super().__init__()
        self.winkelmand = winkelmand     # koppeling naar de winkelmand class 

        # Stel titel en grootte van het PyQt-venster in
        self.setWindowTitle("Uw bestelling")
        self.setGeometry(100, 100, 400, 500)

        # CSS-bestand laden om de GUI te stylen
        css_pad = os.path.join(os.path.dirname(__file__), "style.css")
        if os.path.exists(css_pad):
            with open(css_pad, "r") as f:
                self.setStyleSheet(f.read())

        layout = QVBoxLayout()  # Hoofdlayout van het venster van boven naar beneden

        title_bar = QHBoxLayout()   #Help knop

        #links een label met tekst "uw bestelling" en de opmaak van de tekst
        self.label_titel = QLabel("Uw bestelling")
        self.label_titel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        # rechts een help-knop (?) met de opmaak
        self.knop_help = QPushButton("?")       
        self.knop_help.setFixedSize(30, 30)
        self.knop_help.setStyleSheet("background: #00bfff; color: white; border-radius: 15px;")

        # Koppel de knop aan een functie (onHelpClicked)
        self.knop_help.clicked.connect(self.onHelpClicked)

        # Plaats titel links, helpknop rechts
        title_bar.addWidget(self.label_titel, alignment=Qt.AlignmentFlag.AlignLeft)
        title_bar.addStretch()
        title_bar.addWidget(self.knop_help, alignment=Qt.AlignmentFlag.AlignRight)

        # Voeg de titelbar-layout toe aan de hoofdlayout
        layout.addLayout(title_bar)

        # De drie puntjes midden in de scherm
        self.progress_bar = QLabel("●  ●  ○")  
        # Dit is een simpele tekstweergave (3 bolletjes waarvan 2 gevuld).
        self.progress_bar.setFont(QFont("Arial", 12))
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.progress_bar)

        # Hierin tonen we alle producten
        self.bestelling_lijst = QListWidget()
        layout.addWidget(self.bestelling_lijst)

        # tafelnummer layout (spinbox) en de opmaak 
        tafelnummer_layout = QHBoxLayout()
        self.label_tafelnummer = QLabel("Tafelnummer:")
        self.label_tafelnummer.setFont(QFont("Arial", 12))

        self.spinbox_tafelnummer = QSpinBox()
        self.spinbox_tafelnummer.setMinimum(1)
        self.spinbox_tafelnummer.setMaximum(99)
        # zet de huidige waarde in op wat er op de winkelmand staat
        self.spinbox_tafelnummer.setValue(self.winkelmand.tafelnummer)
        # koppel de verandering aan onTafelnummerChanged
        self.spinbox_tafelnummer.valueChanged.connect(self.onTafelnummerChanged)

        tafelnummer_layout.addWidget(self.label_tafelnummer)
        tafelnummer_layout.addWidget(self.spinbox_tafelnummer)
        layout.addLayout(tafelnummer_layout)

        # scheidingslijn 
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: #ccc; height: 2px;")
        layout.addWidget(line)

        # Totaal + afrekenknop
        prijs_layout = QHBoxLayout()

        #label voor het totaal bedrag
        self.label_totaal = QLabel("Totaal: €0.00")
        self.label_totaal.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        # knop "afrekenen" opmaak geven
        self.knop_afrekenen = QPushButton("Afrekenen")
        self.knop_afrekenen.setStyleSheet("background: #00bfff; color: white; font-size: 14px; padding: 10px;")
        self.knop_afrekenen.setFixedWidth(150)
        # Wanneer gebruiker klikt -> onAfrekenenClicked
        self.knop_afrekenen.clicked.connect(self.onAfrekenenClicked)

        #Zet het label links en knop rechts
        prijs_layout.addWidget(self.label_totaal)
        prijs_layout.addStretch()
        prijs_layout.addWidget(self.knop_afrekenen)
        layout.addLayout(prijs_layout)

        # Stel de hoofdlayout in op dit venster
        self.setLayout(layout)

        # vul de lijst met producten
        self.updateWinkelmand()

    def updateWinkelmand(self):
        # Leeg eerst de QListWidget voordat we hem opnieuw opbouwen.
        self.bestelling_lijst.clear()

        # Doorloop alle items in de winkelmand
        for product_id, (naam, prijs, hoeveelheid) in self.winkelmand.items.items():
            # maak een horizontale layout voor elk item
            item_widget = QWidget()
            item_layout = QHBoxLayout()

            # label met productnaam en prijs
            label_info = QLabel(f"{naam}  €{prijs:.2f}")
            label_info.setFont(QFont("Arial", 10))

            # Spinbox om de hoeveelheid te wijzigen
            spinbox = QSpinBox()
            spinbox.setMinimum(1)
            spinbox.setMaximum(99)
            spinbox.setValue(hoeveelheid)
            # bij verandering wordt aangegeven om welke product_id het is
            spinbox.valueChanged.connect(
                lambda value, pid=product_id: self.onHoeveelheidChanged(pid, value)
            )

            # Verwijderknop "X"
            btn_verwijder = QPushButton("X")
            btn_verwijder.setStyleSheet("background-color:red; color:white; border-radius:5px;")
            btn_verwijder.setFixedWidth(30)
            # koppel aan onVerwijderClicked
            btn_verwijder.clicked.connect(
                lambda _, pid=product_id: self.onVerwijderClicked(pid)
            )
            
            # Zet label links dan ruimte laten dan dan spinbox daarna de "X"
            item_layout.addWidget(label_info)
            item_layout.addStretch()
            item_layout.addWidget(spinbox)
            item_layout.addWidget(btn_verwijder)
            item_widget.setLayout(item_layout)

            #Hier maken we een listwidgetitem 
            list_item = QListWidgetItem(self.bestelling_lijst)
            # Zorg dat de hoogte van de item_widget voldoende ruimte krijgt
            list_item.setSizeHint(item_widget.sizeHint())

            self.bestelling_lijst.addItem(list_item)
            self.bestelling_lijst.setItemWidget(list_item, item_widget)

        # Bereken en toon het nieuwe totaalbedrag
        self.label_totaal.setText(f"Totaal: €{self.winkelmand.berekenTotaal():.2f}")

    # Event-handler methodes

    def onHoeveelheidChanged(self, product_id, nieuwe_hoeveelheid):
        self.winkelmand.wijzigHoeveelheid(product_id, nieuwe_hoeveelheid)
        self.updateWinkelmand()

    def onVerwijderClicked(self, product_id):
        self.winkelmand.verwijder(product_id)
        self.updateWinkelmand()

    def onHelpClicked(self):
        QMessageBox.information(
            self, "Help", "Een medewerker is onderweg om te helpen."
        )

    def onAfrekenenClicked(self):
        totaal = self.winkelmand.berekenTotaal()
        tafelnr = self.winkelmand.tafelnummer
        QMessageBox.information(
            self, "Afrekenen",
            f"U gaat nu afrekenen.\nTafelnummer: {tafelnr}\nTotaal: €{totaal:.2f}"
        )

    def onTafelnummerChanged(self, value):
        self.winkelmand.setTafelnummer(value)


# Opstartpunt: als dit bestand direct wordt gedraaid 
if __name__ == "__main__":

    app = QApplication([])

    # Maak een Winkelmand en voeg wat testdata toe
    winkelmand = Winkelmand()
    winkelmand.voegToe(1, "Cheeseburger", 6.99)
    winkelmand.voegToe(2, "Frietjes", 2.99)

    # Start het WinkelmandScherm en toon het venster
    window = WinkelmandScherm(winkelmand)
    window.show()

    # Voer de PyQt event-loop uit
    app.exec()
