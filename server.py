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

def TTS(text=""):
    try:
        playAudioFromText(text)
    except:
        pass

def findCVArray(imageUrls,functions,parentx,parenty,parentwidth,parentheight):
    imagesOr = []
    imagesAnd = []
    imagesIgnore = []
    if(len(imageUrls)<1 or imageUrls[0] == None):
        return [0,0,0,0,0,0]
    for idx, function in enumerate(functions):
        if(idx == 0):
            imagesOr.append(imageUrls[idx])
            continue
        if function == 1:
            imagesAnd.append(imageUrls[idx])
        elif function == 2:
            imagesOr.append(imageUrls[idx])
        else:
            imagesIgnore.append(imageUrls[idx])
    
    maxMatchScore = 0
    maxMatch = None

    for imageOr in imagesOr:
        result = findCV(imageOr,parentx,parenty,parentwidth,parentheight)
        if(maxMatchScore < result[5]):
            maxMatchScore = result[5]
            maxMatch = result

    return maxMatch

dispatcher.add_method(snipImage)
dispatcher.add_method(findCV)
dispatcher.add_method(findCVArray)
dispatcher.add_method(TTS)


@Request.application
def application(request):
    response = manager.handle(request.get_data(
        cache=False, as_text=True), dispatcher)
    result = Response(response.json, headers={
                      "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Content-Type"}, mimetype='application/json')
    result.access_control_allow_origin = '*'
    return result


if __name__ == "__main__":
    try:
        run_simple('localhost', 4000, application)
    except:
        logging.error("error")
        pass
