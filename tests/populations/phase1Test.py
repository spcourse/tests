from checkpy import *
from pathlib import Path
from shared import collect_all_of_type, has_main, contains_rabbit, contains_experiment, rabbit_attributes, rabbit_values
from movement import rabbit_step1, rabbit_step2, rabbit_step3

only("phase1.py")




@passed(contains_rabbit, contains_experiment, timeout=10, hide=False)
def test2():
    """Experiment contains one Rabbit, after intializing:
        rabbit = Rabbit(0.1, 0.1, 10)
        experiment = Experiment(rabbit)"""
    Rabbit = getModule().Rabbit._function
    Experiment = getModule().Experiment._function
    rabbit = Rabbit(0.1, 0.1, 10)
    experiment = Experiment(rabbit)
    rabbits_in_experiment = collect_all_of_type(experiment, Rabbit)

    assert len(rabbits_in_experiment) <= 1, "Experiment contains more than one Rabbit"
    assert len(rabbits_in_experiment) == 1, "Experiment does not contain a Rabbit"
