'''
Created on 22.03.2014

This is the example from: http://docs.cherrypy.org/en/latest/tutorial/REST.html
@author: uvwxy
'''

from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy
import time
import random

class RestSeriesConfig():
    
    @cherrypy.tools.json_out()
    def GET(self, id=None):
        print "TEST1"
        config1 = {"title" : "CPU 1", "id" : "g1", "valueField": "v1", "lineColor" : "#ff0000"}
        config2 = {"title" : "CPU 2", "id" : "g2", "valueField": "v2", "lineColor" : "#00ff00"}
        config3 = {"title" : "CPU 3", "id" : "g3", "valueField": "v3", "lineColor" : "#0000ff"}

        return {"timeField" : "ts", "graphs" : [config1, config2, config3]}
    exposed = True

class RestSeriesData():
    
    @cherrypy.tools.json_out()
    def GET(self, id=None):
        print "TEST1"
        return  {"ts" : int(time.time()), "v1" : random.randint(1,100), "v2" : random.randint(1,100), "v3" : random.randint(1,100)}
    exposed = True
