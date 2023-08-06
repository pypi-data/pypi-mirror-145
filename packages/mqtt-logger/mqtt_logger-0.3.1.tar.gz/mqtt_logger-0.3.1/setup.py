# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mqtt_logger']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'rich>=12.0.0,<13.0.0']

setup_kwargs = {
    'name': 'mqtt-logger',
    'version': '0.3.1',
    'description': 'Python based MQTT to SQLite3 logger',
    'long_description': '# MQTT to SQLite Logger\n\n[![PyPI version](https://badge.fury.io/py/mqtt-logger.svg)](https://badge.fury.io/py/mqtt-logger)\n[![Python package](https://github.com/Blake-Haydon/mqtt-logger/actions/workflows/python-package.yml/badge.svg)](https://github.com/Blake-Haydon/mqtt-logger/actions/workflows/python-package.yml)\n[![Upload Python Package](https://github.com/Blake-Haydon/mqtt-logger/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Blake-Haydon/mqtt-logger/actions/workflows/python-publish.yml)\n\n## Table of Contents\n- [MQTT to SQLite Logger](#mqtt-to-sqlite-logger)\n  - [Table of Contents](#table-of-contents)\n  - [Description](#description)\n    - [`LOG` Table](#log-table)\n    - [`RUN` Table](#run-table)\n  - [Installation](#installation)\n  - [Example Usage](#example-usage)\n    - [Recording MQTT Messages](#recording-mqtt-messages)\n    - [Playback Recorded MQTT Messages](#playback-recorded-mqtt-messages)\n  - [Unit Tests](#unit-tests)\n\n## Description\n\n`mqtt-logger` allows for asynchronous data logging of MQTT messages to a SQLite database. The SQLite database has two \ntables called `LOG` and `RUN`. The `LOG` table contains the messages that are being logged. The `RUN` table contains \nthe information about the current run of the program.\n\n### `LOG` Table\n\n| ROW NAME  | DESCRIPTION                                            |\n| --------- | ------------------------------------------------------ |\n| ID        | Unique number assigned to each message (ascending int) |\n| RUN_ID    | ID of the current run (ascending int)                  |\n| UNIX_TIME | Time when the message was received                     |\n| TOPIC     | MQTT topic                                             |\n| MESSAGE   | MQTT message received                                  |\n\n### `RUN` Table\n\n| ROW NAME        | DESCRIPTION                                   |\n| --------------- | --------------------------------------------- |\n| ID              | Unique number assigned to run (ascending int) |\n| START_UNIX_TIME | Time when logger was started                  |\n| END_UNIX_TIME   | Time when logger was stopped                  |\n\n\n--- \n\n\n## Installation\n\nIf you are using `mqtt-logger` as a python package, you can install it using pip.\n\n```bash\n# To use as a package\npip install mqtt-logger\n```\n\nIf you are looking to develop `mqtt-logger`, clone and run the following commands (poetry must be installed). \n\n```bash\n# For development work\ngit clone git@github.com:Blake-Haydon/mqtt-logger.git\ngit config --local core.hooksPath .githooks/\npoetry install\n```\n\n---\n\n\n## Example Usage\n\n### Recording MQTT Messages\n\nThis example records messages to the `test/#` topic using a public MQTT broker. It will record for 10 seconds. If you \nare using a private broker, you may need to set the `username` and `password` parameters.\n\n```bash\n# Run example in terminal\npoetry run python examples/10s_recording.py\n```\n\nExample recorder taken from [examples/10s_recording.py](examples/10s_recording.py)\n```python\nimport mqtt_logger\nimport os\nimport time\n\n# Initalise mqtt recorder object\nrec = mqtt_logger.Recorder(\n    sqlite_database_path=os.path.join(os.path.dirname(__file__), "MQTT_log.db"),\n    topics=["test/#"],\n    broker_address="broker.hivemq.com",\n    verbose=True,\n)\n\n# Start the logger, wait 10 seconds and stop the logger\nrec.start()\ntime.sleep(10)\nrec.stop()\n```\n\n### Playback Recorded MQTT Messages\n\nThis example plays back previously recorded MQTT messages from `mqtt_logger.Recorder`. If you are using a private \nbroker, you may need to set the `username` and `password` parameters.\n\n```bash\n# Run example in terminal after running the recorder example\npoetry run python examples/10s_playback.py\n```\n\nExample recorder taken from [examples/10s_playback.py](examples/10s_playback.py)\n```python\nimport mqtt_logger\nimport os\n\n# Initalise playback object\nplayback = mqtt_logger.Playback(\n    sqlite_database_path=os.path.join(os.path.dirname(__file__), "MQTT_log.db"),\n    broker_address="broker.hivemq.com",\n    verbose=True,\n)\n\n# Start playback at 2x speed (twice as fast)\nplayback.play(speed=2)\n```\n\n\n---\n\n\n## Unit Tests\n\n```bash\n# Run tests in poetry virtual environment\npoetry run pytest\n```',
    'author': 'Blake Haydon',
    'author_email': 'blake.a.haydon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Blake-Haydon/mqtt-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
