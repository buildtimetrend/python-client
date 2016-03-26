#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
"""
Retrieve Travis CI build data and log to Keen.io.

Copyright (C) 2014-2016 Dieter Adriaenssens <ruleant@users.sourceforge.net>

This file is part of buildtimetrend/python-client
<https://github.com/buildtimetrend/python-client/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function

import sys
from buildtimetrend.travis.parser import TravisData
from buildtimetrend.settings import Settings
from buildtimetrend import keenio

CLIENT_NAME = "buildtimetrend/python-client service.py"
CLIENT_VERSION = "0.4.dev"

def retrieve_and_store_data(argv):
    """
    Load timing and build data, process and store it.

    Retrieve timing and build data from Travis CI log, parse it
    and store the result in Keen.io.
    Parameters:
    - argv : command line parameters
    """
    settings = Settings()
    settings.set_client(CLIENT_NAME, CLIENT_VERSION)

    # load settings from config file, env_var and cli parameters
    if settings.load_settings(argv, "config_service.yml") is None:
        return

    build = settings.get_setting('build')
    if build is None:
        print("Build number is not set, use --build=build_id")
        return

    travis_data = TravisData(settings.get_project_name(), build)

    # retrieve build data using Travis CI API
    print(
        "Retrieve build #{:s} data of {:s} from Travis CI".format(
            build, settings.get_project_name()
        )
    )
    travis_data.get_build_data()

    # process all build jobs
    travis_data.process_build_jobs()

    if not keenio.is_writable():
        print("Keen IO write key not set, no data was sent")
        return

    # send build job data to Keen.io
    for build_job in travis_data.build_jobs:
        print("Send build job #{:s} data to Keen.io".format(build_job))
        keenio.send_build_data_service(travis_data.build_jobs[build_job])

if __name__ == "__main__":
    retrieve_and_store_data(sys.argv)
