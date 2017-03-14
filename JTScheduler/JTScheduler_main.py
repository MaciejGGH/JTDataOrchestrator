# -*- coding: utf-8 -*
#-------------------------------------------------------------------------------
# Name:        Informatica Scheduler
# Purpose:
#
# Author:      Maciej Grabowski
#
# Created:     22.02.2017
# Copyright:   (c) macie 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cherrypy
from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath, sep
from os import getcwd
import ConfigParser





##@cherrypy.expose
class JTSchedulerWebService(object):
    @cherrypy.tools.accept(media='text/plain')

    def __init__(self):
        self.executors={}
        self.affectedFiles=[] #list of files coming from FileMatchers
        # get config
        dir = dirname(__file__)
        configFileName = join(dir, r'cfg\scheduler.cfg')

        # fetch filematchers
        try:
            fm = open(join(dir, r'job_config\filematchers.csv'), 'r').readlines()
            for line in fm:
                filematcherId, jobId, type, value = line.split(',')
        except Exception as e:
            print e

        try:
            configReady = False
            #config = ConfigParser.SafeConfigParser()
            #Forcing parser to reuse existing letter case
            config = ConfigParser.RawConfigParser()
            config.optionxform = lambda option: option
            config.read(configFileName)
            ExecutorList = config.get('Common', 'ExecutorList').split(',')
            for executorName in ExecutorList:
                executorAddress = config.get('Executors', executorName)
                executors[executorName] = executorAddress

            configReady = True

        except Exception as e:
            print e

    def listRegistrations(self):
        print 1
        return 'HW'
    listRegistrations.exposed = True

##    ##def GET(self):
    def status(self):
        template_dir = join(dirname(__file__), 'templates')
        jinja_env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = jinja_env.get_template('JTSchedulerIndex.html')
        return template.render(affectedFiles = self.affectedFiles)
    status.exposed = True

##    def POST(self):
##        self.affectedFiles
##        print '='*150
##        # return affectedFiles
##        li = ''.join('<li>{0}</li>'.format(f) for f in self.affectedFiles)
##        return '<ul>{0}</ul>'.format(li)

##

    def registerFile(self):
##        #def PUT(self, fileName):
##        def checkJobsToActivate(fileName):
##            pass
##        print '<>'*150
##        print cherrypy.request.params##['fileName']
##        #self.affectedFiles += [fileName]
##        # check filematchers for jobs to be activated
##        # send notification to Executor if FM found
        return 'fileName'
    registerFile.exposed = True


##    def DELETE(self):
##        cherrypy.session.pop('mystring', None)

    def index(self):
        return self.affectedFiles
    index.exposed = True

if __name__ == '__main__':

    # On Startup
    current_dir = dirname(abspath(__file__)) + sep
    config = {
        'global': {
##            'environment': 'production',
##            'log.screen': True,
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'engine.autoreload_on': True,
            'log.error_file': join(current_dir, 'errors.log'),
            'log.access_file': join(current_dir, 'access.log'),
        },

##            '/': {
##                #'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
##                'tools.sessions.on': True,
##                #'tools.staticdir.root': current_dir
##        },
##            '/registerFile': {
##                #'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
##                'tools.sessions.on': True,
##                ##'tools.staticdir.root': current_dir
##        },
            '/css': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': '/css'
        },
            '/css/mystyle.css': {
                'tools.staticfile.debug': True,
                'tools.staticfile.on': True,
                'tools.staticfile.filename': join(join(current_dir, 'css'), 'mystyle.css')
        },
        }
    #cherrypy.quickstart(JTSchedulerWebService(), '/', config)
    cherrypy.tree.mount(JTSchedulerWebService(), '/', config)

    cherrypy.engine.start()
    cherrypy.engine.block()
