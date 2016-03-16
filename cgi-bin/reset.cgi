#!/usr/bin/env python

import os
import cgi
import cgitb
import image_process
import gencookie
import MySQLdb

cgitb.enable()

form = cgi.FieldStorage()

image_dir = "/var/www/html/images"
edit_dir = "/var/www/html/tmp"

conn = MySQLdb.connect(
    host = 'db',
    user = 'csci4140',
    passwd = 'opensource',
    db = 'instagram'
)
cursor = conn.cursor()

if ('reset' in form):


    # Clean DataBase
    cursor.execute("DROP TABLE IF EXISTS images")
    cursor.execute("DROP TABLE IF EXISTS edit")

    tb_image = '''
    CREATE TABLE `images` (
      `pid` int(11) NOT NULL,
      `filename` varchar(255) NOT NULL,
      `imagetype` varchar(5) NOT NULL
    )
    '''
    tb_edit = '''
    CREATE TABLE `edit` (
      `name` varchar(255) NOT NULL,
      `step` int(11) NOT NULL,
      `edit_name` varchar(255) NOT NULL,
      `ext` varchar(5) NOT NULL
    )
    '''
    cursor.execute(tb_image)
    conn.commit()
    cursor.execute(tb_edit)
    conn.commit()

    # Clean session
    cookieDict = gencookie.remove_cookie()

    # Clean all images
    image_process.discard(os.path.join(image_dir,"*"))
    image_process.discard(os.path.join(edit_dir,"*"))

    # Display job is done
    print "Content-Type: text/html"
    print cookieDict
    print
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Init</title>
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            <br>
            Job is done
            <form method="post" action="index.cgi">
                <span class="btn btn-default btn-file"> Back to Home <input type="submit"></span>
            </form>
        </div>
        </body>
        </html>
    '''


else:
    print "Location: /cgi-bin/index.cgi"
    print

cursor.close()
conn.close()