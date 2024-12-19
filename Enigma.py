import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit
)

class EnigmaMachine:
    def __init__(self, key="AAAAAA"):
        # Строки замены у роторов
        self.rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        self.rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        self.rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        self.rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
        self.rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
        self.rotor6 = "JPGVOUMFYQBENHZRDKASXLICTW"
        # Замена букв на диске рефлектора
        self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        # Алфавит
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Буквы, при которых поворачивается следующий ротор
        self.notch1 = "Q"
        self.notch2 = "E" 
        self.notch3 = "V"
        self.notch4 = "J"
        self.notch5 = "Z"
        self.notch6 = "M"  # Выемка нового ротора

        # Установка начальных позиций роторов по ключу
        self.set_key(key)

    def set_key(self, key):
        if len(key) != 6 or not key.isalpha():
            raise ValueError("Ключ должен состоять из 6 букв (например, AAAAAA).")

        # Устанавливаем начальные позиции роторов на основе положения буквы в алфавите
        self.position1 = self.alphabet.index(key[0].upper())
        self.position2 = self.alphabet.index(key[1].upper())
        self.position3 = self.alphabet.index(key[2].upper())
        self.position4 = self.alphabet.index(key[3].upper())
        self.position5 = self.alphabet.index(key[4].upper())
        self.position6 = self.alphabet.index(key[5].upper())

    def rotate_rotors(self):
        # Поворачиваем ротор 1 на каждую букву
        self.position1 = (self.position1 + 1) % 26

        # Если буква на лицевой стороне ротора 1 совпадает с выемкой, поворачиваем ротор 2 и так далее
        if self.rotor1[self.position1] == self.notch1:
            self.position2 = (self.position2 + 1) % 26

            if self.rotor2[self.position2] == self.notch2:
                self.position3 = (self.position3 + 1) % 26

                if self.rotor3[self.position3] == self.notch3:
                    self.position4 = (self.position4 + 1) % 26

                    if self.rotor4[self.position4] == self.notch4:
                        self.position5 = (self.position5 + 1) % 26

                        if self.rotor5[self.position5] == self.notch5:
                            self.position6 = (self.position6 + 1) % 26

    def encrypt_char(self, char):
        if char.upper() not in self.alphabet:
            return char 

        # Роторы поворачиваются перед шифровкой буквы
        self.rotate_rotors()

        # Здесь будем сохранять сдвиги
        offset1 = self.position1
        offset2 = self.position2
        offset3 = self.position3
        offset4 = self.position4
        offset5 = self.position5
        offset6 = self.position6  # Сдвиг для нового ротора

        # Пропускаем через 6 роторов
        index = self.alphabet.index(char.upper())
        index = (index + offset1) % 26
        char = self.rotor1[index]
        print(char)

        index = self.alphabet.index(char)
        index = (index + offset1 - offset2) % 26
        char = self.rotor2[index]
        print(char)

        index = self.alphabet.index(char)
        index = (index + offset2 - offset3) % 26
        char = self.rotor3[index]
        print(char)

        index = self.alphabet.index(char)
        index = (index + offset3 - offset4) % 26
        char = self.rotor4[index]
        print(char)

        index = self.alphabet.index(char)
        index = (index + offset4 - offset5) % 26
        char = self.rotor5[index]
        print(char)

        index = self.alphabet.index(char)
        index = (index + offset5 - offset6) % 26
        char = self.rotor6[index]
        print(char)

        # Прохожу через рефлектор
        index = self.alphabet.index(char)
        char = self.reflector[index]

        # Возвращаюсь через роторы в обратном порядке
        index = self.rotor6.index(char)
        index = (index - offset6) % 26
        char = self.alphabet[index]

        index = self.rotor5.index(char)
        index = (index + offset6 - offset5) % 26
        char = self.alphabet[index]

        index = self.rotor4.index(char)
        index = (index + offset5 - offset4) % 26
        char = self.alphabet[index]

        index = self.rotor3.index(char)
        index = (index + offset4 - offset3) % 26
        char = self.alphabet[index]

        index = self.rotor2.index(char)
        index = (index + offset3 - offset2) % 26
        char = self.alphabet[index]

        index = self.rotor1.index(char)
        index = (index + offset2 - offset1) % 26
        char = self.alphabet[index]

        return char

    def encrypt(self, text):
        return ''.join(self.encrypt_char(c) for c in text)

    def decrypt(self, text):
        return self.encrypt(text)

# Фронт энд
class EnigmaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.enigma = EnigmaMachine()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Шифровальная машина Энигма с notch и ключом")

        main_layout = QVBoxLayout()

        key_layout = QHBoxLayout()
        key_label = QLabel("Ключ (6 букв):")
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("AAAAAA")
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)
        main_layout.addLayout(key_layout)

        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Введите текст для шифрования/расшифрования")
        main_layout.addWidget(self.input_text)

        button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("Зашифровать", self)
        self.encrypt_button.clicked.connect(self.encrypt_text)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Расшифровать", self)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        button_layout.addWidget(self.decrypt_button)

        main_layout.addLayout(button_layout)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Результат")
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

    def encrypt_text(self):
        key = self.key_input.text()
        try:
            self.enigma.set_key(key)
            text = self.input_text.toPlainText()
            encrypted_text = self.enigma.encrypt(text)
            self.output_text.setText(encrypted_text)
        except ValueError as e:
            self.output_text.setText(f"Ошибка: {e}")

    def decrypt_text(self):
        key = self.key_input.text()
        try:
            self.enigma.set_key(key)
            text = self.input_text.toPlainText()
            decrypted_text = self.enigma.decrypt(text)
            self.output_text.setText(decrypted_text)
        except ValueError as e:
            self.output_text.setText(f"Ошибка: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaApp()
    window.show()
    sys.exit(app.exec_())