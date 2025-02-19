from checkpy import *
from pathlib import Path

from shared import has_main, contains_rabbit, contains_experiment, contains_fox
from shared import rabbit_attributes, rabbit_values, fox_attributes, fox_values
from experiment_methods import experiment_contains_add_rabbits, experiment_contains_add_foxes
from experiment_methods import experiment_contains_rabbits_and_foxes

only("phase4.py")
