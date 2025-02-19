from checkpy import *
from math import pi
from shared import *
import dis

@passed(contains_rabbit, contains_creature, timeout=10, hide=False)
def rabbit_is_creature():
    """Rabbit inherits from Creature"""
    Rabbit = getModule().Rabbit._function
    Creature = getModule().Creature._function
    assert len(Rabbit.__bases__) == 1, "Expecting Rabbit to inherit from exactly one parent class"
    parent = Rabbit.__bases__[0]
    assert parent == Creature, "Expecting parent of Rabbit to be Creature"

@passed(contains_rabbit, contains_creature, timeout=10, hide=False)
def fox_is_creature():
    """Fox inherits from Creature"""
    Fox = getModule().Fox._function
    Creature = getModule().Creature._function
    assert len(Fox.__bases__) == 1, "Expecting Fox to inherit from exactly one parent class"
    parent = Fox.__bases__[0]
    assert parent == Creature, "Expecting parent of Fox to be Creature"

@passed(contains_rabbit, contains_creature, timeout=10, hide=False)
def rabbit_attribbutes_set_in_init():
    """All Rabbit attributes are set in the init methods"""

    Rabbit = getModule().Rabbit._function
    Creature = getModule().Creature._function
    init_attrs = get_init_attr(Rabbit) | get_init_attr(Creature)

    for attr in ["pos_x", "pos_y", "angle", "speed", "color"]:
        assert attr in init_attrs, f"attribute: {attr} is not defined in .__init__()"

@passed(contains_rabbit, contains_creature, timeout=10, hide=False)
def fox_attribbutes_set_in_init():
    """All Fox attributes are set in the init methods"""

    Fox = getModule().Fox._function
    Creature = getModule().Creature._function
    init_attrs = get_init_attr(Fox) | get_init_attr(Creature)

    for attr in ["pos_x", "pos_y", "angle", "speed", "color"]:
        assert attr in init_attrs, f"attribute: {attr} is not defined in .__init__()"


@passed(rabbit_attribbutes_set_in_init, fox_attribbutes_set_in_init, timeout=10, hide=False)
def creature_attributes_correct():
    """Creature sets "pos_x", "pos_y", "angle" attributes"""
    Creature = getModule().Creature._function
    init_attrs = get_init_attr(Creature)

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr in init_attrs, f"attribute: {attr} is not set in Creature"

@passed(rabbit_attribbutes_set_in_init, timeout=10, hide=False)
def rabbbit_attributes_correct():
    """Rabbbit does not set "pos_x", "pos_y", "angle" attributes"""
    Rabbit = getModule().Rabbit._function
    init_attrs = get_init_attr(Rabbit)

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr not in init_attrs, f"attribute: {attr} is set in Rabbit (but should be set in Creature)"

@passed(fox_attribbutes_set_in_init, timeout=10, hide=False)
def fox_attributes_correct():
    """Fox does not set "pos_x", "pos_y", "angle" attributes"""
    Fox = getModule().Fox._function
    init_attrs = get_init_attr(Fox)

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr not in init_attrs, f"attribute: {attr} is set in Fox (but should be set in Creature)"

def get_init_attr(tclass):
    return {instr.argval
        for instr in dis.get_instructions(tclass.__init__)
        if instr.opname == "STORE_ATTR"}
#
#     assert "pos_x" in fields, "required attribute: pos_x"
#     assert "pos_y" in fields, "required attribute: pos_y"
#     assert "angle" in fields, "required attribute: angle"
#     assert "speed" in fields, "required attribute: speed"
#     assert "color" in fields, "required attribute: color"

# @passed(rabbit_attributes, hide=False)
# def rabbit_values():
#     """Rabbit contains all attribute values set correctly
#         rabbit = Rabbit(0.1, 0.1, 10)"""
#
#     Rabbit = getModule().Rabbit._function
#     rabbit = Rabbit(0.1, 0.1, 10)
#
#     assert rabbit.pos_x == 0.1
#     assert rabbit.pos_y == 0.1
#     assert rabbit.angle == 10
#     assert rabbit.color == "blue"
#     assert rabbit.speed == 0.01



# @passed(contains_fox, timeout=10, hide=False)
# def fox_attributes():
#     """Rabbit contains all important attributes
#         fox = Fox(0.1, 0.1, 10)"""
#
#     Fox = getModule().Fox._function
#     fox = Fox(0.1, 0.1, 10)
#
#     fields = fox.__dict__
#     assert "pos_x" in fields, "required attribute: pos_x"
#     assert "pos_y" in fields, "required attribute: pos_y"
#     assert "angle" in fields, "required attribute: angle"
#     assert "speed" in fields, "required attribute: speed"
#     assert "color" in fields, "required attribute: color"
#
# @passed(fox_attributes, hide=False)
# def fox_values():
#     """Rabbit contains all attribute values set correctly
#         fox = Fox(0.1, 0.1, 10)"""
#
#     Fox = getModule().Fox._function
#     fox = Fox(0.1, 0.1, 10)
#
#     assert fox.pos_x == 0.1
#     assert fox.pos_y == 0.1
#     assert fox.angle == 10
#     assert fox.color == "red"
#     assert fox.speed == 0.03
