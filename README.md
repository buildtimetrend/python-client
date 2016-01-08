Buildtime Trend Python Client
=============================

Visualise what's trending in your build process

[![Buildtime trend](http://img.shields.io/badge/release-v0.3-blue.svg)](https://github.com/buildtimetrend/python-client/releases/latest)
[![Buildtime trend](http://img.shields.io/badge/dev-v0.4.dev-blue.svg)](https://github.com/buildtimetrend/python-client/zipball/master)
[![Build Status](https://travis-ci.org/buildtimetrend/python-client.svg)](https://travis-ci.org/buildtimetrend/python-client)
[![Code Health](https://landscape.io/github/buildtimetrend/python-client/master/landscape.png)](https://landscape.io/github/buildtimetrend/python-client/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/buildtimetrend/python-client/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/buildtimetrend/python-client/?branch=master)
[![Codacy Badge](https://www.codacy.com/project/badge/b392eb72c5044ea6a4ce40e0eaa6c518)](https://www.codacy.com/public/ruleant/python-client)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/e44ba62bf09c4649b9103cc4225ae345/badge.svg)](https://www.quantifiedcode.com/app/project/e44ba62bf09c4649b9103cc4225ae345)

[![Buildtime trend](https://buildtimetrend.herokuapp.com/badge/buildtimetrend/python-client/latest)](http://buildtimetrend.github.io/python-client/buildtime-trend/)
[![Total builds](https://buildtimetrend.herokuapp.com/badge/buildtimetrend/python-client/builds/month)](http://buildtimetrend.github.io/python-client/buildtime-trend/)
[![Percentage passed build jobs](https://buildtimetrend.herokuapp.com/badge/buildtimetrend/python-client/passed/month)](http://buildtimetrend.github.io/python-client/buildtime-trend/)

[![Stack Share](http://img.shields.io/badge/tech-stack-0690fa.svg)](http://stackshare.io/ruleant/buildtime-trend)


Features
--------

Visualise trends of build processes on Continuous Integration platforms by gathering and analysing build and timing data: 

- Capture timing data from each stage in a build process
- Store, analyse and create trends of the build process data
  - keen mode : send timing data to Keen.io and use the Keen.io API for analysis and visualisation
  - native mode : store data in xml format and use matplotlib to generate a chart (limited)
- Available charts and metrics :
  - number of builds, successful and failed
  - average build duration
  - duration of individual build stages
  - builds per branch
  - build duration per time of day/day of week

How to get it?
--------------

The [latest version](https://github.com/buildtimetrend/python-client/releases/latest) is available for download as zip and tarball on GitHub. Unzip and copy to the desired directory.

If you prefer to use git, several options are available :

- development version : `git clone --recursive https://github.com/buildtimetrend/python-client.git`
- latest release : `git clone --recursive https://github.com/buildtimetrend/python-client.git --branch release`
- a specific release : `git clone --recursive https://github.com/buildtimetrend/python-client.git --branch v0.3`

Dependencies
------------

- `buildtimetrend` : [Buildtime Trend library](https://github.com/buildtimetrend/python-lib)

### Dependency installation

- using pip :

`pip install -r requirements.txt`

- if you want to store data or generate charts in `native` mode :

`pip install -r requirements-native.txt`


Usage
-----

First the timestamp recording needs to be initialised :

`source /path/to/init.sh`

This script will detect the location of the build-trend script folder,
adds it to the PATH and cleans logfiles of previous runs.
Executing the init script with `source` is required to export environment variables to the current shell session.

Because the script dir is added to PATH, no path needs to be added
when logging a timestamp :

`timestamp.sh event_name`

This will log the current timestamp to a file and display it on STDOUT.
Repeat this step as much as needed.

When all build stages are finished, run

`analyse.py`

which will analyse the logfile with timestamps and print out the results.
The `analyse.py` script will calculate the duration between the timestamps and add those to a file with the analysed data of previous builds.
When the analysis script encounters the `end` timestamp, it will stop analysing the timestamp file and return the duration of the build stages. Possible event names ending the analysis are : `end`, `done`, `finished` or `completed`.

Optionally `timestamp.sh end` can be run before `analyse.py`, but `analyse.py` adds the end timestamp automatically. The `end` timestamp can be useful if `analyse.py` is not immediately run after the monitored build process finishes.

When Keen.io is enabled, the data will be sent to your Keen.io project for analysis.

When run on Travis CI, it will automatically add build/job related info.
Parameter `-m native` will store data in xml format. It is recommended to use Keen.io to store data, see below for details.

To generate a graph from previous builds, run

`generate_trend.py`

It will take the file with analysed data generated by the analyse script and turn it into a trend graph and saves this graph.
Parameter `--mode=native` will create a trend using Python `matplotlib`. It is recommended to use Keen.io to generate graphs, see below for details.
If Keen.io is enabled, `generate_trend.py` can be run without parameters.

Use the `sync-buildtime-trend-with-gh-pages.sh` script when you run it as part of a Travis CI build. See below for details.

Store build time data in xml (native mode)
------------------------------------------

(It is recommended to use Keen.io to store data and generate trends, see below)

To store data in xml, native mode needs to be enabled. The xml file is stored in `dashboard/buildtimes.xml` by default.

To analyse timestamps and store the analysed data :

`analyse.py --mode=native`

See wiki for [data schema of the xml file](https://github.com/buildtimetrend/python-lib/wiki/Structure#data-file-in-native-mode).

To generate a chart from the data stored in the xml file :

`generate_trend.py --mode=native`

This will save a trend image in `dashboard/trend.png`

Store build time data in Keen.io
--------------------------------

Next to storing your build time data in xml, it can be sent to Keen.io for storage, analysis and generating graphs.

Follow these steps to enable using Keen.io :

1. [Create a Keen.io account](https://keen.io/signup), if you haven't already done so.
2. [Create a project](https://keen.io/add-project) in your Keen.io account.
3. Look up the `project ID`, `Write Key` and `Master key` and assign them to environment variables :
- `export KEEN_PROJECT_ID=<Project ID>`
- `export KEEN_WRITE_KEY=<Write Key>` (when running on Travis CI, use `Master Key`, see below)
- `export KEEN_MASTER_KEY=<Master Key>`

If these environment variables are set, the scripts will detect this and use Keen.io to store data, do analysis and generate graphs.

See wiki for [data schema of data sent to Keen.io](https://github.com/buildtimetrend/python-lib/wiki/Structure#data-structures-in-keen-mode).

Visualise the trends (powered by Keen.io)
-----------------------------------------

Multiple trends are available when data was stored in `keen` mode :

Folder `dashboard` contains all files necessary to display the generated trends.
- Copy folder `dashboard` to the desired location
- Rename (or copy) `config_sample.js` to `config.js`
- Edit `config.js` :
  - add `keen_project_id` (see Keen.io section above)
  - add `keen_read_key` (see Keen.io section above, or generate a scoped read key with `get_read_key.py project_name` (`project_name` should be the same as the project_name used to store the data, this is usually the git-repo name, fe. `buildtimetrend/python-client`)
  - add `project_name` : repo name is a good default, but it can be custom project name as well, this is only used as title on the webpage. It is not used to collect data.
- Browse to `dashboard/index.html`, this should display the trends

If you are building a Github repo on Travis CI, and you have `gh-pages` branch, you can use the script mentioned below to automatically add the right files and create the config file.


Integrate with Travis CI
------------------------

You can integrate Buildtime Trend with your build process on Travis CI :
install and initialise the buildtime trend scripts, add timestamp labels, generate the trend
and synchronise it with your gh-pages branch.

All you need is a github repo, a Travis CI account for your repo and a gh-pages branch to publish the results.

You also need to create an encrypted `GH_TOKEN` to get write access to your repo (publish results on gh-pages branch) :
- [create](https://github.com/settings/applications) the access token for your github repo, `repo` scope is sufficient
- encrypt the environment variable using the [Travis CI command line tool](http://docs.travis-ci.com/user/encryption-keys/) :
`travis encrypt GH_TOKEN=github_access_token`
- add the encrypted token to your `.travis.yml` file (see below)

To enable integration with Keen.io, `KEEN_PROJECT_ID` and `KEEN_WRITE_KEY` should be set (see above):

1. Follow the steps above to create a Keen.io account and project and look up the `Project ID` and `Master Key`
2. Assign the `Project ID` and `Master Key` to the corresponding environment variables and encrypt them using the [Travis CI command line tool](http://docs.travis-ci.com/user/encryption-keys/) and add it them to `.travis.yml` (see below) :
- `travis encrypt KEEN_PROJECT_ID=<Project ID>`
- `travis encrypt KEEN_WRITE_KEY=<Master Key>`
**Remark :** Use the `Master Key` instead of the `Write Key` of your Keen.io project, because the `Write Key` is too long to encrypt using the Travis CI encryption tool
- `travis encrypt KEEN_MASTER_KEY=<Master Key>`
The `Master Key` of your Keen.io project is used to generate a scoped read key

The generated trend graph and build-data will be put in folder `buildtime-trend` on your `gh-pages` branch.
The trend is available on http://{username}.github.io/{repo_name}/buildtime-trend/index.html

Example `.travis.yml` file :

    language: python
    env:
      global:
        - secure: # your secure GH_TOKEN goes here (required to share trend on gh-pages)
        - secure: # your secure KEEN_PROJECT_ID goes here (required to store data on Keen.io)
        - secure: # your secure KEEN_WRITE_KEY goes here (required to store data on Keen.io)
        - secure: # your secure KEEN_MASTER_KEY goes here (required to generate a scoped read key to generate graphs using the Keen.io API)
    before_install:
      # install and initialise build-trend scripts
      # uncomment one of two options below (stable or development)
      # download latest stable release
      - git clone --recursive --depth 1 --branch release https://github.com/buildtimetrend/python-client.git $HOME/buildtime-trend
      # use latest development version (clone git repo)
      # - if [[ -d $HOME/buildtime-trend/.git ]]; then cd $HOME/buildtime-trend; git pull; cd ..; else git clone --recursive https://github.com/buildtimetrend/python-client.git $HOME/buildtime-trend; fi
      # initialise buildtime-trend scripts
      - source $HOME/buildtime-trend/init.sh
    install:
      # generate timestamp with label 'install'
      - timestamp.sh install
      # install buildtime-trend dependencies
      - CFLAGS="-O0" pip install -r ${BUILD_TREND_HOME}/requirements.txt
      # install dependencies
    script:
      # generate timestamp with label 'tests'
      - timestamp.sh tests
      # run your tests
    after_script:
      # synchronise buildtime-trend result with gh-pages
      - sync-buildtime-trend-with-gh-pages.sh

Run `sync-buildtime-trend-with-gh-pages.sh` in `after_script` to report the gathered timestamps with the result of the build in `$TRAVIS_TEST_RESULT`, which comes available in `after_{success|failure}`. `after_script` is executed regardless of the build result, so after both `after_success` and `after_failure`.

To enable `native` mode, add `-m native` when calling `sync-buildtime-trend-with-gh-pages.sh`

Bugs and feature requests
-------------------------

Please report bugs and add feature requests in the Github [issue tracker](https://github.com/buildtimetrend/python-lib/issues).

Contribute
----------

If you want to contribute to make Buildtime Trend even better, check out the [contribution](https://github.com/buildtimetrend/python-lib/wiki/Contribute) page.
We are looking for testers, developers, designers, ... and what more. [Contact us](#contact) if you want to help out.

Donations
---------

You can support the project by making a [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=LG9M6QTBS9LKL). The donations will help pay for the hosting and support further development.

Credits
-------

For an overview of who contributed to create Buildtime trend, see [Credits](https://github.com/buildtimetrend/python-lib/wiki/Credits).

Contact
-------

Project website : http://buildtimetrend.github.io/

Mailinglist : [Buildtime Trend Community](https://groups.google.com/d/forum/buildtimetrend-dev)

Follow us on [Twitter](https://twitter.com/buildtime_trend), [Github](https://github.com/buildtimetrend/python-client) and [OpenHub](https://www.openhub.net/p/buildtime-trend).


License
-------

Copyright (C) 2014-2016 Dieter Adriaenssens <ruleant@users.sourceforge.net>

This software was originally released under GNU General Public License
version 3 or any later version, all commits contributed from
12th of November 2014 on, are contributed as GNU Affero General Public License.
Hence the project is considered to be GNU Affero General Public License
from 12th of November 2014 on.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
