# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sydent',
 'sydent.config',
 'sydent.db',
 'sydent.hs_federation',
 'sydent.http',
 'sydent.http.servlets',
 'sydent.replication',
 'sydent.sms',
 'sydent.terms',
 'sydent.threepid',
 'sydent.users',
 'sydent.util',
 'sydent.validators']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1.0',
 'jinja2>=3.0.0',
 'matrix-common>=1.1.0,<2.0.0',
 'netaddr>=0.7.0',
 'phonenumbers>=8.12.32',
 'pyOpenSSL>=16.0.0',
 'pynacl>=1.2.1',
 'pyyaml>=3.11',
 'service-identity>=1.0.0',
 'signedjson==1.1.1',
 'sortedcontainers>=2.1.0',
 'twisted>=18.4.0',
 'typing-extensions>=3.7.4',
 'unpaddedbase64>=1.1.0',
 'zope.interface>=4.6.0']

extras_require = \
{'prometheus': ['prometheus-client>=0.4.0'], 'sentry': ['sentry-sdk>=0.7.2']}

entry_points = \
{'console_scripts': ['sydent = sydent.sydent:main']}

setup_kwargs = {
    'name': 'matrix-sydent',
    'version': '2.5.2',
    'description': 'Reference Matrix Identity Verification and Lookup Server',
    'long_description': 'Installation\n============\n\nInstalling the system dependencies\n----------------------------------\n\nTo install Sydent\'s dependencies on a Debian-based system, run::\n\n    sudo apt-get install build-essential python3-dev libffi-dev \\\n                         sqlite3 libssl-dev python-virtualenv libxslt1-dev\n\nCreating the virtualenv\n-----------------------\n\nTo create the virtual environment in which Sydent will run::\n\n    virtualenv -p python3 ~/.sydent\n    source ~/.sydent/bin/activate\n    pip install --upgrade pip\n    pip install --upgrade setuptools\n\n\nInstalling the latest Sydent release from PyPI\n----------------------------------------------\n\nSydent and its dependencies can be installed using ``pip`` by running::\n\n    pip install matrix-sydent\n\nInstalling from source\n----------------------\n\nAlternatively, Sydent can be installed using ``pip`` from a local git checkout::\n\n    git clone https://github.com/matrix-org/sydent.git\n    cd sydent\n    pip install -e .\n\n\nRunning Sydent\n==============\n\nWith the virtualenv activated, you can run Sydent using::\n\n    python -m sydent.sydent\n\nThis will create a configuration file in ``sydent.conf`` with some defaults. If a setting is\ndefined in both the ``[DEFAULT]`` section and another section in the configuration file,\nthen the value in the other section is used.\n\nYou\'ll most likely want to change the server name (``server.name``) and specify an email server\n(look for the settings starting with ``email.``).\n\nBy default, Sydent will listen on ``0.0.0.0:8090``. This can be changed by changing the values for\nthe configuration settings ``clientapi.http.bind_address`` and ``clientapi.http.port``.\n\nSydent uses SQLite as its database backend. By default, it will create the database as ``sydent.db``\nin its working directory. The name can be overridden by modifying the ``db.file`` configuration option.\nSydent is known to be working with SQLite version 3.16.2 and later.\n\nSMS originators\n---------------\n\nDefaults for SMS originators will not be added to the generated config file, these should\nbe added to the ``[sms]`` section of that config file in the form::\n\n    originators.<country code> = <long|short|alpha>:<originator>\n\nWhere country code is the numeric country code, or ``default`` to specify the originator\nused for countries not listed. For example, to use a selection of long codes for the\nUS/Canada, a short code for the UK and an alphanumertic originator for everywhere else::\n\n    originators.1 = long:12125552368,long:12125552369\n    originators.44 = short:12345\n    originators.default = alpha:Matrix\n\nDocker\n======\n\nA Dockerfile is provided for sydent. To use it, run ``docker build -t sydent .`` in a sydent checkout.\nTo run it, use ``docker run --env=SYDENT_SERVER_NAME=my-sydent-server -p 8090:8090 sydent``.\n\nPersistent data\n---------------\n\nBy default, all data is stored in ``/data``. To persist this to disk, bind `/data` to a\nDocker volume.\n\n.. code-block:: shell\n\n   docker volume create sydent-data\n   docker run ... --mount type=volume,source=sydent-data,destination=/data sydent\n\nBut you can also bind a local directory to the container.\nHowever, you then have to pay attention to the file permissions.\n\n.. code-block:: shell\n\n   mkdir /path/to/sydent-data\n   chown 993:993 /path/to/sydent-data\n   docker run ... --mount type=bind,source=/path/to/sydent-data,destination=/data sydent\n\nEnvironment variables\n---------------------\n\n.. warning:: These variables are only taken into account at first start and are written to the configuration file.\n\n+--------------------+-----------------+-----------------------+\n| Variable Name      | Sydent default  | Dockerfile default    |\n+====================+=================+=======================+\n| SYDENT_SERVER_NAME | *empty*         | *empty*               |\n+--------------------+-----------------+-----------------------+\n| SYDENT_CONF        | ``sydent.conf`` | ``/data/sydent.conf`` |\n+--------------------+-----------------+-----------------------+\n| SYDENT_PID_FILE    | ``sydent.pid``  | ``/data/sydent.pid``  |\n+--------------------+-----------------+-----------------------+\n| SYDENT_DB_PATH     | ``sydent.db``   | ``/data/sydent.db``   |\n+--------------------+-----------------+-----------------------+\n\n\nInternal bind and unbind API\n============================\n\nIt is possible to enable an internal API which allows for binding and unbinding\nbetween identifiers and matrix IDs without any validation.\nThis is open to abuse, so is disabled by\ndefault, and when it is enabled, is available only on a separate socket which\nis bound to ``localhost`` by default.\n\nTo enable it, configure the port in the config file. For example::\n\n    [http]\n    internalapi.http.port = 8091\n\nTo change the address to which that API is bound, set the ``internalapi.http.bind_address`` configuration\nsetting in the ``[http]`` section, for example::\n\n    [http]\n    internalapi.http.port = 8091\n    internalapi.http.bind_address = 192.168.0.18\n\nAs already mentioned above, this is open to abuse, so make sure this address is not publicly accessible.\n\nTo use bind::\n\n    curl -XPOST \'http://localhost:8091/_matrix/identity/internal/bind\' -H "Content-Type: application/json" -d \'{"address": "matthew@arasphere.net", "medium": "email", "mxid": "@matthew:matrix.org"}\'\n\nThe response has the same format as\n`/_matrix/identity/api/v1/3pid/bind <https://matrix.org/docs/spec/identity_service/r0.3.0#deprecated-post-matrix-identity-api-v1-3pid-bind>`_.\n\nTo use unbind::\n\n    curl -XPOST \'http://localhost:8091/_matrix/identity/internal/unbind\' -H "Content-Type: application/json" -d \'{"address": "matthew@arasphere.net", "medium": "email", "mxid": "@matthew:matrix.org"}\'\n\nThe response has the same format as\n`/_matrix/identity/api/v1/3pid/unbind <https://matrix.org/docs/spec/identity_service/r0.3.0#deprecated-post-matrix-identity-api-v1-3pid-unbind>`_.\n\n\nReplication\n===========\n\nIt is possible to configure a mesh of Sydent instances which replicate identity bindings\nbetween each other. See `<docs/replication.md>`_.\n\nDiscussion\n==========\n\nMatrix room: `#sydent:matrix.org <https://matrix.to/#/#sydent:matrix.org>`_.\n\n',
    'author': 'Matrix.org Team and Contributors',
    'author_email': 'packages@matrix.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matrix-org/sydent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
