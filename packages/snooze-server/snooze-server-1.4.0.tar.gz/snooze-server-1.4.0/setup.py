# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snooze',
 'snooze.alerta',
 'snooze.api',
 'snooze.cli',
 'snooze.db',
 'snooze.db.file',
 'snooze.db.mongo',
 'snooze.plugins',
 'snooze.plugins.core',
 'snooze.plugins.core.action',
 'snooze.plugins.core.action.falcon',
 'snooze.plugins.core.aggregaterule',
 'snooze.plugins.core.audit',
 'snooze.plugins.core.basic',
 'snooze.plugins.core.basic.falcon',
 'snooze.plugins.core.comment',
 'snooze.plugins.core.comment.falcon',
 'snooze.plugins.core.grafana',
 'snooze.plugins.core.grafana.falcon',
 'snooze.plugins.core.influxdb2',
 'snooze.plugins.core.influxdb2.falcon',
 'snooze.plugins.core.kapacitor',
 'snooze.plugins.core.kapacitor.falcon',
 'snooze.plugins.core.kv',
 'snooze.plugins.core.mail',
 'snooze.plugins.core.notification',
 'snooze.plugins.core.profile',
 'snooze.plugins.core.profile.falcon',
 'snooze.plugins.core.prometheus',
 'snooze.plugins.core.prometheus.falcon',
 'snooze.plugins.core.rule',
 'snooze.plugins.core.script',
 'snooze.plugins.core.settings',
 'snooze.plugins.core.settings.falcon',
 'snooze.plugins.core.snooze',
 'snooze.plugins.core.snooze.falcon',
 'snooze.plugins.core.stats',
 'snooze.plugins.core.stats.falcon',
 'snooze.plugins.core.user',
 'snooze.plugins.core.user.falcon',
 'snooze.plugins.core.webhook',
 'snooze.plugins.core.widget',
 'snooze.plugins.core.widget.falcon',
 'snooze.utils']

package_data = \
{'': ['*'],
 'snooze': ['defaults/*', 'defaults/web/*'],
 'snooze.plugins.core': ['environment/*', 'record/*', 'role/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'MarkupSafe>=2.0.1,<3.0.0',
 'PyJWT==1.7.1',
 'PyYAML==5.4.1',
 'click>=8.0.1,<9.0.0',
 'falcon-auth>=1.1.0,<2.0.0',
 'falcon>=3.0.1,<4.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'kombu==5.1.0',
 'ldap3>=2.9.1,<3.0.0',
 'netifaces>=0.11.0,<0.12.0',
 'pathlib>=1.0.1,<2.0.0',
 'prometheus-client>=0.13.1,<0.14.0',
 'pymongo==3.12.1',
 'pyparsing>=2.4.7,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-unixsocket>=0.2.0,<0.3.0',
 'requests>=2.26.0,<3.0.0',
 'tinydb==4.5.2',
 'typing-extensions>=3.10.0.2,<4.0.0.0',
 'waitress>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['snooze = snooze.cli.__main__:snooze',
                     'snooze-server = snooze.__main__:main']}

