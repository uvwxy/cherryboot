'''
Created on 22.03.2014

This is the example from: http://docs.cherrypy.org/en/latest/tutorial/REST.html
@author: uvwxy
'''

from mako.template import Template
from mako.lookup import TemplateLookup

songs = {
        '1': {
            'title': 'Lumberjack Song',
            'artist': 'Canadian Guard Choir'
        },
    
        '2': {
            'title': 'Always Look On the Bright Side of Life',
            'artist': 'Eric Idle'
        },
    
        '3': {
            'title': 'Spam Spam Spam',
            'artist': 'Monty Python'
        }
    }

class ExampleRest():
    def GET(self, id=None):
        if id == None:
            return('Here are all the songs we have: %s' % songs)
        elif id in songs:
            song = songs[id]
            return('Song with the ID %s is called %s, and the artist is %s' % (id, song['title'], song['artist']))
        else:
            return('No song with the ID %s :-(' % id)
        
    def POST(self, title, artist):
    
        id = str(max([int(_) for _ in songs.keys()]) + 1)
    
        songs[id] = {
            'title': title,
            'artist': artist
        }
        return ('Create a new song with the ID: %s' % id)
    
    def PUT(self, id, title=None, artist=None):
        if id in songs:
            song = songs['id']
    
            song['title'] = title or song['title']
            song['artist'] = artist or song['artist']
    
            return('Song with the ID %s is now called %s, and the artist is now %s' % (id, song['title'], song['artist']))
        else:
            return('No song with the ID %s :-(' % id)
        
    def DELETE(self, id):
        if id in songs:
            songs.pop(id)
    
            return('Song with the ID %s has been deleted.' % id)
        else:
            return('No song with the ID %s :-(' % id)
    exposed = True
