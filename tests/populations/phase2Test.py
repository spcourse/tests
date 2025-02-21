from checkpy import *
from pathlib import Path
from shared import collect_all_of_type, has_main, contains_rabbit, contains_experiment
from shared import rabbit_attributes, rabbit_values
from movement import rabbit_step1, rabbit_step2, rabbit_step3
from experiment_methods import experiment_contains_add_rabbits

only("phase2.py")

@passed(contains_rabbit, contains_experiment, timeout=10, hide=False)
def experiment_contains_rabbits():
    """Experiment contains 10 Rabbits, after intializing:
        experiment = Experiment(1, 10)"""
    Rabbit = getModule().Rabbit._function
    Experiment = getModule().Experiment._function
    experiment = Experiment(1, 10)
    rabbits_in_experiment = collect_all_of_type(experiment, Rabbit)

    assert len(rabbits_in_experiment) <= 10, "Experiment contains more than 10 Rabbits"
    assert len(rabbits_in_experiment) == 10, "Experiment contains less than 10 Rabbits"
