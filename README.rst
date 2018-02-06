=============================
How to deploy it on openshift
=============================

----------
Quickstart
----------

- Create a project::

oc new-project python-cgi-example

- New an APP using the python 2.7 and the source code in the github::

oc new-app python:2.7~https://github.com/ayueei/python-cgi-example.git --name=hit-counter

- OpenShift will kick off build and deployment automatically. Then expose the service by::

oc expose svc/hit-counter --path=/cgi-bin/hit-counter.py

- Now you can visit the generated link in the web console.

-----
Notes
-----

There are some notes that you need to pay attention to (or your application may fail)

- Name the script that activates a server as app.py (default in OpenShift), or if you use another name, you need to add an environment variable in deployconfig: APP_FILE=<your_file>

- Make sure the scripts are executable (use "chmod +x <your_file>" to make the file executable)

- Add "#!/usr/bin/env python" into the first line of your python scripts

- When creating the route, you need to specify the path to your target script. ("/cgi-bin/hit-counter.py" in this example)

