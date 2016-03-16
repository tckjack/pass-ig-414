#!/usr/bin/env python

import MySQLdb
import os
import cgi
import cgitb
import gencookie
import image_process


cgitb.enable()

form = cgi.FieldStorage()

conn = MySQLdb.connect(
    host = 'db',
    user = 'csci4140',
    passwd = 'opensource',
    db = 'instagram'
)

cursor = conn.cursor()

saveDir = '/var/www/html/tmp' # Full path or relative path
readDir = '/tmp'

cookieDict = gencookie.find_cookie()


if ('pic' not in form):
    print "Content-Type: text/html"
    print
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Uploaded</title>
            <link rel="stylesheet" href="../css/bootstrap.min.css">
            <link rel="stylesheet" href="../css/pagination.css">
        </head>
        <body>
        <div class="container">
            <div class="col-sm-12">
                <div id="upload">
                    <br>
                    No file uploaded. <br>
                    <form action="index.cgi" method="post">
                        <span class="btn btn-default btn-file">Cancel<input type="submit" name="cancel" value="cancel"></span>
                    </form>
                </div>
            </div>
        </div>
    '''

elif (not form['pic'].filename):
    print "Content-Type: text/html"
    print
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Uploaded</title>
            <link rel="stylesheet" href="../css/bootstrap.min.css">
            <link rel="stylesheet" href="../css/pagination.css">
        </head>
        <body>
        <div class="container">
            <div class="col-sm-12">
                <div id="upload">
                    <br>
                    No file selected. <br>
                    <form action="index.cgi" method="post">
                        <span class="btn btn-default btn-file">Cancel<input type="submit" name="cancel" value="cancel"></span>
                    </form>
                </div>
            </div>
        </div>
    '''

else:
    fileitem = form['pic']
    cookieDict = gencookie.create_cookies()
    (fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
    fn = cookieDict['session'].value
    savePath = os.path.join(saveDir, fn + ext)
    open(savePath, 'wb').write(fileitem.file.read())
    result = image_process.identify(savePath)
    if (result != "Error"):
        print "Content-Type: text/html"
        print cookieDict
        print
        print '''
            <html>
            <head>
                <title>CSCI 4140 Assignment 1 -- Instagram -- Uploaded</title>
                <link rel="stylesheet" href="../css/bootstrap.min.css">
                <link rel="stylesheet" href="../css/pagination.css">
            </head>
            <body>
            <br>
            <div class="container">
                <br>
                <div class="row">
        '''
        print '<br><img id="im" src="%s"/>' %(os.path.join(readDir, fn + ext))
        print '''
                </div>
                <div class="row">
                    <br>
                    <div class="upload">
                        <form method="post" action="edit.cgi">
                            <span class="btn btn-default btn-file"> Edit <input type="submit" name="edit" value="%s"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Cancel <input type="submit" name="cancel" value="cancel"></span>
                        </form>
                    </div>
                </div>
            </div>
        ''' %(ext)
    else:
        cookieDict = gencookie.remove_cookie()
        print "Content-Type: text/html"
        print cookieDict
        print
        print '''
            <html>
            <head>
                <title>CSCI 4140 Assignment 1 -- Instagram -- Uploaded</title>
                <link rel="stylesheet" href="../css/bootstrap.min.css">
                <link rel="stylesheet" href="../css/pagination.css">
            </head>
            <body>
            <br>
            <div class="container">
                <br>
                <div class="row">
                    This is not a image!
                </div>
                <div class="row">
                    <br>
                    <div class="upload">
                        <form method="post" action="index.cgi">
                            <span class="btn btn-default btn-file"> Cancel <input type="submit"></span>
                        </form>
                    </div>
                </div>
            </div>
        '''


print '</body></html>'
cursor.close()
conn.close()