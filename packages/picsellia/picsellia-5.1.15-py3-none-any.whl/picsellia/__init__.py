__version__ = "5.1.15"

import sys
import os
from setuptools import find_packages
import picsellia
from picsellia.client import Client  # Not used here but allows to : from picsellia import Client directly
import logging
import logging.config
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

for p in find_packages(where=picsellia.__path__[0]):
    sys.path.append(os.path.join(picsellia.__path__[0], p.replace('.', '/')))

sys.path.append(picsellia.__path__[0])

warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)

logger = logging.getLogger('picsellia')

logger.addHandler(logging.NullHandler())

try:
    custom_logging = os.environ["PICSELLIA_SDK_CUSTOM_LOGGING"]
except KeyError:
    custom_logging = False


if not custom_logging:
    try:
        logging.config.fileConfig('{}/conf/default_logging.conf'.format(picsellia.__path__[0]))
    except Exception as e:
        print('Error while loading conf file for logging. No logging done.')
