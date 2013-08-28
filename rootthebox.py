#!/usr/bin/env python
'''
    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
----------------------------------------------------------------------------

This file is the main starting point for the application, based on the 
command line arguments it calls various components setup/start/etc.

'''


import os
import sys
import logging

from optparse import OptionParser
from datetime import datetime
from libs.ConsoleColors import *


__version__ = 'Root the Box - v0.3.0'
current_time = lambda: str(datetime.now()).split(' ')[1].split('.')[0]


def serve(options, *args, **kwargs):
    ''' Starts the application '''
    from libs.ConfigManager import ConfigManager  # Sets up logging
    from handlers import start_server
    print(INFO+'%s : Starting application ...' % current_time())
    start_server()


def create(options, *args, **kwargs):
    ''' Creates/bootstraps the database '''
    from libs.ConfigManager import ConfigManager  # Sets up logging
    from models import create_tables, boot_strap
    print(INFO+'%s : Creating the database ...' % current_time())
    create_tables()
    print(INFO+'%s : Bootstrapping the database ...' % current_time())
    boot_strap()


def recovery(options, *args, **kwargs):
    ''' Starts the recovery console '''
    from libs.ConfigManager import ConfigManager  # Sets up logging
    from setup.recovery import RecoveryConsole
    print(INFO+'%s : Starting recovery console ...' % current_time())
    console = RecoveryConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        print(INFO + "Have a nice day!")

def setup_xml(options, *args, **kwargs):
    ''' Imports XML file(s) '''
    index = sys.argv.index('-x') if '-x' in sys.argv else sys.argv.index('--xml')
    if not index + 1 < len(sys.argv):
        print(WARN+"Missing .xml file/directory parameter")
        os._exit(1)
    from libs.ConfigManager import ConfigManager  # Sets up logging
    from setup.importers import import_xml
    import_xml(sys.argv[index + 1])

def setup(options, *args, **kwargs):
    ''' Imports a setup file '''
    from libs.ConfigManager import ConfigManager  # Sets up logging
    print(INFO+"%s : Running default setup file 'setup/game.py' ..." % current_time())
    try:
        from setup import game
    except Exception as error:
        logging.exception("Game setup script raised an exception!")
        print(WARN+"Setup Error: Game script failed with "+str(error))
        sys.exit()
    print(INFO+"Setup file completed successfully.")

def test(options, *args, **kwargs):
    print "Test has been fired"
    from setup import XmlGameImporter
    XmlGameImporter.import_xml_box_files_for_game("sample", 1)

### Main
if __name__ == '__main__':
    if not 1 < len(sys.argv):
        sys.argv.append('-h')
    parser = OptionParser(
        usage=bold+"rootthebox.py"+W+" <options>",
        version=__version__,
    )
    parser.add_option(
        "-c", "--create-tables",
        action="callback",
        callback=create,
        help="create and initialize database tables (run once)"
    )
    parser.add_option(
        "-s", "--start",
        action="callback",
        callback=serve,
        help="start the server"
    )
    parser.add_option(
        "-x", "--xml",
        action="callback",
        callback=setup_xml,
        help="import xml file, or directory or file(s)"
    )
    parser.add_option(
        "-g", "--game-script",
        action="callback",
        callback=setup,
        help="run a game setup script (setup/game.py)"
    )
    parser.add_option(
        "-r", "--recovery",
        action="callback",
        callback=recovery,
        help="start the admin recovery console"
    )
    #TODO remove this before production
    parser.add_option(
        "-t", "--test",
        action="callback",
        callback=test,
        help="run testing code in the 'test' function (for debugging and development purposes)"
    )
    parser.parse_args()
