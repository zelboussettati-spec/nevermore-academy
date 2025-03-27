import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QDialog, QButtonGroup,
    QMessageBox, QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QIcon


# ------------------------------------------------
# bedankt popup
# ------------------------------------------------
class BedanktPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bevestiging")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        label_icon = QLabel("\u2714", alignment=Qt.AlignmentFlag.AlignCenter)
        label_icon.setStyleSheet("font-size: 60px; color: green;")

        label_text = QLabel("Bedankt!", alignment=Qt.AlignmentFlag.AlignCenter)
        label_text.setStyleSheet("font-size: 18px; color: black;")

        layout.addStretch()
        layout.addWidget(label_icon)
        layout.addWidget(label_text)
        layout.addStretch()


# ------------------------------------------------
# betaalmethode schjerm
# ------------------------------------------------
class BetaalMethode(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lakeside Mania")
        self.setFixedSize(500, 750)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = self._create_topbar()
        center_widget = self._create_center_area()
        footer_bar = self._create_footer()

        main_layout.addWidget(top_bar, 0)
        main_layout.addWidget(center_widget, 1)
        main_layout.addWidget(footer_bar, 0)

        self._set_stylesheet()

    def _create_topbar(self) -> QWidget:
        top_bar = QWidget()
        top_bar.setObjectName("TopBar")

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)

        back_button = QPushButton("← Terug")
        back_button.setObjectName("BackButton")
        back_button.clicked.connect(self.ga_terug)

        title_label = QLabel("Betaalmethode", alignment=Qt.AlignmentFlag.AlignCenter)

        help_button = QPushButton("?")
        help_button.setObjectName("HelpButton")

        layout.addWidget(back_button, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label, 1)
        layout.addWidget(help_button, 0, Qt.AlignmentFlag.AlignRight)

        return top_bar

    def _create_center_area(self) -> QWidget:
        dark_area = QWidget()
        dark_area.setObjectName("DarkArea")

        main_layout = QVBoxLayout(dark_area)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        instruction_label = QLabel("Kies uw betaalmethode:")
        instruction_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(instruction_label, 0, Qt.AlignmentFlag.AlignLeft)
        main_layout.addStretch()
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addStretch()

        self.btn_betaalpas = QPushButton("Betaalpas / Mobiele Telefoon")
        self.btn_betaalpas.setCheckable(True)
        self.btn_betaalpas.setIcon(QIcon("apple.png"))

        self.btn_contant = QPushButton("Contant")
        self.btn_contant.setCheckable(True)
        self.btn_contant.setIcon(QIcon("cash.png"))

        group = QButtonGroup(dark_area)
        group.setExclusive(True)
        group.addButton(self.btn_betaalpas)
        group.addButton(self.btn_contant)

        btn_layout.addWidget(self.btn_betaalpas)
        btn_layout.addWidget(self.btn_contant)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        return dark_area

    def _create_footer(self) -> QWidget:
        footer_bar = QWidget()
        footer_bar.setObjectName("FooterBar")

        layout = QHBoxLayout(footer_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        confirm_button = QPushButton("Bevestigen")
        confirm_button.setObjectName("ConfirmButton")
        confirm_button.clicked.connect(self._show_confirmation_dialog)

        layout.addStretch()
        layout.addWidget(confirm_button)
        layout.addStretch()

        return footer_bar

#bevestigscherm oproepen en checken of betaalmethode geselecteerd is
    def _show_confirmation_dialog(self):
        if not (self.btn_betaalpas.isChecked() or self.btn_contant.isChecked()):
            QMessageBox.warning(self, "Fout", "Selecteer alstublieft een betaalmethode.")
            return

        dialog = BedanktPopup(self)
        dialog.exec()

#terugknop
    def ga_terug(self):
        if self.parent():
            self.parent().show()
        self.close()

    def _set_stylesheet(self):
        stylesheet = """
        QMainWindow {
            background-color: #f8f8f8;
        }
        #TopBar {
            background-color: #ffffff;
            min-height: 70px;
        }
        #BackButton, #HelpButton {
            background: transparent;
            border: none;
            font-size: 16px;
            padding: 5px 10px;
            color: #333;
        }
        #BackButton:hover, #HelpButton:hover {
            background-color: #eeeeee;
        }
        /* Titel */
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        #DarkArea {
            background-color: #e3e3e3;
        }
        #FooterBar {
            background-color: #ffffff;
            border-top: 1px solid #dddddd;
            min-height: 70px;  /* Grotere hoogte van de footer */
        }
        /* Betaalknoppen */
        QPushButton {
            border: 1px solid #cccccc;
            border-radius: 4px;
            font-size: 14px;
            color: #333333;
            padding: 10px 20px;
            background-color: #fafafa;
        }
        QPushButton:hover {
            background-color: #dddddd;
        }
        QPushButton:checked {
            background-color: #cccccc;
            border: 1px solid #999999;
        }
        /* Bevestigen */
        #ConfirmButton {
            background-color: #007BFF;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            padding: 10px 40px;
        }
        #ConfirmButton:hover {
            background-color: #0056b3;
        }
        """
        self.setStyleSheet(stylesheet)


# ------------------------------------------------
# winkelwagen
# ------------------------------------------------
class WinkelwagenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lakeside Mania")
        self.setFixedSize(500, 750)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = self._create_topbar()
        center_widget = self._create_center_area()
        tafelnummer_bar = self._create_tmr_bar()
        footer_bar = self._create_footer()

        main_layout.addWidget(top_bar, 0)
        main_layout.addWidget(center_widget, 1)
        main_layout.addWidget(tafelnummer_bar, 0)
        main_layout.addWidget(footer_bar, 0)

        self._set_stylesheet()

    def _create_topbar(self) -> QWidget:
        top_bar = QWidget()
        top_bar.setObjectName("TopBar")

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)

        title_label = QLabel("Uw bestelling", alignment=Qt.AlignmentFlag.AlignCenter)

        help_button = QPushButton("?")
        help_button.setObjectName("HelpButton")

        layout.addStretch()
        layout.addWidget(title_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(help_button, 0, Qt.AlignmentFlag.AlignRight)

        return top_bar

    def _create_center_area(self) -> QWidget:
        center_area = QWidget()
        center_area.setObjectName("CenterArea")

        layout = QVBoxLayout(center_area)
        layout.setContentsMargins(20, 20, 20, 20)

        cart_label = QLabel("Hier komen de winkelwagen producten", alignment=Qt.AlignmentFlag.AlignCenter)
        cart_label.setStyleSheet("color: #666; margin: 40px 0; font-size: 14px;")

        layout.addStretch()
        layout.addWidget(cart_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        return center_area

    def _create_tmr_bar(self) -> QWidget:
        tafelnummer_bar = QWidget()
        tafelnummer_bar.setObjectName("TafelNummer")

        layout = QHBoxLayout(tafelnummer_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        label = QLabel("Tafelnummer:")
        label.setObjectName("TafelLabel")

        self.lineedit_tafelnummer = QLineEdit()
        self.lineedit_tafelnummer.setPlaceholderText("Voer tafelnummer in...")

        layout.addWidget(label)
        layout.addWidget(self.lineedit_tafelnummer)

        return tafelnummer_bar

    def _create_footer(self) -> QWidget:
        footer_bar = QWidget()
        footer_bar.setObjectName("FooterBar")

        layout = QHBoxLayout(footer_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # Afrekenen-knop
        confirm_button = QPushButton("Afrekenen")
        confirm_button.setObjectName("BetaalButton")
        confirm_button.clicked.connect(self.go_to_payment)

        layout.addStretch()
        layout.addWidget(confirm_button)
        layout.addStretch()

        return footer_bar

    def go_to_payment(self):
        tafelnummer = self.lineedit_tafelnummer.text().strip()

        if not tafelnummer:
            QMessageBox.warning(
                self,
                "Oops",
                "Vul alstublieft uw tafelnummer in."
            )
            return

        self.payment_window = BetaalMethode(parent=self)
        self.payment_window.show()
        self.hide()

    def _set_stylesheet(self):
        stylesheet = """
        QMainWindow {
            background-color: #f8f8f8;
        }
        #TopBar {
            background-color: #ffffff;
            min-height: 70px; 
        }
        #HelpButton {
            background: transparent;
            border: none;
            font-size: 16px;
            padding: 5px 10px;
            color: #333;
        }
        #HelpButton:hover {
            background-color: #eeeeee;
        }
                #TafelBar {
            background-color: #ffffff;
            border-top: 1px solid #dddddd;
            min-height: 50px;
        }
        #TafelLabel {
            font-size: 16px;
            font-weight: normal;
            margin-right: 10px;
        }
        /* Tite*/
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }

        #CenterArea {
            background-color: #f8f8f8;
        }

        #FooterBar {
            background-color: #ffffff;
            border-top: 1px solid #dddddd;
            min-height: 70px; 
        }
        #BetaalButton {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            padding: 10px 40px;
        }
        #BetaalButton:hover {
            background-color: #0056b3;
        }
        """
        self.setStyleSheet(stylesheet)



def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    # lightmode forceren
    light_palette = QPalette()
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(220, 220, 220))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    light_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(120, 120, 120))
    light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 120, 120))

    app.setPalette(light_palette)

    # start met winkelwagen
    winkelwagen = WinkelwagenWindow()
    winkelwagen.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
