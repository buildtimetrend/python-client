#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
'''
Generates a trend (graph) from the buildtimes in buildtimes.xml

Usage : generate_trend.py -h --mode=native,keen

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
'''

import os
import sys
from buildtimetrend.tools import get_logger
from buildtimetrend.settings import Settings
from buildtimetrend.travis import load_travis_env_vars


def generate_trend(argv):
    '''
    Generate trends from analised buildtime data
    '''
    settings = Settings()

    # load settings from config file, env_var and cli parameters
    if settings.load_settings(argv) is None:
        return

    # load Travis CI environment variables
    load_travis_env_vars()

    # run trend_keen() always,
    # if $KEEN_PROJECT_ID variable is set (checked later), it will be executed
    if settings.get_setting("mode_native") is True:
        trend_native()
    if settings.get_setting("mode_keen") is True:
        trend_keen()


def trend_native():
    '''
    Generate native trend with matplotlib : chart in PNG format
    '''
    from buildtimetrend.trend import Trend
    # use parameter for timestamps file and check if file exists
    result_file = os.getenv('BUILD_TREND_OUTPUTFILE',
                            'dashboard/buildtimes.xml')
    chart_file = os.getenv('BUILD_TREND_TRENDFILE', 'dashboard/trend.png')

    trend = Trend()
    if trend.gather_data(result_file):
        logger = get_logger()
        # log number of builds and list of buildnames
        logger.debug('Builds (%d) : %s', len(trend.builds), trend.builds)
        logger.debug('Stages (%d) : %s', len(trend.stages), trend.stages)
        trend.generate(chart_file)


def trend_keen():
    '''
    Setup trends using Keen.io API
    '''
    from buildtimetrend.keenio import generate_dashboard_config_file

    generate_dashboard_config_file(Settings().get_project_name())

if __name__ == "__main__":
    generate_trend(sys.argv)
