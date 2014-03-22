#!/usr/bin/python
'''
Created on 22.03.2014

@author: uvwxy
'''

import cherrypy
import os
import ConfigParser
from www.page.main import ExamplePage
from www.rest.main import ExampleRest

cfgParser = ConfigParser.ConfigParser()
cfgParser.read("server.config")
dirCss = os.path.join(os.path.dirname(os.path.realpath(__file__)), "www-lib/css/")
dirFonts = os.path.join(os.path.dirname(os.path.realpath(__file__)), "www-lib/fonts/")
dirJs = os.path.join(os.path.dirname(os.path.realpath(__file__)), "www-lib/js/")

print dirCss
print dirFonts
print dirJs

        
# server start and configuration
conf = {
    '/css':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir': dirCss,
            },
    '/fonts':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir': dirFonts,
            },
     '/js':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir': dirJs,
            },
    'global': {
        'server.socket_host': cfgParser.get("server", "host"),
        'server.socket_port': cfgParser.getint("server", "port"),
    }
}

cherrypy.tree.mount(ExamplePage(), "/", config=conf);
cherrypy.tree.mount(ExampleRest(), "/api/v1/songs", {'/':
        {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    });
cherrypy.engine.start()
cherrypy.engine.block();
