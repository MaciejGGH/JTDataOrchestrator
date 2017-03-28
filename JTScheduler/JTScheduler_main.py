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


class job():
    def __init__(self, jobId, executorName, name, description, groupId, statusId, type, expectedBy, maxRunTime, maxRetryCnt, maxThreads, updatedBy, updatedOn, version):
        self.jobId = jobId.strip()
        self.executorName = executorName.strip()
        self.name = name.strip()
        self.description = description
        self.groupId = groupId.strip()
        self.statusId = statusId.strip()
        self.type = type.strip()
        self.expectedBy = expectedBy.strip()
        self.maxRunTime = maxRunTime.strip()
        self.maxRetryCnt = maxRetryCnt.strip()
        self.maxThreads = maxThreads.strip()
        self.updatedBy = updatedBy.strip()
        self.updatedOn = updatedOn.strip()
        self.version = version.strip()

    def __str__(self):
        return 'Job: {0}, running on: {1}'.format(self.name, self.executorName)

class filematcher():
    def __init__(self, filematcherId, jobId, type, value):
        self.filematcherId = filematcherId.strip()
        self.jobId = jobId.strip()
        self.type = type.strip()
        self.value = value.strip()
    def __str__(self):
        return 'jobId: {0}, type: {1}, value: {2}'.format(self.jobId, self.type, self.value)

class JTSchedulerWebService(object):
    @cherrypy.tools.accept(media='text/plain')

    def __init__(self):
        self.executors = {}
        self.affectedFiles = [] #list of files coming from FileMatchers
        self.jobs = {}
        self.filematchers = {}
        # get config
        self.registerJobs()
        self.registerFileMatchers()
        self.registerExecutors()
        self.filematcherseparator = ';'

    def registerExecutors(self):
        dir = dirname(__file__)
        configFileName = join(dir, r'cfg\scheduler.cfg')
        config = ConfigParser.RawConfigParser()
        config.optionxform = lambda option: option
        config.read(configFileName)
        ExecutorList = config.get('Common', 'ExecutorList').split(',')
        for executorName in ExecutorList:
            executorAddress = config.get('Executors', executorName)
            self.executors[executorName] = executorAddress
    registerExecutors.exposed = True

    def registerJobs(self):
        dir = dirname(__file__)
        for jobLine in open(join(dir, r'job_config\jobs.cfg'), 'r').readlines()[1:]:
            jobId, executorName, name, description, groupId, statusId, type, expectedBy, maxRunTime, maxRetryCnt, maxThreads, updatedBy, updatedOn, version = jobLine.replace('\n', '').split(',')
            self.jobs[jobId.strip()] = job(jobId, executorName, name, description, groupId, statusId, type, expectedBy, maxRunTime, maxRetryCnt, maxThreads, updatedBy, updatedOn, version)
    registerJobs.exposed = True

    def registerFileMatchers(self):
        dir = dirname(__file__)
        for fmLine in open(join(dir, r'job_config\filematchers.cfg'), 'r').readlines()[1:]:
            filematcherId, jobId, type, value = fmLine.replace('\n', '').split(',')
            newFM = filematcher(filematcherId, jobId, type, value)
            try:
                self.filematchers[jobId.strip()] += [newFM]
            except:
                self.filematchers[jobId.strip()] = [newFM]
    registerFileMatchers.exposed = True

    def listRegistrations(self):
        return '<ul>' + ''.join('<li>{0}</li>'.format(f) for f in self.affectedFiles) + '</ul>'
    listRegistrations.exposed = True

    def viewJobs(self):
        print self.jobs
        return '<ul>' + ''.join('<li>{0}</li>'.format(self.jobs[k]) for k in self.jobs) + '</ul>'
    viewJobs.exposed = True

    def viewFilematchers(self):
        fmList = '<ul>'
        for jobId in self.filematchers:
            print '>{0}<'.format(jobId.strip())
            fmList += '<li>{0}</li>'.format(self.jobs[jobId].name)
            fmList += '<ul>' + ''.join('<li>{0}</li>'.format(fm) for fm in self.filematchers[jobId]) + '</ul>'
        fmList += '</ul>'
        return fmList
        #return '<ul>' + ''.join('<li>{0}</li>'.format(self.filematchers[jobId]) for jobId in self.filematchers) + '</ul>'
    viewFilematchers.exposed = True

    def viewExecutors(self):
        print self.executors
        return '<ul>' + ''.join('<li>{0}:{1}</li>'.format(k, self.executors[k]) for k in self.executors) + '</ul>'
    viewExecutors.exposed = True

    def status(self):
        template_dir = join(dirname(__file__), 'templates')
        jinja_env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = jinja_env.get_template('JTSchedulerIndex.html')
        return template.render(affectedFiles = self.affectedFiles)
    status.exposed = True

    def registerFile(self, fileName, testMode = 0):
        def checkJobsToRun(fileName):
            jobsToRun = []
            for jobId in self.filematchers:
                activateJob = True
                for fm in self.filematchers[jobId]:
                    #print fm
                    if fm.type == 'FS':
                        if fileName[:len(fm.value)] != fm.value: activateJob = False
                    elif fm.type == 'FE':
                        if fileName[-1*len(fm.value):] != fm.value: activateJob = False
                    elif fm.type == 'FM':
                        if fileName != fm.value: activateJob = False
                    elif fm.type == 'FSL':
                        matchFound = False
                        for val in fm.value.split(self.filematcherseparator):
                            if fileName[:len(val)] == val: matchFound = True
                        if not matchFound: activateJob = False
                    elif fm.type == 'FEL':
                        matchFound = False
                        for val in fm.value.split(self.filematcherseparator):
                            if fileName[-1*len(val):] == val: matchFound = True
                        if not matchFound: activateJob = False
                    elif fm.type == 'FML':
                        matchFound = False
                        for val in fm.value.split(self.filematcherseparator):
                            if fileName == val: matchFound = True
                        if not matchFound: activateJob = False
                if activateJob:
                    jobsToRun += [jobId]
            return jobsToRun

        self.affectedFiles += [fileName]
        print cherrypy.request.params['fileName']

        jobsToRun = checkJobsToRun(fileName)
        if testMode:
            li = ''.join('<li>{0}</li>'.format(self.jobs[jobId]) for jobId in jobsToRun)
            return '<ul>{0}</ul>'.format(li)
        else:
            #TODO: rum the jobs
            # check filematchers for jobs to be activated
            # send notification to Executor if FM found
            return fileName


        # check filematchers for jobs to be activated
        # send notification to Executor if FM found
        return fileName
    registerFile.exposed = True

    def requestCheck(self):
##        #def PUT(self, fileName):
        # check filematchers for jobs to be activated
        # send notification to Executor if FM found
        s = cherrypy.request.headers
        print s
        return ''.join(k + ': ' + s[k] + '<br>' for k in s)
    requestCheck.exposed = True

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
            'log.screen': True,
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'engine.autoreload_on': True,
            'log.error_file': join(current_dir, 'errors.log'),
            'log.access_file': join(current_dir, 'access.log'),
        },

            '/registerFile': {
                #'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                #'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
            '/css': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': '/css'
        },
            '/job_config': {
                'tools.staticfile.debug': True,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': '/job_config'

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
