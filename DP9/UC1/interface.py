from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QHBoxLayout, \
    QListWidget
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QTime


# Qwidget basisvenster die meerdere weergavegebeiden toestaat.
# Gridlayout: Voegt knoppen toe aan het rooster
# Qlabel: En label die tekst kan weergeven
# QHBoxlayout: horizentale lay out dat betekent dat ik de elementen onder elkaar kan zetten
# Qpushbutton Een knop die de naam en het icoon van de catogorie toont
# Qlistwidget een lijst waar je items zoals gerechtjes in kunt toevoegen
# click.connect: Dat verbind de klikactie met de knop
class MenuScreen(QWidget):  # basisvenster is een venster die meerdere weergavegebieden toestaat.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hoodscherm")  # setwindowtitle grote van de vensternaam
        self.setGeometry(100, 100, 420, 650)  # bepaalde grote van het venster
        self.layout = QVBoxLayout()  # horizontale lay-out
        self.init_ui()
        self.setLayout(self.layout)

    def init_ui(self):
        self.layout.addWidget(self.create_title("menukaart"))  # addwidget voegt een nieuw element toe aan de lay-out
        self.create_menu_buttons()
        self.create_footer()

    def create_title(self, text):
        title = QLabel(text)
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("padding: 10px; text-align: center;")
        return title

    def create_menu_buttons(self):  # icoon gebruikt van de laptop en in de code toegevoegd.
        categories = [
            ("Hamburgers", "🍔"),
            ("Tacos", "🌮"),
            ("Salades", "🥗"),
            ("Friet en Sauzen", "🍟"),
            ("Dranken en Desserts", "🥤")
        ]

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        for i, (name, icon) in enumerate(categories):
            button = QPushButton(f"{icon}\n{name}")
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(
                "padding: 15px; border-radius: 10px; background-color: #f8f8f8; text-align: center;")  # kleur lichtblauw
            button.clicked.connect(lambda checked, n=name: self.open_category_screen(n))
            grid_layout.addWidget(button, i // 2, i % 2)

        ontbijt_button = QPushButton("🥪\nOntbijt")
        ontbijt_button.setFont(QFont("Arial", 14))
        ontbijt_button.setStyleSheet(
            "padding: 12px; border-radius: 10px; background-color: #d3d3d3; text-align: center;")  # kleur lichtgrijs
        if QTime.currentTime().hour() >= 11:
            ontbijt_button.setEnabled(False)
            ontbijt_button.setText("🥪\nOntbijt\n(Niet mogelijk na 11:00)")
        else:
            ontbijt_button.clicked.connect(lambda: self.open_category_screen("Ontbijt"))
        grid_layout.addWidget(ontbijt_button, 3, 0, 1, 2)

        self.layout.addLayout(grid_layout)

    def create_footer(self):
        footer_layout = QHBoxLayout()
        home_button = QPushButton("🏠 Hoofdscherm")  # klikbaar om terug te gaan na het beginscherm
        home_button.setFont(QFont("Arial", 14))
        home_button.setStyleSheet("padding: 10px; background-color: #007bff; color: white; border-radius: 8px;")
        home_button.clicked.connect(self.close)
        footer_layout.addWidget(home_button)
        self.layout.addLayout(footer_layout)

    def open_category_screen(self, category):
        self.category_screen = CategoryScreen(category)
        self.category_screen.show()


class CategoryScreen(QWidget):
    def __init__(self, category_name):
        super().__init__()
        self.setWindowTitle(category_name)
        self.setGeometry(100, 100, 420, 650)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"{category_name} Menu"))
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.cart = []
        back_button = QPushButton("⬅️ Terug naar Menu")
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MenuScreen()
    window.show()
    app.exec()