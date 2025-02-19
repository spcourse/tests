from checkpy import *
from pathlib import Path

from shared import has_main, contains_rabbit, contains_experiment, contains_fox, contains_creature
from shared import rabbit_attributes, rabbit_values, fox_attributes, fox_values
from inheritance import rabbit_is_creature, fox_is_creature
from inheritance import rabbit_attribbutes_set_in_init, fox_attribbutes_set_in_init
from inheritance import creature_attributes_correct, rabbbit_attributes_correct, fox_attributes_correct
from experiment_methods import experiment_contains_add_rabbits, experiment_contains_add_foxes
from experiment_methods import experiment_contains_rabbits_and_foxes

only("phase5.py")
