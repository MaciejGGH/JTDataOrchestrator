# -*- coding: utf-8 -*
#-------------------------------------------------------------------------------
# Name:        Job-Triggering File Watcher
# Purpose:
#
# Author:      Maciej Grabowski
#
# Created:     22-02-2017
# Copyright:   (c) Maciej Grabowski 2017
# Licence:
#-------------------------------------------------------------------------------

import requests
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import ConfigParser
from os.path import join, dirname

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
        dir = dirname(__file__)
        configFileName = join(dir, r'cfg\filewatcher.cfg')
        try:
            configReady = False
            #config = ConfigParser.SafeConfigParser()
            #Forcing parser to reuse existing letter case
            config = ConfigParser.RawConfigParser()
            config.optionxform = lambda option: option
            config.read(configFileName)
            self.sourceDir = config.get('Common', 'SourceDir')
            self.schedulerServiceAddress = config.get('Common', 'SchedulerWebAddress')
            configReady = True

        except Exception as e:
            print e
        #todo: check if path exists
        print 'Monitorig started for path: {0}'.format(self.sourceDir)
        print 'Ctrl+C to stop.'

    def on_any_event(self, event):
        s = requests.Session()
        #print "e=", event
        #print event.__dict__
        try:
            affectedFile = event.dest_path.encode('utf-8')
            destPath = event.dest_path
            print '{1} {0}'.format(event.event_type, affectedFile)
        except:
            if not event.is_directory:
                affectedFile = event.src_path.encode('utf-8')
                print '{1} {0}'.format(event.event_type, affectedFile)
        r = s.put(self.schedulerServiceAddress, params={'fileName': affectedFile})
        print r.status_code, r.text

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    ##path = sys.argv[1] if len(sys.argv) > 1 else '.'
    #event_handler = LoggingEventHandler()
    observer = Observer()
    event_handler = MyEventHandler(observer)
    observer.schedule(event_handler, event_handler.sourceDir, recursive=True)
    observer.start()
    i=0
    try:
        while True:
            i+=1
            time.sleep(1)
            if i == 120:
                print 'Monitoring {0}...'.format(self.sourceDir)
                i=0
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
