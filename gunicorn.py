# http://cheng.logdown.com/posts/2016/10/20/deploy-django-nginx-gunicorn-on-mac-osx-part-2
# cd ~/source/ba-namotswe/
# gunicorn -c gunicorn.conf.py ba-namotswe.wsgi --pid ~/source/ba-namotswe/logs/gunicorn.pid --daemon
#

import os

SOURCE_ROOT = os.path.expanduser('~/source')

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
errorlog = os.path.join(SOURCE_ROOT, 'ba-namotswe/logs/gunicorn-error.log')  # Make sure you have the log folder create
accesslog = os.path.join(SOURCE_ROOT, 'ba-namotswe/logs/gunicorn-access.log')
loglevel = 'debug'
