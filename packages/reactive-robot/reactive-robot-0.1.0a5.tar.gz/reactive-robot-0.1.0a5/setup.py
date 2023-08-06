# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reactive_robot',
 'reactive_robot.config',
 'reactive_robot.connectors',
 'reactive_robot.parsers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'importlib-metadata>=4.8.2,<5.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'minio>=7.1.1,<8.0.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pika>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['reactive-robot = reactive_robot.cli:cli']}

setup_kwargs = {
    'name': 'reactive-robot',
    'version': '0.1.0a5',
    'description': 'Fastest way to turn your robot workflows into event driven service.',
    'long_description': '# Reactive Robot (⚡ 🤖)\n\n[![cli-build](https://github.com/yusufcanb/reactive-robot/actions/workflows/python-tests.yml/badge.svg?branch=master)](https://github.com/yusufcanb/reactive-robot/actions/workflows/python-tests.yml)\n![pypi-badge](https://img.shields.io/pypi/v/reactive-robot)\n![stable](https://img.shields.io/static/v1?label=status&message=alpha-phase&color=yellow)\n\n\n## Mission\n\nThis project aims to turn Robot Framework projects into event-driven services using popular message brokers like RabbitMQ, Kafka or MQTT.\n\n## Installation\n\nYou can install reactive-robot into projects using pip;\n\n```\npip install reactive-robot\n```\n\n## Usage\n\nCreate a definition file called `reactive-robot.yml` then paste following configuration;\n\n```yaml\n\nservice_name: Example Robot Service\nservice_version: 1.0.0\n\nconnector:\n  driver: reactive_robot.connectors.mqtt.MQTTConnector\n  connection_url: mqtt://localhost:1883\n\nbindings:\n  - name: Example Task\n    topic: robot-queue\n    robot:\n      file: your-robots/examples.robot\n      args: null\n```\n\nYou\'re all set!\nNow all you have to do is start the service;\n\n```\npython -m reactive_robot serve\n```\n\nYou should see the following output;\n\n```\n$ python -m reactive_robot serve\n2021-11-27 18:22:58,517 - [INFO] - reactive_robot.serve::serve::40 - Using Robot Framework v4.1.2 (Python 3.10.0 on darwin)\n2021-11-27 18:22:58,518 - [INFO] - reactive_robot.serve::serve::47 - Event loop started. Waiting for events.\n```\n\nFinally publish a message to see your robots are running.\n\n```\npython tests/mqtt/publish.py localhost 1883\n```\n## Examples\n\nIn this section you can find example implementations with different message brokers;\nYou need **`docker`** and **`docker-compose`** in order to execute example projects.\n\n### Robot Service with Kafka Broker\n\nNavigate to the `examples/kafka`\n```\ncd examples/kafka\n```\n\nThen start containers with below; \n\n```\ndocker-compose up\n```\n\nFinally, trigger an event in basic topic to see your robots are running;\n\n```\ndocker-compose exec robot-service python /opt/service/publish.py basic \n```\n\n\n### Robot Service with MQTT Broker\n\nNavigate to the `examples/mqtt`\n```\ncd examples/mqtt\n```\n\nThen start containers with below; \n\n```\ndocker-compose up\n```\n\nFinally, trigger an event to see your robots are running;\n\n```\ndocker-compose exec mqtt-broker /opt/hivemq-4.7.2/tools/mqtt-cli/bin/mqtt pub --topic basic --message TEST_VAR:321\n```\n\n## Recipes\n\nIn the [examples/](examples) directory you can find example projects which implements all recipes below;\n\n### Dockerize your service\n\nHere you can find an example Dockerfile to convert your Robot Framework projects into dockerized event-driven service \n\n```dockerfile\nFROM robotframework/rfdocker\n\nWORKDIR /opt/service\n\nCOPY . /opt/service\nRUN pip install -r requirements.txt  # Your project dependencies.\n\n# reactive-robot setup\nCOPY reactive-robot.yml .\nRUN pip install reactive-robot\n\nCMD ["python", "-m", "reactive-robot", "serve"]\n```\n\nThen, we can build the image with following;\n\n```\ndocker build -t robot-service:1.0.0 .\n```\n\nFinally, run your service;\n\n```\ndocker run -it robot-service:1.0.0\n```\n\n\n## License\n\nDistributed under the Apache License 2.\nSee `LICENSE` for more information.\n\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create.\nAny contributions are **appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/some-feature`)\n3. Commit your Changes (`git commit -m \'some feature added\'`)\n4. Push to the Branch (`git push origin feature/some-feature`)\n5. Open a Pull Request\n',
    'author': 'Yusuf Can Bayrak',
    'author_email': 'yusufcanbayrak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yusufcanb/reactive-robot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
