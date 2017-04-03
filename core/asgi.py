"""
This is the Channel Layer instance of the ASGI Spec for deployment.
It acts in between protocol (frontend) server and the Websocket consumer/WSGI app code in workers.

Usage
-----
1. Run the following code for starting the protocol server (Daphne) with it.
```
daphne core.asgi:channel_layer
```
2. Run the normal `./manage.py runworker` cmd to start as many workers as needed.

Note
----
This is for deployment only, using `./manage.py runserver` in dev doesn't need this unless you want to 
access the channel_layer directly which is needed when manually creating the Channel/Group object for 
.send(content_dict) in other part of Django app code (non-consumer).
"""
import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

channel_layer = get_channel_layer()