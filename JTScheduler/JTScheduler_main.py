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
from os.path import join, dirname
import ConfigParser

dir = dirname(__file__)
configFileName = join(dir, r'cfg\scheduler.cfg')

executors={}
affectedFiles=[] #list of files coming from FileMatchers

# get config
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

# fetch filematchers
try:
    fm = open(join(dir, r'job_config\filematchers.csv'), 'r').readlines()
    for line in fm:
        filematcherId, jobId, type, value = line.split(',')
except Exception as e:
    print e


@cherrypy.expose
class JTSchedulerWebService(object):
    @cherrypy.tools.accept(media='text/plain')

    def listRegistrations(self):
        print 1
        #return True
    listRegistrations.exposed = True

    def GET(self):
        global affectedFiles
        template_dir = join(dirname(__file__), 'templates')
        jinja_env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = jinja_env.get_template('JTSchedulerIndex.html')
        # return cherrypy.session['mystring']
        # return ('{0}\n'.format(f.encode('utf-8')) for f in affectedFiles)
        return template.render(affectedFiles = affectedFiles)

    def POST(self):
        global affectedFiles
        # print '='*150
        # return affectedFiles
        li = ''.join('<li>{0}</li>'.format(f) for f in affectedFiles)
        return '<ul>{0}</ul>'.format(li)

    def PUT(self, fileName):
        def checkJobsToActivate(fileName):
            pass
        global affectedFiles
        print fileName.encode('utf-8')
        # cherrypy.session['mystring'] = [fileName]
        affectedFiles += [fileName]
        # check filematchers for jobs to be activated
        # send notification to Executor if FM found


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
    cherrypy.quickstart(JTSchedulerWebService(), '/', conf)