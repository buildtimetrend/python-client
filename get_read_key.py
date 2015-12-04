#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
"""
Generate a read key for Keen.io API.

Usage : get_read_key.py [project_name]

When argument project_name is used, the read key will be
generated to access this project.
If no argument is given, the default project name will be used.

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
from __future__ import print_function

from buildtimetrend.keenio import keen_io_generate_read_key
from buildtimetrend.settings import Settings
import sys


def get_read_key(argv):
    """Generate a read key for the project and print that key."""
    settings = Settings()

    # load settings from config file, env_var and cli parameters
    args = settings.load_settings(argv)

    # exit script if processing cli parameters failed (result = None)
    if args is None:
        return

    # get project name from argument
    if len(args) > 0:
        settings.set_project_name(args[0])

    # generate a read key
    print(keen_io_generate_read_key(settings.get_project_name()))

if __name__ == "__main__":
    get_read_key(sys.argv)
