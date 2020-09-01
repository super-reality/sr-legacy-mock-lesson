import sys
from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import logging
from datetime import datetime
from MyUtil import *

manager = JSONRPCResponseManager()
mw = None


def showAnchorDlg():
    return {"State": True}


def hideAnchorDlg():
    return {"State": True}


def snipImage(posx, posy, width, height, path):
    path = saveWindowRect(posx, posy, width, height, path)
    path = path.replace('\\', '/')
    return {"imgPath": path}

def findCV(imageUrl,parentx,parenty,parentwidth,parentheight):
    result = findCVMatch(imageUrl,parentx,parenty,parentwidth,parentheight)
    return list(result)

dispatcher.add_method(snipImage)
dispatcher.add_method(findCV)


@Request.application
def application(request):
    response = manager.handle(request.get_data(
        cache=False, as_text=True), dispatcher)
    result = Response(response.json, headers={
                      "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Content-Type"}, mimetype='application/json')
    result.access_control_allow_origin = '*'
    return result


if __name__ == "__main__":
    print(findCV("https://openverse-lms.s3-us-west-1.amazonaws.com/3.PNG",0,0,10,10))
    # try:
    #     run_simple('localhost', 4000, application)
    # except:
    #     logging.error("error")
    #     pass
