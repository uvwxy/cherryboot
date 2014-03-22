'''
Created on 22.03.2014

@author: uvwxy
'''
import cherrypy
import os
import time

from mako.template import Template
from mako.lookup import TemplateLookup
        
if __name__ == '__main__':
    pass

libTemplates = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"../../www-lib/mako/");
pageTemplates = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"mako/");
lookup = TemplateLookup(directories=[ libTemplates, pageTemplates])

class ExamplePage(object):
  
  @cherrypy.expose
  def index(self, *args, **kw):
    tmpl = lookup.get_template("index.html")
    title = "Title"
    return tmpl.render(title=title, params=kw)


  @cherrypy.expose
  def charttest(self, *args, **kw):
    tmpl = lookup.get_template("charttest.html")
    title = "Title"
    return tmpl.render(title=title, params=kw)
  
  @cherrypy.expose
  @cherrypy.tools.json_out()
  @cherrypy.tools.json_in()
  def getJson(self):
    result = {"series" : "test", "data" : [[int(time.time()), 0.8]]}
    return result
