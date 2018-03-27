"""
This is required by django channels package as a step upon installation.

Hint
----
Look at this file as if you were looking at urls.py for the WSGI version 
of the same project.

@author Tim Lauv

"""
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})