# -*- coding: utf-8 -*-
import sys
import queue
import driver
from gui import main
from PyQt5 import QtCore, QtGui, QtWidgets

class App(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.connect_components()
        
        # execute commands from response queue
        self.tmr_cmd = QtCore.QTimer()
        self.tmr_cmd.timeout.connect(self.cmd_timer)
        self.tmr_cmd.start(30)

    def connect_components(self):
        self.actionInput.triggered.connect(self.input)
        self.pte_output.appendPlainText("If you change the gui execute: pyuic5 -x main.ui -o main.py")
    
    def input(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text","Your input:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            self.output(text)

    def cmd_timer(self, evt=None):
        ''' read out command queue and execute commands in gui-thread.'''
        try:
            # process max 5 commands at a time
            for i in range(5):
                # gets command from response queue
                command, args = driver.Response()
                # execute command in gui thread
                command(*args)
        except queue.Empty:
            pass

    def output(self, text, style="color:black"):
        html = """<span style="{}" >{}</span>""".format(style,text)
        driver.putInQueue(self.pte_output.appendHtml, '<pre >%s</pre>' % html)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())