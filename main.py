import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QFileDialog, QMainWindow, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


# Plot Creation

class PlotWindow(QMainWindow):
    def __init__(self, title, parent=None, position=None):
        super(PlotWindow, self).__init__(parent, Qt.Window)
        self.setWindowTitle(title)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        if position is not None:
            self.move(position)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.file_name = None
        self.data_from_csv = None
        self.setWindowTitle("CSV Plotter")

        self.setFixedSize(300, 300)

        self.loadButton = QPushButton('Load CSV File')
        self.loadButton.setFixedSize(200, 50)

        self.plotButton = QPushButton('Generate Plots')
        self.plotButton.setFixedSize(200, 50)
        self.plotButton.setEnabled(False)

        self.loadButton.clicked.connect(self.load_csv_file)
        self.plotButton.clicked.connect(self.plot)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addStretch(1)
        layout.addWidget(self.loadButton, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.plotButton, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        self.setCentralWidget(widget)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def load_csv_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Load CSV File", "",
                                                        "CSV Files (*.csv);;All Files (*)", options=options)
        if self.file_name:
            self.data_from_csv = pd.read_csv(self.file_name)
            self.plotButton.setEnabled(True)

    def plot(self):
        # Plot 1
        window1 = PlotWindow('Plot 1', self)
        window1.move(0, 0)
        ax = window1.figure.add_subplot(111)
        column_to_sample = 'IMAGE_Count_Cells'
        retrieved_data = self.data_from_csv.loc[:, column_to_sample].values
        ax.bar(np.arange(len(retrieved_data)), retrieved_data)
        ax.set_xlabel('Well')
        ax.set_ylabel(column_to_sample)
        window1.show()

        # Plot 2
        window2 = PlotWindow('Plot 2', self)
        window2.move(500, 0)
        ax = window2.figure.add_subplot(111)
        row_number_for_sample = 'AZ11547175-001'
        sample_ID = self.data_from_csv.loc[:, 'SAMPLEIDDISPLAY'].values
        find_rows = np.where(sample_ID == row_number_for_sample)[0]
        dose = self.data_from_csv.loc[find_rows, 'CONCENTRATION'].values
        column_to_sample = 'NUCLEI_Intensity_IntegratedIntensity_DNA'
        nuc_Int = self.data_from_csv.loc[find_rows, column_to_sample].values
        ax.plot(np.log(dose), nuc_Int, 'o')
        window2.show()


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())
