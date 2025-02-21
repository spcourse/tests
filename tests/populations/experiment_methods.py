from checkpy import *
from shared import *

@passed(contains_rabbit, contains_experiment, timeout=10, hide=False)
def experiment_contains_add_rabbits():
    """Experiment contains 'add_rabbits' method."""
    Experiment = getModule().Experiment._function
    assert callable(Experiment.__dict__.get("add_rabbits")), "Experiment does not contain 'add_rabbits' method."

@passed(contains_rabbit, contains_experiment, timeout=10, hide=False)
def experiment_contains_add_foxes():
    """Experiment contains 'add_foxes' method."""
    Experiment = getModule().Experiment._function
    assert callable(Experiment.__dict__.get("add_foxes")), "Experiment does not contain 'add_foxes' method."

@passed(contains_rabbit, contains_experiment, timeout=10, hide=False)
def experiment_contains_rabbits_and_foxes():
    """Experiment contains 10 Rabbits and 5 Foxes after intializing:
        experiment = Experiment(1, 10, 5)"""
    Rabbit = getModule().Rabbit._function
    Fox = getModule().Fox._function
    Experiment = getModule().Experiment._function
    experiment = Experiment(1, 10, 5)
    rabbits_in_experiment = collect_all_of_type(experiment, Rabbit)
    foxes_in_experiment = collect_all_of_type(experiment, Fox)

    assert len(rabbits_in_experiment) <= 10, "Experiment contains more than 10 Rabbits"
    assert len(rabbits_in_experiment) == 10, "Experiment contains less than 10 Rabbits"
    assert len(foxes_in_experiment) <= 5, "Experiment contains more than 5 Foxes"
    assert len(foxes_in_experiment) == 5, "Experiment contains less than 5 Foxes"
