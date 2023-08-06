__version__ = "0.1.5"

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui
from eagerx_gui.gui import Gui
import sys


def launch_gui(state):
    app = QtGui.QApplication(sys.argv)

    ## Create main window with grid layout
    win = QtWidgets.QMainWindow()
    win.setWindowTitle("pyqtgraph example: Flowchart")
    cw = QtWidgets.QWidget()
    win.setCentralWidget(cw)
    layout = QtWidgets.QGridLayout()
    cw.setLayout(layout)

    rx_gui = Gui(state)
    w = rx_gui.widget()

    # Add flowchart control panel to the main window
    layout.addWidget(w, 0, 0, 2, 1)

    win.show()

    app.exec()
    new_state = rx_gui.state()
    app.quit()
    return new_state
