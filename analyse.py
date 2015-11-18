#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
"""
Analyse buildtime data.

Read timestamps.csv, calculates stage duration and saves the result
to an xml file (native mode) or sends it to Keen.io (keen mode).

Usage :
  analyse.py -h
    --log=<log_level> : DEBUG, INFO, WARNING, ERRROR, CRITICAL
    --build=<buildID>
    --job=<jobID>
    --branch=<branchname>
    --repo=<repo_slug>
    --ci=<ci_platform> : fe. travis, jenkins, shippable, local, ...
    --result=<build_result> : fe. passed, failed, errored, ...
    --mode=<storage_mode> : fe. native, keen (default)

Copyright (C) 2014-2015 Dieter Adriaenssens <ruleant@users.sourceforge.net>

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

import os
import sys
import time
from buildtimetrend.settings import Settings
from buildtimetrend.buildjob import BuildJob
from buildtimetrend.travis import TravisData
from buildtimetrend.travis import load_travis_env_vars
from buildtimetrend.keenio import send_build_data
from buildtimetrend.tools import check_file
from buildtimetrend import logger

CLIENT_NAME = "buildtimetrend/python-client analyse.py"
CLIENT_VERSION = "0.3"

# use parameter for timestamps file and check if file exists
TIMESTAMP_FILE = os.getenv('BUILD_TREND_LOGFILE', 'timestamps.csv')
RESULT_FILE = os.getenv('BUILD_TREND_OUTPUTFILE', 'buildtimes.xml')
BUILD_TREND_INIT = os.getenv('BUILD_TREND_INIT', '0')


def analyse(argv, timestamp):
    """Analyse timestamp file."""
    settings = Settings()
    settings.set_client(CLIENT_NAME, CLIENT_VERSION)

    # load settings from config file, env_var and cli parameters
    if settings.load_settings(argv) is None:
        return

    # load Travis CI environment variables
    load_travis_env_vars()

    # read build data from timestamp CSV file
    build = BuildJob(TIMESTAMP_FILE, timestamp)

    # load build properties from settings
    build.load_properties_from_settings()

    # retrieve data from Travis CI API
    if build.get_property("ci_platform") == "travis":
        travis_data = TravisData(
            build.get_property("repo"),
            build.get_property("build"),
        )
        travis_data.get_build_data()
        build.set_started_at(travis_data.get_started_at())

    # log data
    if settings.get_setting("mode_native") is True:
        log_build_native(build)
    if settings.get_setting("mode_keen") is True:
        send_build_data(build)


def log_build_native(build):
    """Store build data in xml format."""
    # import dependency
    from lxml import etree

    # load previous buildtimes file, or create a new xml root
    if check_file(RESULT_FILE):
        try:
            root_xml = etree.parse(RESULT_FILE).getroot()
        except etree.XMLSyntaxError:
            logger.error('XML format invalid : a new file is created,'
                               ' the corrupt file is discarded')
            root_xml = etree.Element("builds")
    else:
        root_xml = etree.Element("builds")

    # add build data to xml
    root_xml.append(build.to_xml())

    # write xml to file
    with open(RESULT_FILE, 'wb') as xmlfile:
        xmlfile.write(etree.tostring(
            root_xml, xml_declaration=True,
            encoding='utf-8', pretty_print=True))


if __name__ == "__main__":
    # check if Buildtime trend is initialised
    if BUILD_TREND_INIT is not "1":
        logger.error(
            "Buildtime-trend is not initialised, first run 'source init.sh'."
        )
    # only run analysis if timestampfile is present
    elif check_file(TIMESTAMP_FILE):
        analyse(sys.argv, time.time())
