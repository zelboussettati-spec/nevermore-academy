from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QSpinBox, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class ProductDetailScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productinformatie")
        self.setGeometry(100, 100, 400, 600)

        # CSS-styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                padding: 5px;
                font-size: 14px;
                border-radius: 5px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 16px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel#image_label {
                border: 2px solid #ddd;
                border-radius: 10px;
                background-color: white;
            }
            QLabel#price_label, QLabel#kcal_label {
                font-weight: bold;
                font-size: 18px;
                color: #000;                                 
            }
        """)
        #kleur hierboven wit #000;

        # dit zijn mijn Productopties
        self.products = {
            "Cheeseburger": {"prijs": "5,99", "kcal": "450", "beschrijving": "Sappige burger met gesmolten kaas op een geroosterd broodje.", "afbeelding": "cheeseburger.png"},
            "Vegan Burger": {"prijs": "6,99", "kcal": "400", "beschrijving": "Heerlijke plantaardige burger met verse groenten.", "afbeelding": "veganburger.png"},
            "Kipburger": {"prijs": "6,49", "kcal": "470", "beschrijving": "Knapperige kipburger met romige saus.", "afbeelding": "kipburger.png"}
        }

        # dit zijn mijn UI-elementen
        self.product_selector = QComboBox()
        self.product_selector.addItems(self.products.keys())
        self.product_selector.currentTextChanged.connect(self.update_product_details)

        self.image_label = QLabel()
        self.image_label.setObjectName("image_label")
        self.image_label.setFixedSize(200, 200)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.product_name_label = QLabel("Product: ")
        self.price_label = QLabel("Prijs: ")
        self.price_label.setObjectName("price_label")
        self.kcal_label = QLabel("Calorieën: ")
        self.kcal_label.setObjectName("kcal_label")

        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)

        self.quantity_label = QLabel("Aantal:")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(10)

        self.note_label = QLabel("Notitie voor de keuken:")
        self.note_input = QLineEdit()

        self.add_to_cart_button = QPushButton("Toevoegen aan winkelmand")
        self.add_to_cart_button.clicked.connect(self.add_to_cart)

        self.back_button = QPushButton("Terug")
        self.back_button.clicked.connect(self.close)

        # dit is de Layout zo kan je dus selecteren
        layout = QVBoxLayout()
        layout.addWidget(self.product_selector)
        layout.addWidget(self.image_label)
        layout.addWidget(self.product_name_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.kcal_label)
        layout.addWidget(self.description_text)

        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.note_label)
        layout.addWidget(self.note_input)

        layout.addWidget(self.add_to_cart_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.update_product_details()

    def update_product_details(self):
        product = self.product_selector.currentText()
        details = self.products[product]

        self.product_name_label.setText(f"Product: {product}")
        self.price_label.setText(f"Prijs: €{details['prijs']}")
        self.kcal_label.setText(f"Calorieën: {details['kcal']} kcal")
        self.description_text.setText(details["beschrijving"])

        afbeelding_pad = os.path.join(os.path.dirname(__file__), details["afbeelding"])
        pixmap = QPixmap(afbeelding_pad)
        self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def add_to_cart(self):
        product = self.product_selector.currentText()
        quantity = self.quantity_input.value()
        note = self.note_input.text()
        print(f"{quantity}x {product} toegevoegd aan winkelmand met notitie: '{note}'")

if __name__ == "__main__":
    app = QApplication([])
    window = ProductDetailScreen()
    window.show()
    app.exec()