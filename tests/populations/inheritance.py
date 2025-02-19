from checkpy import *
from math import pi
from shared import *
import ast

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
    ast_node = static.AbstractSyntaxTree()
    # Rabbit = getModule().Rabbit._function
    # Creature = getModule().Creature._function
    init_attrs = get_init_attr(ast_node, "Rabbit") | get_init_attr(ast_node, "Creature")

    for attr in ["pos_x", "pos_y", "angle", "speed", "color"]:
        assert attr in init_attrs, f"attribute: self.{attr} is not defined in .__init__()"

@passed(contains_rabbit, contains_creature, timeout=10, hide=False)
def fox_attribbutes_set_in_init():
    """All Fox attributes are set in the init methods"""
    ast_node = static.AbstractSyntaxTree()
    # Fox = getModule().Fox._function
    # Creature = getModule().Creature._function
    init_attrs = get_init_attr(ast_node, "Fox") | get_init_attr(ast_node, "Creature")

    for attr in ["pos_x", "pos_y", "angle", "speed", "color"]:
        assert attr in init_attrs, f"attribute: self.{attr} is not defined in .__init__()"


@passed(rabbit_attribbutes_set_in_init, fox_attribbutes_set_in_init, timeout=10, hide=False)
def creature_attributes_correct():
    """Creature sets "pos_x", "pos_y", "angle" attributes"""
    # Creature = getModule().Creature._function
    init_attrs = get_init_attr(static.AbstractSyntaxTree(), "Creature")

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr in init_attrs, f"attribute: self.{attr} is not set in Creature"

@passed(rabbit_attribbutes_set_in_init, timeout=10, hide=False)
def rabbbit_attributes_correct():
    """Rabbbit does not set "pos_x", "pos_y", "angle" attributes"""
    # Rabbit = getModule().Rabbit._function
    init_attrs = get_init_attr(static.AbstractSyntaxTree(), "Rabbit")

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr not in init_attrs, f"attribute: self.{attr} is set in Rabbit (but should be set in Creature)"

@passed(fox_attribbutes_set_in_init, timeout=10, hide=False)
def fox_attributes_correct():
    """Fox does not set "pos_x", "pos_y", "angle" attributes"""
    # Fox = getModule().Fox._function
    init_attrs = get_init_attr(static.AbstractSyntaxTree(), "Fox")

    for attr in ["pos_x", "pos_y", "angle"]:
        assert attr not in init_attrs, f"attribute: self.{attr} is set in Fox (but should be set in Creature)"



### get_init_attr
def get_init_attr(ast_node, class_name):
    # find ast node for class def of class_name
    class_nodes = static.getAstNodes(ast.ClassDef)
    class_node = None
    for node in class_nodes:
        if node.name == class_name:
            class_node = node

    init_visitor = InitVisitor()
    init_visitor.visit(class_node)
    init_node = init_visitor.init_node

    assign_visitor = AssignTargetVisitor()
    assign_visitor.visit(init_node)

    return {target.attr
        for target in assign_visitor.targets
        if type(target) == ast.Attribute
    }

class InitVisitor(ast.NodeVisitor):
    def __init__(self):
        self.init_node = None

    def visit_FunctionDef(self, node):
        if node.name == "__init__":
            self.init_node = node

class AssignTargetVisitor(ast.NodeVisitor):
    def __init__(self):
        self.targets = []
    def visit_Assign(self, node):
        self.targets += node.targets
