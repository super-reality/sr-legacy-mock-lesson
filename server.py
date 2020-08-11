import sys
from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from Container import QAnchorDialog
from PyQt5.QtWidgets import QApplication
from main import MainWindow
import logging
from datetime import datetime
import threading

manager = JSONRPCResponseManager()
mw = None

def showAnchorDlg():
  # mw.anchorDlg.show()
  return {"State":True}
  
def hideAnchorDlg():
  # mw.anchorDlg.hide()
  return {"State":True}
  
def dict_to_list(dictionary):
    return list(dictionary.items())


@dispatcher.add_method
def simple_add(first=0, **kwargs):
    return first + kwargs["second"]


def echo_with_long_name(msg):
    return msg


def time_ping():
    return datetime.now().isoformat()


dispatcher.add_method(time_ping)
dispatcher.add_method(echo_with_long_name, name='echo')

dispatcher['subtract'] = lambda a, b: a - b
dispatcher['dict_to_list'] = dict_to_list

dispatcher.add_method(showAnchorDlg)
dispatcher.add_method(hideAnchorDlg)

@Request.application
def application(request):
    response = manager.handle(request.get_data(cache=False, as_text=True), dispatcher)
    return Response(response.json, mimetype='application/json')

def launchMainWin():
  mw = MainWindow()
  mw.show(

if __name__ == "__main__":

  logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
  app = QApplication(sys.argv)
  UI = threading.Thread(target=launchMainWin,daemon=True)
  UI.start()
  # run_simple('localhost', 4000, application)
  sys.exit(app.exec_())
  
  

