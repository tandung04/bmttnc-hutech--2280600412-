import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ecc_ui import Ui_MainWindow
from ecdsa import SigningKey, NIST256p
import hashlib

class ECCApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.private_key = None
        self.public_key = None
        self.ui.generate_button.clicked.connect(self.generate_keys)
        self.ui.encrypt_button.clicked.connect(self.encrypt)
        self.ui.decrypt_button.clicked.connect(self.decrypt)

    def generate_keys(self):
        self.private_key = SigningKey.generate(curve=NIST256p)
        self.public_key = self.private_key.get_verifying_key()
        self.ui.public_key_text.setText(self.public_key.to_string().hex())
        self.ui.private_key_text.setText(self.private_key.to_string().hex())

    def encrypt(self):
        if self.public_key is None:
            self.ui.output_text.setText("Vui lòng tạo khóa trước!")
            return
        text = self.ui.input_text.text().encode('utf-8')
        signature = self.private_key.sign(text)
        self.ui.output_text.setText(signature.hex())

    def decrypt(self):
        if self.public_key is None:
            self.ui.output_text.setText("Vui lòng tạo khóa trước!")
            return
        try:
            signature = bytes.fromhex(self.ui.input_text.text())
            text = self.ui.input_text.text().encode('utf-8')
            is_valid = self.public_key.verify(signature, text)
            self.ui.output_text.setText("Chữ ký hợp lệ!" if is_valid else "Chữ ký không hợp lệ!")
        except:
            self.ui.output_text.setText("Lỗi xác minh chữ ký!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())