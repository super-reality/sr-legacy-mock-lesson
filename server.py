import sys
from jsonrpc import JSONRPCResponseManager, dispatcher
from Container import QAnchorDialog
from PyQt5.QtWidgets import QApplication
from main import MainWindow
import logging

manager = JSONRPCResponseManager()

def showAnchorDlg():
  pass
def hideAnchorDlg():
  pass
if __name__ == "__main__":

  logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
  app = QApplication(sys.argv)
  mw = MainWindow()
  sys.exit(app.exec_())

