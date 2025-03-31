from checkpy import *
from math import pi
from shared import *

@passed(rabbit_values, hide=False)
def rabbit_step1():
    """Rabbit steps correctly
        rabbit = Rabbit(0.1, 0.1, 0)
        rabbit.step()"""

    Rabbit = getModule().Rabbit._function
    rabbit = Rabbit(0.1, 0.1, 0)
    rabbit.step()
    assert rabbit.pos_x == approx(0.11, abs=0.0001), "expected pos_x: 0.11"
    assert rabbit.pos_y == approx(0.1, abs=0.0001), "expected pos_y: 0.1"

@passed(rabbit_values, hide=False)
def rabbit_step2():
    """Rabbit steps correctly
        rabbit = Rabbit(0.1, 0.1, pi/2)
        rabbit.step()"""

    Rabbit = getModule().Rabbit._function
    rabbit = Rabbit(0.1, 0.1, pi/2)
    rabbit.step()
    assert rabbit.pos_x == approx(0.1, abs=0.0001), "expected pos_x: 0.1"
    assert rabbit.pos_y == approx(0.11, abs=0.0001), "expected pos_y: 0.11"

@passed(rabbit_values, hide=False)
def rabbit_step3():
    """Rabbit turns around correctly at the edge
        rabbit = Rabbit(0.995, 0.5, 0)
        rabbit.step()

    The rabbit should not move, and it's angle should become pi."""

    Rabbit = getModule().Rabbit._function
    rabbit = Rabbit(0.995, 0.5, 0)
    rabbit.step()
    assert rabbit.pos_x == approx(0.995, abs=0.0001), "expected pos_x remains: 0.995"
    assert rabbit.pos_y == approx(0.5, abs=0.0001), "expected pos_y remains: 0.5"
    assert rabbit.angle == approx(pi, abs=0.0001), "expected angle changed to: pi"
