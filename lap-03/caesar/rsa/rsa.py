import sys
import rsa
from PyQt5.QtWidgets import QApplication, QMainWindow
from rsa_ui import Ui_MainWindow

class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.public_key = None
        self.private_key = None
        self.ui.generate_button.clicked.connect(self.generate_keys)
        self.ui.encrypt_button.clicked.connect(self.encrypt)
        self.ui.decrypt_button.clicked.connect(self.decrypt)

    def generate_keys(self):
        (self.public_key, self.private_key) = rsa.newkeys(512)
        self.ui.public_key_text.setText(str(self.public_key))
        self.ui.private_key_text.setText(str(self.private_key))

    def encrypt(self):
        if self.public_key is None:
            self.ui.output_text.setText("Vui lòng tạo khóa trước!")
            return
        text = self.ui.input_text.text().encode('utf-8')
        try:
            encrypted = rsa.encrypt(text, self.public_key)
            self.ui.output_text.setText(encrypted.hex())
        except OverflowError:
            self.ui.output_text.setText("Văn bản quá dài cho khóa hiện tại!")

    def decrypt(self):
        if self.private_key is None:
            self.ui.output_text.setText("Vui lòng tạo khóa trước!")
            return
        try:
            encrypted = bytes.fromhex(self.ui.input_text.text())
            decrypted = rsa.decrypt(encrypted, self.private_key).decode('utf-8')
            self.ui.output_text.setText(decrypted)
        except ValueError:
            self.ui.output_text.setText("Dữ liệu không hợp lệ!")
        except rsa.pkcs1.OverflowError:
            self.ui.output_text.setText("Lỗi giải mã!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())