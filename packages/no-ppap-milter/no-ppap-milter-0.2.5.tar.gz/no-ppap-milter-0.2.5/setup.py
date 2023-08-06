# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['no_ppap_milter']

package_data = \
{'': ['*']}

install_requires = \
['pymilter>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['no-ppap-milter = no_ppap_milter.cli_no_ppap_milter:main']}

setup_kwargs = {
    'name': 'no-ppap-milter',
    'version': '0.2.5',
    'description': 'This is a milter to prevent receiving emails which has encrypted zip attachments.',
    'long_description': '# no-ppap-milter\n\nThis Milter rejects the email which has encrypted zip file.\n\nIf the MTA receives such email, this will respond `550 5.7.1 We do not accpet encrypted zip.` on the DATA command to reject it.\n\n## Requirements\n\n### CentOS7\n\n```console\nyum install -y python3 gcc python3-devel sendmail-devel\n```\n\n### Ubuntu 20.04\n\n```console\napt-get install -y python3-pip libmilter-dev\n```\n\n## Install\n\n```cosole\npip install no-ppap-milter\n```\n\n## Run\n\nThis will listen on port 9201 by default.\n\n```\nno-ppap-milter\n```\n\nIf you want to use another port,\n\n```\nno-ppap-milter --socket-name inet:1234\n```\n\nwill listen on port 1234.\n\nIf you want to use UNIX domain socket, invoke like this.\n\n```\nno-ppap-milter --socket-name unix:/var/run/milter.sock\n```\n',
    'author': 'HIRANO Yoshitaka',
    'author_email': 'yo@hirano.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hirachan/no-ppap-milter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
