import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from caesar_ui import Ui_MainWindow

def caesar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) + key - ascii_offset) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

class CaesarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.encrypt_button.clicked.connect(self.encrypt)
        self.ui.decrypt_button.clicked.connect(self.decrypt)

    def encrypt(self):
        text = self.ui.input_text.text()
        try:
            key = int(self.ui.key_input.text())
            result = caesar_encrypt(text, key)
            self.ui.output_text.setText(result)
        except ValueError:
            self.ui.output_text.setText("Khóa phải là số nguyên!")

    def decrypt(self):
        text = self.ui.input_text.text()
        try:
            key = int(self.ui.key_input.text())
            result = caesar_decrypt(text, key)
            self.ui.output_text.setText(result)
        except ValueError:
            self.ui.output_text.setText("Khóa phải là số nguyên!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarApp()
    window.show()
    sys.exit(app.exec_())