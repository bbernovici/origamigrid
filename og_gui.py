import sys

from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QCheckBox, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np

class OrigamiGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        open_button = QPushButton("Open Picture / Generate", self)
        open_button.resize(220,  25)
        open_button.move(50, 50)
        icon = QIcon('open.png')
        open_button.setIcon(icon)
        open_button.clicked.connect(self.showDialog)


        # generate_button = QPushButton('Generate Grid', self)
        # generate_button.resize(generate_button.sizeHint())
        # generate_button.move(150, 50)

        self.width_textbox = QLineEdit(self)
        self.width_textbox.resize(40, 25)
        self.width_textbox.move(300, 50)
        self.width_textbox.setText("6")

        width_label = QLabel("width (mm)", self)
        width_label.move(345, 55)

        self.height_textbox = QLineEdit(self)
        self.height_textbox.resize(40, 25)
        self.height_textbox.move(450, 50)
        self.height_textbox.setText("5")

        height_label = QLabel("height (mm)", self)
        height_label.move(495, 55)

        show_grid_cb = QCheckBox('Show Grid', self)
        show_grid_cb.move(600, 52)
        # height_label = QLabel("Height (in millimeters", self)

        self.setGeometry(150, 150, 800, 150)
        self.setWindowTitle('Origami Grid Generator')
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = Image.open(fname[0])

            with f:
                import origamigrid as og
                w, h = f.size
                data = np.array(f)
                data = og.generate_grid(data, h, w, int(self.height_textbox.text()), int(self.width_textbox.text()))
                img = Image.fromarray(data)
                img.save("output.png")
                Image.open("output.png")
                # print(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    og = OrigamiGrid()
    sys.exit(app.exec_())