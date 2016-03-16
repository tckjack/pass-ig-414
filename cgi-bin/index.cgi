#!/usr/bin/env python

import MySQLdb
import gencookie
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()

conn = MySQLdb.connect(
    host = 'db',
    user = 'csci4140',
    passwd = 'opensource',
    db = 'instagram'
)

cursor = conn.cursor()
fn = gencookie.find_cookie()
page = 1
if('page' in form):
    page = form['page'].value
else:
    page = 1

print 'Content-type: text/html'
print

print '''
<html>

<head>
  <title>CSCI 4140 Assignment 1 -- Instagram</title>
  <link rel="stylesheet" href="/css/bootstrap.min.css">
  <link rel="stylesheet" href="/css/pagination.css">
</head>

<body>
  <div class="container">
    <div class="row" align="right">
      <br>
'''

if (fn != None):
    print '''
      <form class="resume" action="edit.cgi" method="post">
        <span class="btn btn-default btn-file">Resume<input type="submit" name="resume"/></span>
      </form>
    '''

else :
    print "<br>"


print '''
      <hr>
    </div>
  </div>
  <div class="container">
    <div class="row">
    <h1>Images:</h1><br>
'''
query_total = "SELECT count(*) FROM images"
query = "SELECT * FROM images ORDER BY pid DESC LIMIT 8 OFFSET %d " %(((int(page)-1)*8))
cursor.execute(query_total)
result = cursor.fetchall()
count = result[0][0]
cursor.execute(query)
total_page = int(round(count/8))+1
images = cursor.fetchall()

for image in images:
    fn = image[1]
    ext = image[2]
    filename =  fn + ext
    print '''
    <div class="col-sm-3">
        <br>
        <a href="/images/%s"><img src="/images/%s" alt="#" height="200" width="200" /></a>
        <br>
    </div>
    ''' %(filename,filename)

print '''
    </div>
  </div>
  <div class="container">
    <div class="col-sm-12">
      <hr>
      <div id="page">
        <ul class="pagination">
'''
# print "page=%d total_page=%d" %(int(page),int(total_page))
if (page == 1):
    print "<li class=\"disabled\"><a href=\"#\"><</a></li>"
else:
    print "<li><a href=\"index.cgi?page=%d\"><</a></li>" %( int(page) - 1 )
print "<li><a href=\"#\">page %d of %d</a></li>" %(int(page),int(total_page))
if (int(page) == int(total_page)):
    print "<li class=\"disabled\"><a href=\"#\">></a></li>"
else:
    print "<li><a href=\"index.cgi?page=%d\">></a></li>" %( int(page) + 1 )


print '''
        </ul>
      </div>
      <hr>
      <div id="upload">
        <br>
        <form enctype="multipart/form-data" action="upload.cgi" method="post">
          Please upload an image:
          <span class="btn btn-default btn-file">Browse<input type="file" name="pic" accept="image/gif, image/jpeg, image/png"></span>
          <span class="btn btn-default btn-file">Upload<input type="submit"></span>
        </form>
      </div>
    </div>
  </div>

</body>

</html>
'''

cursor.close()
conn.close()