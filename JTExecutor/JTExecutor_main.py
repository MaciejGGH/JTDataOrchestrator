# -*- coding: utf-8 -*
#-------------------------------------------------------------------------------
# Name:        Executor
# Purpose:     Execute external tool e.g. PowerCenter
#
# Author:      Maciej Grabowski
#
# Created:     22.02.2017
# Copyright:   (c) macie 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cherrypy
from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname

affectedFiles=[]
@cherrypy.expose
class JTExecutor(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        global affectedFiles
        template_dir = join(dirname(__file__), 'templates')
        jinja_env = Environment(loader = FileSystemLoader(template_dir), autoescape = True)
        template = jinja_env.get_template('JTSchedulerIndex.html')
        #return cherrypy.session['mystring']
        #return ('{0}\n'.format(f.encode('utf-8')) for f in affectedFiles)
        return template.render(affectedFiles = affectedFiles)

    def POST(self):
        global affectedFiles
        ##print '='*150
        #return affectedFiles
        li = ''.join('<li>{0}</li>'.format(f) for f in affectedFiles)
        return '<ul>{0}</ul>'.format(li)

    def PUT(self, fileName):
        global affectedFiles
        print fileName.encode('utf-8')
        #cherrypy.session['mystring'] = [fileName]
        affectedFiles += [fileName]

    def DELETE(self):
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            ##'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(JTExecutor(), '/', conf)