setup_kwargs = {
    'name': 'snooze-server',
    'version': '1.4.0',
    'description': 'Monitoring tool for logs aggregation and alerting',
    'long_description': '![Snoozeweb Logo](https://github.com/snoozeweb/snooze/raw/master/web/public/img/logo.png)\n\n# About\n\nSnooze is a powerful monitoring tool used for log aggregation and alerting. It comes with the following features:\n* Backend + Web interface\n* Local / LDAP / JWT token based authentication\n* Built-in clustering for scalability\n* Large number of sources as inputs\n* Log aggregation\n* Log manipulation\n* Log archiving\n* Alerting policies\n* Various alerting methods\n* Auto housekeeping\n* Auto backups\n* Metrics\n\nTry it now on: https://try.snoozeweb.net\n\n![Alerts](https://github.com/snoozeweb/snooze/raw/master/doc/images/web_alerts.png)\n\n# Installation\n\nInstallation on CentOS/RHEL\n\n```bash\n$ wget https://rpm.snoozeweb.net -O snooze-server-latest.rpm\n$ sudo yum localinstall snooze-server-latest.rpm\n$ sudo systemctl start snooze-server\n```\n\nInstallation on Ubuntu/Debian\n\n```bash\n$ wget https://deb.snoozeweb.net -O snooze-server-latest.deb\n$ sudo apt install snooze-server-latest.deb\n$ sudo systemctl start snooze-server\n```\n\nWeb interface URL:\n\n```\nhttp://localhost:5200\n```\n\nif `create_root_user` in `/etc/snooze/core.yaml` has not been set to **false**, login credentials are `root:root`\n\nOtherwise, it is always possible to generate a root token that can be used for **JWT Token** authentication method if [Snooze Client](https://github.com/snoozeweb/snooze_client) is installed:\n\n```bash\n$ snooze root-token\n# Run with root or snooze user\nRoot token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im...\n```\n\n## Recommendations\n\nBy default, Snooze is using a single file to store its database and therefore can run out of the box without any additional configuration or dependency. While this implementation is convenient for testing purpose, it is heavily recommended to switch the database configuration to MongoDB.\n\n## Docker\n\n### Simple\n\n```\n$ docker run --name snoozeweb -d -p <port>:5200 snoozeweb/snooze\n```\n\nThen the Web interface should be available at this URL:\n\n```\nhttp://<docker>:<port>\n```\n\nSnoozeweb docker image can be run without any backend database (will default to a file based DB) but if one is needed:\n\n```\n$ docker run --name snooze-db -d mongo\n```\n\nThen\n\n```\n$ export DATABASE_URL=mongodb://db:27017/snooze\n$ docker run --name snoozeweb -e DATABASE_URL=$DATABASE_URL --link snooze-db:db \\\n-d -p <port>:5200 snoozeweb/snooze\n```\n\n### Advanced\n\nRequirements:\n* Docker (version >= 17.0.0)\n* Docker-Compose\n\nThe `docker-compose.yaml` recipe will create the following (Replace `HOST1`, `HOST2` and `HOST3` with swarm workers):\n* 3 nodes MongoDB Replica Set\n* 3 Snooze servers in cluster mode\n* 1 Nginx load balancer (manager node)\n\nAfter initializing [docker swarm](https://docs.docker.com/engine/swarm/) and adding workers, run the command:\n```\ndocker stack deploy -c docker-compose.yaml snoozeweb\n# Wait until MongoDB containers are up\nreplicate="rs.initiate(); sleep(1000); cfg = rs.conf(); cfg.members[0].host = \\"mongo1:27017\\"; rs.reconfig(cfg); rs.add({ host: \\"mongo2:27017\\", priority: 0.5 }); rs.add({ host: \\"mongo3:27017\\", priority: 0.5 }); rs.status();"\ndocker exec -it $(docker ps -qf label=com.docker.swarm.service.name=snoozeweb_mongo1) /bin/bash -c "echo \'${replicate}\' | mongo"\n```\n\nThe web interface should be available on the manager node on port 80\n\n# Configuration\n\nThe only configuration file not managed in the web interface is `/etc/snooze/core.yaml` and requires restarting Snooze if changed.\n\n`/etc/snooze/core.yaml`\n* `listen_addr` (`\'0.0.0.0\'`): IPv4 address on which Snooze process is listening to\n* `port` (`5200`): Port on which Snooze process is listening to\n* `debug` (`false`): Activate debug log output\n* `bootstrap_db` (`true`): Populate the database with an initial configuration\n* `create_root_user` (`true`): Create a *root* user with a default password *root*\n* `no_login` (`false`): Disable Authentication (everyone has admin priviledges)\n* `audit_excluded_paths` (`[/api/patlite\', /metrics, /web]`): List of HTTP paths excluded from audit logs\n* `ssl`\n    * `enabled` (`false`): Enable TLS termination for both the API and the web interface\n    * `certfile` (`\'\'`): Path to the SSL certificate\n    * `keyfile` (`\'\'`): Path to the private key\n* `web`\n    * `enabled` (`true`): Enable the web interface\n    * `path` (`/opt/snooze/web`): Path to the web interface dist files\n* `clustering`\n    *  `enabled` (`false`): Enable clustering mode\n    * `members`: List of snooze servers in the cluster {host, port}\n        - `host` (`localhost`): Hostname or IPv4 address of the first member\n\n          `port` (`5200`): Port on which the first member is listening to\n        - ...\n* `database`\n    * `type` (`file`): Backend database to use (file or mongo)\n* `backup`\n    * `enabled` (`true`): Enable backups\n    * `path` (`WORKDIR/backups`): Path to store database backups\n    * `exclude` ([record, stats, comment, secrets]): Collections to exclude from backups\n\nExample for MongoDB backend with database replication enabled:\n```yaml\ndatabase:\n    type: mongo\n    host:\n        - hostA\n        - hostB\n        - hostC\n    port: 27017\n    username: snooze\n    password: 7dg9khqg1w6\n    authSource: snooze\n    replicaSet: rs0\n```\n\n# Documentation\n\n[Documentation page](doc/)\n\n# License\n\n```\nSnooze - Log aggregation and alerting\n\nCopyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>\nCopyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>\nCopyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as\npublished by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n```\n',
    'author': 'Florian Dematraz',
    'author_email': 'florian.dematraz@snoozeweb.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
