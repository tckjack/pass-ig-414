#!/usr/bin/env python

import os
import cgi
import cgitb
import gencookie
import subprocess
import image_process
import MySQLdb

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
result = []
saveFinishDir = '/var/www/html/images'
readFinishDir = '/images'

fn = gencookie.find_cookie()

if (fn == None):
    print "Content-Type: text/html"
    print
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Not Found</title>
            <meta http-equiv="refresh" content="1;url=/cgi-bin/index.cgi" />
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            NO COOKIES FOUND
        </div>
        </body>
        </html>
    '''

elif ('cancel' in form):

    filename = fn + "*"
    removepath = os.path.join(saveDir,filename)
    query = "DELETE FROM edit WHERE name LIKE \"fn%\" "

    cursor.execute(query)
    conn.commit()
    image_process.discard(removepath)
    cookieDict = gencookie.remove_cookie()
    # if (result != "Error"):
    print "Content-Type: text/html"
    print cookieDict
    print
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Cancel</title>
            <meta http-equiv="refresh" content="1;url=/cgi-bin/index.cgi" />
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            Upload Cancel
        </div>
        </body>
        </html>
    '''

elif ('finish' in form):
    query = "SELECT edit_name, ext , step FROM edit WHERE name = \"%s\" GROUP BY step DESC LIMIT 1" %(fn)
    cursor.execute(query)
    result = cursor.fetchall()
    latestFilename = result[0][0]
    ext = result[0][1]
    readPath = os.path.join(saveDir,latestFilename+ext)
    savePath = os.path.join(saveFinishDir,fn+ext)
    cmd = ['cp',readPath,savePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    cookieDict = gencookie.remove_cookie()
    query2 = "INSERT INTO images(filename,imagetype) VALUES (\"%s\",\"%s\")" %(fn,ext)
    cursor.execute(query2)
    conn.commit()

    if(len(err) == 0):
        print "Content-Type: text/html"
        print cookieDict
        print
        print '''
            <html>
            <head>
                <title>CSCI 4140 Assignment 1 -- Instagram -- Finish</title>
                <link rel="stylesheet" href="/css/bootstrap.min.css">
                <link rel="stylesheet" href="/css/pagination.css">
            </head>
            <body>
            <div class="container">
                <div class="row">
        '''
        # print readPath , savePath
        print '<br><img id="im" src="%s" style="width:500px"/>' %(os.path.join(readFinishDir, fn+ext))
        print '''
                </div>
                <div class="row">
                    <form method="post" action="index.cgi">
                        Permalink: <span class="btn btn-default btn-file"> %s <input type="input" name="edit" disabled></span>'

                        <span class="btn btn-default btn-file"> Back to Home <input type="submit"></span>
                    </form>
                </div>
            </div>
            </body>
            </html>
        ''' %('http://'+os.environ['HTTP_HOST']+os.path.join(readFinishDir, fn+ext))
    else:
        print "Content-Type: text/html"
        print cookieDict
        print
        print "Error"

elif ('edit' in form):
    print "Content-Type: text/html"
    print
    # print "edit"
    ext = form['edit'].value
    query = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,1,fn+'_'+str(1),ext)
    # print query
    cursor.execute(query)
    conn.commit()
    readPath = os.path.join(saveDir,fn+ext)
    newfn = fn + "_" + str(1)
    savePath = os.path.join(saveDir,newfn+ext)
    cmd = ['cp',readPath,savePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()

    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Edit</title>
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            <div class="row">
                <div class="col-sm-6">
    '''

    print '<br><img id="im" src="%s" style="width:500px"/>' %(os.path.join(readDir, newfn + ext))
    print '''
                </div>
                <div class="col-sm-6">
                    <br>
                    <div class="upload">
                        <form method="post" action="edit.cgi">
                            Filter:&nbsp;&nbsp;&nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Border <input type="submit" name="filter" value="border"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lomo <input type="submit" name="filter" value="lomo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lens Flare <input type="submit" name="filter" value="lf"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Black & White <input type="submit" name="filter" value="bw"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Blur <input type="submit" name="filter" value="blur"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            Annotate:&nbsp;&nbsp;&nbsp;&nbsp;
                            Message <input type="text" name="message" value="Message"/>
                            <br>
                            <br>
                            Font Type
                            <br>
                            Font Size
                            <br>
                            <span class="btn btn-default btn-file"> Annotate Top <input type="submit" name="filter" value="top"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Annotate Bottom <input type="submit" name="filter" value="bottom"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            <span class="btn btn-default btn-file"> Undo <input type="submit" name="undo" value="undo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Discard <input type="submit" name="cancel" value="%s"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Finish <input type="submit" name="finish" value="finish"></span>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        </body>
        </html>
    '''

elif ('filter' in form):
    print "Content-Type: text/html"
    print

    filter_type = form['filter'].value
    query = "SELECT edit_name, ext , step FROM edit WHERE name = \"%s\" GROUP BY step DESC LIMIT 1" %(fn)
    # print query
    cursor.execute(query)
    result = cursor.fetchall()
    oldfn = result[0][0]
    ext = result[0][1]
    step = result[0][2]
    newfn = fn + "_" +str(int(step)+1)
    inpath = os.path.join(saveDir,oldfn + ext)
    outpath = os.path.join(saveDir,newfn + ext)
    if (filter_type == "border"):
        result = image_process.border(inpath,outpath)
        if(result == "Success"):
            query2 = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,int(step)+1,fn+'_'+str(int(step)+1),ext)
            # print query
            cursor.execute(query2)
            conn.commit()

    elif(filter_type == "lomo"):
        result = image_process.lomo(inpath,outpath)
        if(result == "Success"):
            query2 = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,int(step)+1,fn+'_'+str(int(step)+1),ext)
            # print query
            cursor.execute(query2)
            conn.commit()

    elif(filter_type == "lf"):
        result = image_process.lensFlare(inpath,outpath)
        if(result == "Success"):
            query2 = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,int(step)+1,fn+'_'+str(int(step)+1),ext)
            # print query
            cursor.execute(query2)
            conn.commit()

    elif(filter_type == "bw"):
        result = image_process.blackWhite(inpath,outpath)
        if(result == "Success"):
            query2 = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,int(step)+1,fn+'_'+str(int(step)+1),ext)
            # print query
            cursor.execute(query2)
            conn.commit()

    elif(filter_type == "blur"):
        result = image_process.blur(inpath,outpath)
        if(result == "Success"):
            query2 = "INSERT INTO edit(name,step,edit_name,ext) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" %(fn,int(step)+1,fn+'_'+str(int(step)+1),ext)
            # print query
            cursor.execute(query2)
            conn.commit()

    if (result != "Success"):

        print "Error<br>"
        print result

    else:
        print '''
            <html>
            <head>
                <title>CSCI 4140 Assignment 1 -- Instagram -- Resume Edit</title>
                <link rel="stylesheet" href="/css/bootstrap.min.css">
                <link rel="stylesheet" href="/css/pagination.css">
            </head>
            <body>
            <div class="container">
                <div class="row">
                    <div class="col-sm-6">
        '''
        # print inpath , outpath
        print '<br><img id="im" src="%s" style="width:500px"/>' %(os.path.join(readDir, newfn +ext))
        print '''
                    </div>
                    <div class="col-sm-6">
                        <br>

                        <div class="upload">
                            <form method="post" action="edit.cgi">
                                Filter:&nbsp;&nbsp;&nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Border <input type="submit" name="filter" value="border"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Lomo <input type="submit" name="filter" value="lomo"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Lens Flare <input type="submit" name="filter" value="lf"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Black & White <input type="submit" name="filter" value="bw"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Blur <input type="submit" name="filter" value="blur"></span>
                            </form>
                            <hr>
                            <form method="post" action="edit.cgi">
                                Annotate:&nbsp;&nbsp;&nbsp;&nbsp;
                                <input type="text" name="message" value="Message"/>
                                <br>
                                <br>
                                Font Type
                                <br>
                                Font Size
                                <br>
                                <span class="btn btn-default btn-file"> Annotate Top <input type="submit" name="filter" value="top"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Annotate Bottom <input type="submit" name="filter" value="bottom"></span>
                            </form>
                            <hr>
                            <form method="post" action="edit.cgi">
                                <span class="btn btn-default btn-file"> Undo <input type="submit" name="undo" value="undo"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Discard <input type="submit" name="cancel" value="%s"></span>
                                &nbsp;&nbsp;
                                <span class="btn btn-default btn-file"> Finish <input type="submit" name="finish" value="finish"></span>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            </body>
            </html>
        ''' %(ext)

elif ('undo' in form):
    query = "DELETE FROM edit WHERE name = \"%s\" ORDER BY step DESC LIMIT 1 " %(fn)
    cursor.execute(query)
    conn.commit()
    query = "SELECT edit_name, ext , step FROM edit WHERE name = \"%s\" GROUP BY step DESC LIMIT 1" %(fn)

    # print query
    cursor.execute(query)
    result = cursor.fetchall()
    fn = result[0][0]
    ext = result[0][1]
    filename = fn + ext

    # print filename
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Resume Edit</title>
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            <div class="row">
                <div class="col-sm-6">
    '''

    print '<br><img id="im" src="%s" style="width:500px"/>' %(os.path.join(readDir, filename))
    print '''
                </div>
                <div class="col-sm-6">
                    <br>
                    <div class="upload">
                        <form method="post" action="edit.cgi">
                            Filter:&nbsp;&nbsp;&nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Border <input type="submit" name="filter" value="border"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lomo <input type="submit" name="filter" value="lomo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lens Flare <input type="submit" name="filter" value="lf"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Black & White <input type="submit" name="filter" value="bw"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Blur <input type="submit" name="filter" value="blur"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            Annotate:&nbsp;&nbsp;&nbsp;&nbsp;
                            <input type="text" name="message" value="Message"/>
                            <br>
                            <br>
                            Font Type
                            <br>
                            Font Size
                            <br>
                            <span class="btn btn-default btn-file"> Annotate Top <input type="submit" name="filter" value="top"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Annotate Bottom <input type="submit" name="filter" value="bottom"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            <span class="btn btn-default btn-file"> Undo <input type="submit" name="undo" value="undo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Discard <input type="submit" name="cancel" value="%s"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Finish <input type="submit" name="finish" value="finish"></span>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        </body>
        </html>
    ''' %(ext)


else:
    print "Content-Type: text/html"
    print

    query = "SELECT edit_name, ext , step FROM edit WHERE name = \"%s\" GROUP BY step DESC LIMIT 1" %(fn)

    # print query
    cursor.execute(query)
    result = cursor.fetchall()
    # print result
    newfn = result[0][0]
    ext = result[0][1]
    filename = newfn + ext

    # print filename
    print '''
        <html>
        <head>
            <title>CSCI 4140 Assignment 1 -- Instagram -- Resume Edit</title>
            <link rel="stylesheet" href="/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/pagination.css">
        </head>
        <body>
        <div class="container">
            <div class="row">
                <div class="col-sm-6">
    '''

    print '<br><img id="im" src="%s" style="width:500px"/>' %(os.path.join(readDir, filename))
    print '''
                </div>
                <div class="col-sm-6">
                    <br>
                    <div class="upload">
                        <form method="post" action="edit.cgi">
                            Filter:&nbsp;&nbsp;&nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Border <input type="submit" name="filter" value="border"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lomo <input type="submit" name="filter" value="lomo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Lens Flare <input type="submit" name="filter" value="lf"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Black & White <input type="submit" name="filter" value="bw"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Blur <input type="submit" name="filter" value="blur"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            Annotate:&nbsp;&nbsp;&nbsp;&nbsp;
                            <input type="text" name="message" value="Message"/>
                            <br>
                            <br>
                            Font Type
                            <br>
                            Font Size
                            <br>
                            <span class="btn btn-default btn-file"> Annotate Top <input type="submit" name="filter" value="top"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Annotate Bottom <input type="submit" name="filter" value="bottom"></span>
                        </form>
                        <hr>
                        <form method="post" action="edit.cgi">
                            <span class="btn btn-default btn-file"> Undo <input type="submit" name="undo" value="undo"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Discard <input type="submit" name="cancel" value="%s"></span>
                            &nbsp;&nbsp;
                            <span class="btn btn-default btn-file"> Finish <input type="submit" name="finish" value="finish"></span>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        </body>
        </html>
    ''' %(ext)

cursor.close()
conn.close()