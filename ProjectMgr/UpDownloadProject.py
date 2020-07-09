"""Upload the contents of your Downloads folder to Dropbox.

This is an example app for API v2.
"""

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata

import dropbox
import logging

# from dbdownload import DBDownload
from Setting import Settings

import boto3
from Setting import Settings
import shutil


def UploadProject(ProjectName=''):
    path = Settings.projectTeacherPath
    session = boto3.Session(
        aws_access_key_id = Settings.aws_access_key_id,
        aws_secret_access_key= Settings.aws_secret_access_key,
        region_name= Settings.region_name
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('openverse-lms')
 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            if((ProjectName) in full_path):
                pass
            else:
                continue
            with open(full_path, 'rb') as data:
                path = path.replace('/','')
                bucket.put_object(Key=full_path[len(path)+1:], Body=data)
 

def DownloadProject(ProjectName = ''):
    
    dist = ProjectName
    local = Settings.projectStudentPath
    bucket = Settings.bucketName

    session = boto3.Session(
        aws_access_key_id = Settings.aws_access_key_id,
        aws_secret_access_key= Settings.aws_secret_access_key,
        region_name= Settings.region_name
    )

    client  = session.client('s3')
    resource = session.resource('s3')

    paginator = client.get_paginator('list_objects')
    
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local, file.get('Key'))

            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            else:
                if not os.path.exists(dest_pathname):
                    pass
                else:
                    continue
            resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)
















############################################ this is for dropbox old version #########################################

# from cloudsync.dropboxsync import DropboxSync
# import shutil

# def DownloadProject(projectPath):
    
#     remotedir = "/" + Settings.dropboxFolder
#     dbx = dropbox.Dropbox(Settings.access_token)
#     for entry in dbx.files_list_folder(remotedir).entries:
#         path = remotedir + '/' + entry.name
#         localdir = os.path.join(projectPath,entry.name)
#         if os.path.exists(localdir):
#             shutil.rmtree(localdir)
#         try:
#             os.mkdir(localdir)
#             dbSync = DropboxSync(path,localdir,False,Settings.access_token)
#             dbSync.setLogger(logging)
#             dbSync.prepare()
#             dbSync.filterSourceFiles(None)
#             dbSync.synchronize()
#         except:
#             logging.exception("downLoadfailed for " + localdir)
    
# def UploadProject(projectPath=""):

#     """Main program.

#     Parse command line, then iterate over files and directories under
#     rootdir and upload all files.  Skips some temporary files and
#     directories, and avoids duplicate uploads by comparing size and
#     mtime with the server.
#     """
    
#     folder = Settings.dropboxFolder
#     rootdir = projectPath
    
#     if not os.path.exists(rootdir):
#         logging.warning(rootdir + ' does not exist on your filesystem')
#         return False
#     elif not os.path.isdir(rootdir):
        
#         logging.warning(rootdir + ' is not a folder on your filesystem')
#         return False

#     dbx = dropbox.Dropbox(Settings.access_token)

#     for dn, dirs, files in os.walk(rootdir):
#         subfolder = dn[len(rootdir):].strip(os.path.sep)
#         listing = list_folder(dbx, folder, subfolder)
        
#         # First do all the files.
#         for name in files:
#             fullname = os.path.join(dn, name)
#             if not isinstance(name, six.text_type):
#                 name = name.decode('utf-8')
#             nname = unicodedata.normalize('NFC', name)
#             if name.startswith('.'):
#                 pass
#             elif name.startswith('@') or name.endswith('~'):
#                 pass
#             elif name.endswith('.pyc') or name.endswith('.pyo'):
#                 pass
#             elif nname in listing:
#                 md = listing[nname]
#                 mtime = os.path.getmtime(fullname)
#                 mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
#                 size = os.path.getsize(fullname)
#                 if (isinstance(md, dropbox.files.FileMetadata) and
#                         mtime_dt == md.client_modified and size == md.size):
#                         pass
#                 else:
#                     res = download(dbx, folder, subfolder, name)
#                     with open(fullname) as f:
#                         data = f.read()
#                     if res == data:
#                         pass
#                     else:
#                         if True:
#                             upload(dbx, fullname, folder, subfolder, name,
#                                    overwrite=True)
#             elif True:
#                 upload(dbx, fullname, folder, subfolder, name)

#         # Then choose which subdirectories to traverse.
#         keep = []
#         for name in dirs:
#             if name.startswith('.'):
#                 pass
#             elif name.startswith('@') or name.endswith('~'):
#                 pass
#             elif name == '__pycache__':
#                 pass
#             elif True:
#                 pass
#                 keep.append(name)
#             else:
#                 pass
#         dirs[:] = keep

# def list_folder(dbx, folder, subfolder):

#     """List a folder.
#     Return a dict mapping unicode filenames to
#     FileMetadata|FolderMetadata entries.
#     """

#     path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
#     while '//' in path:
#         path = path.replace('//', '/')
#     path = path.rstrip('/')
#     try:
#         with stopwatch('list_folder'):
#             res = dbx.files_list_folder(path)
#     except dropbox.exceptions.ApiError as err:
#         return {}
#     else:
#         rv = {}
#         for entry in res.entries:
#             rv[entry.name] = entry
#         return rv

# def download(dbx, folder, subfolder, name):
#     """Download a file.

#     Return the bytes of the file, or None if it doesn't exist.
#     """
#     path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
#     while '//' in path:
#         path = path.replace('//', '/')
#     with stopwatch('download'):
#         try:
#             md, res = dbx.files_download(path)
#         except dropbox.exceptions.HttpError as err:
#             print('*** HTTP error', err)
#             return None
#     data = res.content
#     return data

# def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
#     """Upload a file.

#     Return the request response, or None in case of error.
#     """
#     path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
#     while '//' in path:
#         path = path.replace('//', '/')
#     mode = (dropbox.files.WriteMode.overwrite
#             if overwrite
#             else dropbox.files.WriteMode.add)
#     mtime = os.path.getmtime(fullname)
#     with open(fullname, 'rb') as f:
#         data = f.read()
#     with stopwatch('upload %d bytes' % len(data)):
#         try:
#             res = dbx.files_upload(
#                 data, path, mode,
#                 client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
#                 mute=True)
#         except dropbox.exceptions.ApiError as err:
#             print('*** API error', err)
#             return None
#     return res

# @contextlib.contextmanager
# def stopwatch(message):
#     """Context manager to print how long a block of code took."""
#     t0 = time.time()
#     try:
#         yield
#     finally:
#         t1 = time.time()
#         print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


