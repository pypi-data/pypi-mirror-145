import logging

import rasa_nlu.version

from rasa_nlu.train import train                  # noqa F401
from rasa_nlu.test import run_evaluation as test  # noqa F401
from rasa_nlu.test import cross_validate          # noqa F401
from rasa_nlu.training_data import load_data      # noqa F401

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = rasa_nlu.version.__version__
