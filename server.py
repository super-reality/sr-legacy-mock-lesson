import sys
from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import logging
from datetime import datetime
from MyUtil import *
import boto3

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

#################  AWS  ######################
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAR5KZMOTEB45JUE45'
SECRET_KEY = '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'


def upload_to_aws(local_file, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    bucket = 'openverse-lms'
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


dispatcher.add_method(snipImage)
dispatcher.add_method(upload_to_aws)


@Request.application
def application(request):
    response = manager.handle(request.get_data(
        cache=False, as_text=True), dispatcher)
    result = Response(response.json, headers={
                      "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Content-Type"}, mimetype='application/json')
    result.access_control_allow_origin = '*'
    return result


if __name__ == "__main__":
    # logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    try:
        run_simple('localhost', 4000, application)
    except:
        logging.error("error")
        pass
    # print(snipImage(2110,110,500,200,"")
