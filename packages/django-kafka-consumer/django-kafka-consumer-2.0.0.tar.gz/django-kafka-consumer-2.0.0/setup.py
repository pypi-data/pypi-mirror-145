# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_consumer',
 'kafka_consumer.management',
 'kafka_consumer.management.commands',
 'kafka_consumer.messages',
 'kafka_consumer.migrations',
 'kafka_consumer.subscribers',
 'kafka_consumer.tests']

package_data = \
{'': ['*'],
 'kafka_consumer': ['locale/en/LC_MESSAGES/*', 'locale/pl/LC_MESSAGES/*']}

install_requires = \
['Django>=2.0,<3.0', 'kafka-python==2.0.2', 'pytz>=2021.3,<2022.0']

setup_kwargs = {
    'name': 'django-kafka-consumer',
    'version': '2.0.0',
    'description': '',
    'long_description': "Django Kafka Consumer\n=====================\n\nPurpose\n-------\n\n**Django Kafka Consumer** is an utility for consume events from\n[Kafka](https://kafka.apache.org/)\n\nQuick start\n-----------\n\n1.  Add `kafka_consumer` to your `INSTALLED_APPS` setting like this:\n\n        INSTALLED_APPS = [\n            # ...\n            'kafka_consumer',\n        ]\n\n2.  Run `python manage.py migrate` to create the `kafka_consumer`\n    models.\n3.  Add custom subscribers as classes derived from\n    `kafka_consumer.subscribers.base.BaseSubscriber`\n4.  Prepare settings:\n\n        KAFKA_HOSTS = ['kafka-host.com:9092']\n\n        KAFKA_CONSUMER_TOPICS = {\n            'topic_key': {\n                'topic': 'topic name',  # no spaces allowed!\n                'group': 'topic group',\n                'client': 'client ID',\n                'subscribers': (\n                    'path.to.subscriber.Class',\n                ),\n                'message_processor': 'processor key',  # lookup in KAFKA_CONSUMERS_MESSAGE_PROCESSORS\n                'wait': 0,  # optional, indicates how many seconds Kafka will wait to fillup buffer, None or ommited means wait forever\n                'max_number_of_messages_in_batch': 200,\n                'consumer_options': {  # Overrides options used to create KafkaConsumer\n                    'auto_offset_reset': 'latest',\n                }\n            },\n        }\n        KAFKA_CONSUMERS_MESSAGE_PROCESSORS = {\n          'processor key': {\n            'class': 'path.to.messageprocessor.Class',\n            # Processors init arguments, e.g.\n            'rsa_private_key_path': 'path/to/private/key'\n          },\n        }\n\n        KAFKA_CONSUMER_SSL_SETTINGS = {\n            'security_protocol': 'SSL',\n            'ssl_cafile': '/path/to/file/ca.crt',\n            'ssl_certfile': '/path/to/file/signed.request.crt',\n            'ssl_keyfile': '/path/to/some/keyfile.key',\n        }\n\n5.  To continuously consume events from kafka run:\n\n        python manage.py consume --supervised --topic topic_key\n\nLicense\n-------\n\nThe Django Kafka Consumer package is licensed under the [FreeBSD\nLicense](https://opensource.org/licenses/BSD-2-Clause).\n",
    'author': 'IIIT',
    'author_email': 'github@iiit.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/innovationinit/django-kafka-consumer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
